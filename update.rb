require 'yaml'
require 'set'
require 'date'
require 'json'
require 'rugged'
require 'liquid'
require 'digest'

WEBSITE_DIR = ARGV[0]
CACHE_DIR = ARGV[1]
OUTPUT_DIR = ARGV[2]
OPTIONAL_PRODUCT = ARGV[3]

# This regex is used in absence of anything else
# This is more lenient from semver, but disallows MAJOR=0 as well
# It also allows MAJOR.MINOR, which is quite common
DEFAULT_VERSION_REGEX = '^v?(?<major>[1-9]\d*)\.(?<minor>0|[1-9]\d*)\.?(?<patch>0|[1-9]\d*)?$'
DEFAULT_TAG_TEMPLATE = '{{major}}.{{minor}}{% if patch %}.{{patch}}{%endif%}'

def fetch_git_releases(repo_dir, config)
  pwd = Dir.pwd
  `git init --bare #{repo_dir}` unless Dir.exist? repo_dir
  Dir.chdir repo_dir
  `git fetch --quiet --tags --filter=blob:none "#{config['git']}"`
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

def get_releases_from_git(repo_dir, auto_config)
  data = {}
  repo = Rugged::Repository.bare repo_dir
  repo.tags.each do |tag|
    next unless good_tag(tag.name, auto_config)

    tag_proper_name = render_tag(tag.name, auto_config)

    # If the tag has an annotation, we get accurate time information
    # from the tag annotation "tagger"
    begin
    if tag.annotated?
      # We pick the data from the "tagger" which includes offset information
      t = tag.annotation.tagger[:time]
      data[tag_proper_name] = t.strftime('%F')
      puts "#{tag_proper_name}: #{t.strftime('%F %X %z')}"
    else
      # In other cases, we de-reference the tag to get the commit
      # and use the date of the commit itself
      t = tag.target.committer[:time]
      data[tag_proper_name] = t.strftime('%F')
      puts "#{tag_proper_name}: #{t.strftime('%F %X %z')}"
    end
    rescue StandardError
      puts "::warning No timestamp for #{tag.name}, ignoring"
    end
  end
  return data
end

def get_cache_dir(ecosystem, product, config)
  h = Digest::SHA1.hexdigest config['git']
  "#{CACHE_DIR}/#{ecosystem}/#{product}_#{h}"
end

def get_output_file(product)
  "#{OUTPUT_DIR}/#{product}.json"
end

def generate_commit_message
  products = Set.new
  ret = nil
  msg = ""
  r = Rugged::Repository.new '.'
  r.status() do |f, s|
    p = Pathname.new(f).dirname
    if p.to_s === 'releases'
      ret = true
      product =  File.basename(f, '.json')
      products << product
      old_version_list = JSON.parse(r.blob_at(r.head.target.oid, f).content).keys.to_set
      new_version_list = JSON.parse(File.read(f)).keys.to_set
      new_versions = (new_version_list - old_version_list)
      msg += "#{product}: #{new_versions.join(', ')}\n"
    end
  end
  ret ? "🤖: #{products.join(', ')}\n\n#{msg}": ""
end

def get_releases(product, config, i)
  type = get_update_type(config)
  if type == 'git'
    dir = get_cache_dir('git', product, config)
    fetch_git_releases(dir, config)
    return get_releases_from_git(dir, config)
  else
    puts "Not implemented: #{type}"
    return {}
  end
end

def get_update_type(config)
  for i in ['git', 'oci', 'npm']
    return i if config[i]
  end
end

Dir.glob("#{WEBSITE_DIR}/products/*.md").each do |product_file|
  data = YAML.safe_load_file product_file, permitted_classes: [Date]
  next unless data['auto']

  product = File.basename product_file, '.md'

  # Only process one product
  next if OPTIONAL_PRODUCT && (OPTIONAL_PRODUCT != product)

  if data['auto']
    release_data = {}

    puts "::group::#{product}"
    data['auto'].each_with_index do |config, i|
      release_data.merge! get_releases(product, config, i)
    end

    File.open(get_output_file(product), 'w') do |file|
      file.write(JSON.pretty_generate(release_data))
    end
    puts "::endgroup::"
  end
end

def github_actions_step_output(msg)
  puts "::set-output name=commit_message::#{JSON.dump(msg)}"
end

github_actions_step_output(generate_commit_message)
