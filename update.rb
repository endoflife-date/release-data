require 'yaml'
require 'set'
require 'date'
require 'json'
require 'rugged'
require 'liquid'

WEBSITE_DIR = ARGV[0]
CACHE_DIR = ARGV[1]
OUTPUT_DIR = ARGV[2]
OPTIONAL_PRODUCT = ARGV[3]

# This regex is used in absence of anything else
# This is more lenient from semver, but disallows MAJOR=0 as well
# It also allows MAJOR.MINOR, which is quite common
DEFAULT_VERSION_REGEX = '^v?(?<major>[1-9]\d*)\.(?<minor>0|[1-9]\d*)\.?(?<patch>0|[1-9]\d*)?$'
DEFAULT_TAG_TEMPLATE = '{{major}}.{{minor}}{% if patch %}.{{patch}}{%endif%}'

def fetch_git_releases(repo_dir, url)
  pwd = Dir.pwd
  puts "Fetching #{url}"
  `git init --bare #{repo_dir}` unless Dir.exist? repo_dir
  Dir.chdir repo_dir
  `git fetch --quiet --tags --filter=blob:none "#{url}"`
  Dir.chdir pwd
end

def good_tag(tag, config)
  config['regex'] ||= DEFAULT_VERSION_REGEX
  tag.match?(config['regex'])
end

def render_tag(tag, config)
  config['regex'] ||= DEFAULT_SEMVER_REGEX
  data = tag.match(config['regex']).named_captures

  template = config['template'] ? config['template'] : DEFAULT_TAG_TEMPLATE
  Liquid::Template.parse(template).render(data)
end

def update_git_releases(repo_dir, output_file, auto_config)
  data = {}
  repo = Rugged::Repository.bare repo_dir
  repo.tags.each do |tag|
    next unless good_tag(tag.name, auto_config)

    tag_proper_name = render_tag(tag.name, auto_config)

    if tag.target.is_a? Rugged::Tag::Annotation
      data[tag_proper_name] = tag.target.tagger[:time].strftime('%F')
    else
      begin
        data[tag_proper_name] = tag.target.time.strftime('%F')
      rescue StandardError
        puts "[WARN] No timestamp for #{tag.name}"
      end
    end
  end
  File.open(output_file, 'w') do |file|
    file.write(JSON.pretty_generate(data))
  end
end

def get_cache_dir(ecosystem, product)
  "#{CACHE_DIR}/#{ecosystem}/#{product}"
end

def get_output_file(ecosystem, product)
  "#{OUTPUT_DIR}/#{ecosystem}/#{product}.json"
end

def generate_commit_message
  products = Set.new
  ret = nil
  msg = ""
  r = Rugged::Repository.new '.'
  r.status() do |f, s|
    p = Pathname.new(f).dirname
    if p.to_s === 'releases/git'
      ret = true
      product =  File.basename(f, '.json')
      products << product
      old_version_list = JSON.parse(r.blob_at(r.head.target.oid, f).content).keys.to_set
      new_version_list = JSON.parse(File.read(f)).keys.to_set
      new_versions = (new_version_list - old_version_list)
      msg += "#{product}: #{new_versions.join(', ')}"
    end
  end
  ret ? "Updates: #{products.join(', ')}\n\n#{msg}": false
end

Dir.glob("#{WEBSITE_DIR}/products/*.md").each do |product_file|
  data = YAML.safe_load_file product_file, permitted_classes: [Date]
  next unless data['auto']

  product = File.basename product_file, '.md'

  next if OPTIONAL_PRODUCT && (OPTIONAL_PRODUCT != product)

  if data['auto']['git']
    fetch_git_releases(get_cache_dir('git', product), data['auto']['git'])
    update_git_releases(get_cache_dir('git', product), get_output_file('git', product), data['auto'])
  end
end

def github_actions_step_output(msg)
  puts "::set-output name=commit_message::#{JSON.dump(msg)}"
end

msg = generate_commit_message
github_actions_step_output(msg) if msg
