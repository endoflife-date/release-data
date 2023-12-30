import json
import logging
import subprocess
import sys

from common import dates, endoflife

"""Fetches versions from GitHub releases using the GraphQL API and the GitHub CLI.

Note: GraphQL API and GitHub CLI are used because it's simpler: no need to manage pagination and authentication.
"""

METHOD = "github_releases"


def fetch_releases(repo_id):
    logging.info(f"fetching {repo_id} GitHub releases")
    (owner, repo) = repo_id.split('/')
    child = subprocess.run("""gh api graphql --paginate -f query='
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
}'""" % (repo, owner), capture_output=True, timeout=300, check=True, shell=True)  # noqa: UP031
    logging.info(f"fetched {repo_id} GitHub releases")

    # splitting because response may contain multiple JSON objects on a single line
    responses = child.stdout.decode("utf-8").strip().replace('}{', '}\n{').split("\n")
    return [json.loads(response) for response in responses]


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product_name in endoflife.list_products(METHOD, p_filter):
    product = endoflife.Product(product_name)
    print(f"::group::{product.name}")

    product_frontmatter = endoflife.ProductFrontmatter(product.name)
    for config in product_frontmatter.get_auto_configs(METHOD):
        for page in fetch_releases(config.url):
            releases = [edge['node'] for edge in (page['data']['repository']['releases']['edges'])]

            for release in releases:
                if not release['isPrerelease']:
                    version_str = release['name']
                    version_match = config.first_match(version_str)
                    if version_match:
                        version = config.render(version_match)
                        date = dates.parse_datetime(release['publishedAt'])
                        product.declare_version(version, date)

    product.write()
    print("::endgroup::")
