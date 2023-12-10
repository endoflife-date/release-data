import regex as re
import sys
from common import endoflife
from common.git import Git
from liquid import Template

"""Fetch versions with their dates from tags in a git repository.

This replace the old update.rb script.

Note that this script is using the regex module because the Python re module does not support
identically named groups (as used in the mariadb product).
"""

# Default tag template and regex should include tiny version to properly handle blender,
# craft-cms, exim, gerrit, jquery, kdeplasma, kirby, logstash, nexus, silverstripe
# and tarantool versions.
METHOD = 'git'


def fetch_releases(url, regex, template):
    releases = {}

    git = Git(url)
    git.setup(bare=True)

    tags = git.list_tags()
    for tag, date in tags:
        match = re.match(regex, tag)
        if match:
            version = Template(template).render(match.groupdict())
            releases[version] = date
            print(f"{version}: {date}")

    return releases

def update_product(product_name, configs):
    versions = {}

    for config in configs:
        t = config.get("template", endoflife.DEFAULT_VERSION_TEMPLATE)
        regex = config.get("regex", endoflife.DEFAULT_VERSION_REGEX)
        regex = regex.replace("(?<", "(?P<")  # convert ruby regex to python regex
        versions = versions | fetch_releases(config[METHOD], regex, t)

    endoflife.write_releases(product_name, versions)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
