import json
import logging
import subprocess


class Release:
    def __init__(self, name: str, tag_name: str, published_at: str, is_prerelease: bool) -> None:
        self.name: str = name
        self.tag_name: str = tag_name
        self.published_at: str = published_at
        self.is_prerelease: bool = is_prerelease


def fetch_releases(repo_id: str) -> list[Release]:
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
          tagName
        }
      }
    }
  }
}'""" % (repo, owner), capture_output=True, timeout=300, check=True, shell=True)  # noqa: UP031
    logging.info(f"fetched {repo_id} GitHub releases")

    # splitting because response may contain multiple JSON objects on a single line
    responses = child.stdout.decode("utf-8").strip().replace('}{', '}\n{').split("\n")
    pages = [json.loads(response) for response in responses]

    releases = []
    for page in pages:
        for edge in page['data']['repository']['releases']['edges']:
            release_data = edge['node']
            releases.append(Release(release_data['name'], release_data['tagName'], release_data['publishedAt'],
                                    release_data['isPrerelease']))

    return releases
