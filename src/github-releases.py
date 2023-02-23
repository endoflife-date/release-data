from glob import glob
import os
import re
import sys
import json
import frontmatter
import subprocess

REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"
AUTO_KEY = "github_releases"


# This script is using the GitHub CLI with the GraphQL API in order to retrieve
# releases. The reasons are:
# - using 'gh release list' does not return all the releases
# - using the API, directly or via GitHub CLI, is slow, produces a lot of 502
#   errors, and is harder due to pagination.
# - using the GraphQL API directly is hard due to pagination.
# - using a library, such as graphql-python, is sightly harder than using the
#   GitHub CLI (and still requires a GITHUB_TOKEN).
def fetch_json(repo_id):
    (owner, repo) = repo_id.split('/')
    query = """gh api graphql --paginate -f query='
query($endCursor: String) {
  repository(name: "%s", owner: "%s") {
    releases(
      orderBy: {field: NAME, direction: ASC}
      first: 100
      after: $endCursor
    ) {
      pageInfo { hasNextPage, endCursor }
      edges {
        node {
          name
          publishedAt
          isPrerelease
        }
      }
    }
  }
}' --jq '.data.repository.releases.edges.[].node | select(.isPrerelease == false) | [.name, .publishedAt] | join(",")'
""" % (repo, owner)

    child = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE)
    return child.communicate()[0].decode('utf-8')


def fetch_releases(repo_id, regex):
    """Returns this repository releases using https://docs.github.com/en/rest/releases/releases#list-releases.
    Only the first page is fetched: there are rate limit rules in place on the GitHub API, and the most recent
    releases are sufficient.
    """
    releases = {}
    regex = [regex] if not isinstance(regex, list) else regex

    for release in fetch_json(repo_id).splitlines():
        (raw_version, raw_date) = release.split(',')

        for r in regex:
            match = re.search(r, raw_version)
            if match:
                version = match.group(1)
                date = raw_date.split("T")[0]
                releases[version] = date
                print("%s: %s" % (version, date))

    return releases


def update_product(product_name, configs):
    print("::group::%s" % product_name)
    releases = {}

    for config in configs:
        config = config if "regex" in config else config | {"regex": REGEX}
        releases = releases | fetch_releases(config[AUTO_KEY], config["regex"])

    with open(f"releases/{product_name}.json", "w") as f:
        f.write(json.dumps(releases, indent=2))
    print("::endgroup::")


def update_releases(product_filter=None):
    for product_file in glob("website/products/*.md"):
        product_name = os.path.splitext(os.path.basename(product_file))[0]
        if product_filter and product_name != product_filter:
            continue

        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            if "auto" in data:
                configs = list(filter(lambda config: AUTO_KEY in config.keys(), data["auto"]))
                if len(configs) > 0:
                    update_product(product_name, configs)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_releases(sys.argv[1])
    else:
        update_releases()
