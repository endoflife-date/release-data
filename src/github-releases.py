from glob import glob
import os
import re
import sys
import json
import frontmatter
import urllib.request

REGEX = r"^(?:(\d+\.(?:\d+\.)*\d+))$"
AUTO_KEY = "github_releases"


def fetch_releases(repo_id, regex):
    """Returns this repository releases using https://docs.github.com/en/rest/releases/releases#list-releases.

    Only the first page is fetched: there are rate limit rules in place on the GitHub API, and we only need the most
    recent releases.
    """
    releases = {}
    regex = [regex] if not isinstance(regex, list) else regex

    url = f"https://api.github.com/repos/{repo_id}/releases?per_page=100"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "endoflife.date",
        "X-GitHub-Api-Version": "2022-11-28",
        "Authorization": f"token {os.environ.get('GITHUB_API_TOKEN')}" if "GITHUB_API_TOKEN" in os.environ else ""
    }

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, data=None, timeout=5) as response:
        data = json.loads(response.read().decode("utf-8"))
        for release in data:
            raw_version = release["tag_name"]

            version = None
            for r in regex:
                match = re.search(r, raw_version)
                if match:
                    version = match.group(1)

            if version and not(release["draft"]) and not(release["prerelease"]):
                d = release["published_at"].split("T")[0]
                releases[version] = d
                print("%s: %s" % (version, d))

    return releases


def update_product(product_name, config):
    print("::group::%s" % product_name)
    config = config if "regex" in config else config | {"regex": REGEX}
    r = fetch_releases(config[AUTO_KEY], config["regex"])
    with open(f"releases/{product_name}.json", "w") as f:
        f.write(json.dumps(r, indent=2))
    print("::endgroup::")


def update_releases(product_filter=None):
    for product_file in glob("website/products/*.md"):
        product_name = os.path.splitext(os.path.basename(product_file))[0]
        if product_filter and product_name != product_filter:
            continue

        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            if "auto" in data:
                for config in data["auto"]:
                    for key, d_id in config.items():
                        if key == AUTO_KEY:
                            update_product(product_name, config)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_releases(sys.argv[1])
    else:
        update_releases()
