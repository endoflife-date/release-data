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
DEFAULT_VERSION_REGEX = r"^v?(?P<major>[1-9]\d*)\.(?P<minor>\d+)(\.(?P<patch>\d+)(\.(?P<tiny>\d+))?)?$"
DEFAULT_TAG_TEMPLATE = "{{major}}.{{minor}}{% if patch %}.{{patch}}{% if tiny %}.{{tiny}}{%endif%}{%endif%}"


def fetch_releases(product_name, url, regex, template):
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
    releases = {}

    for config in configs:
        t = config.get("template", DEFAULT_TAG_TEMPLATE)
        regex = config.get("regex", DEFAULT_VERSION_REGEX)
        regex = regex.replace("(?<", "(?P<")  # convert ruby regex to python regex
        releases = releases | fetch_releases(product_name, config[METHOD], regex, t)

    endoflife.write_releases(product_name, releases)


p_filter = sys.argv[1] if len(sys.argv) > 1 else None
for product, configs in endoflife.list_products(METHOD, p_filter).items():
    print(f"::group::{product}")
    update_product(product, configs)
    print("::endgroup::")
