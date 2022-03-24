require 'yaml'
require 'date'

WEBSITE_DIR=ARGV[0]
CACHE_DIR=ARGV[1]
OUTPUT_DIR=ARGV[2]

def update_git_releases(product, url)
  pwd = Dir.pwd
  repo_dir = "#{CACHE_DIR}/git/#{product}"
  puts "Fetching #{url}"
  unless Dir.exist? repo_dir
    `git init --bare #{repo_dir}`
  end
  Dir.chdir repo_dir
  `git config extensions.partialClone true`
  `git fetch --auto-gc --auto-maintenance --progress --prune --prune-tags --quiet --tags --filter=blob:none "#{url}"`
  Dir.chdir pwd
end

pp ARGV

Dir.glob("#{WEBSITE_DIR}/products/*.md").each do |product_file|
  data = YAML.load_file product_file, permitted_classes: [Date]
  data['auto'].each_entry do |ecosystem, url|
    product = File.basename product_file, ".md"
    case ecosystem
    when 'git'
      update_git_releases(product, url)
    else
      puts "No support for #{ecosystem} yet (#{url})"
    end
  end if data['auto']
end
