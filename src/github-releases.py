import re
import sys
import subprocess
from common import endoflife

METHOD = "github_releases"
REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"


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
    """Returns this repository releases using
    https://docs.github.com/en/rest/releases/releases#list-releases. Only the
    first page is fetched: there are rate limit rules in place on the GitHub
    API, and the most recent releases are sufficient.
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
                print(f"{version}: {date}")

    return releases


def update_product(product_name, configs):
    releases = {}

    for config in configs:
        config = config if "regex" in config else config | {"regex": REGEX}
        releases = releases | fetch_releases(config[METHOD], config["regex"])

    endoflife.write_releases(product_name, releases)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
