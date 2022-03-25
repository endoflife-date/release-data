require 'yaml'
require 'date'
require 'json'
require 'rugged'

WEBSITE_DIR=ARGV[0]
CACHE_DIR=ARGV[1]
OUTPUT_DIR=ARGV[2]

def fetch_git_releases(repo_dir, url)
  pwd = Dir.pwd
  puts "Fetching #{url}"
  unless Dir.exist? repo_dir
    `git init --bare #{repo_dir}`
  end
  Dir.chdir repo_dir
  `git fetch --quiet --tags --filter=blob:none "#{url}"`
  Dir.chdir pwd
end

def update_git_releases(repo_dir, output_file)
  data = {}
  repo = Rugged::Repository.bare repo_dir
  repo.tags.each do |tag|
    data[tag.name] = tag.target.time.strftime('%F')
  end
  File.open(output_file, 'w') do |file|
    file.write(JSON.pretty_generate data)
  end
end

Dir.glob("#{WEBSITE_DIR}/products/*.md").each do |product_file|
  data = YAML.load_file product_file, permitted_classes: [Date]
  data['auto'].each_entry do |ecosystem, url|
    product = File.basename product_file, ".md"
    cache_dir = "#{CACHE_DIR}/#{ecosystem}/#{product}"
    output_file = "#{OUTPUT_DIR}/#{ecosystem}/#{product}.json"
    case ecosystem
    when 'git'
      fetch_git_releases(cache_dir, url)
      update_git_releases(cache_dir, output_file)
    else
      puts "No support for #{ecosystem} yet (#{url})"
    end
  end if data['auto']
end
