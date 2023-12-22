require 'set'
require 'json'
require 'rugged'

def generate_commit_message
  begin
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

    commit_title = products.join(', ')
    return ret ? "🤖: #{commit_title}\n\n#{msg}": ""

  rescue StandardError => e
    return "🤖: Automatic Update"
  end
end

def github_actions_step_output(msg)
  puts "::set-output name=commit_message::#{JSON.dump(msg)}"
end

github_actions_step_output(generate_commit_message)
