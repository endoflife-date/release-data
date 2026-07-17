from glob import glob
from packageurl import PackageURL
import os
from collections import namedtuple
import re
import sys
import json
import frontmatter
import urllib.request

# Repology tracks hundreds of distros
# and repositories. We only want packages
# against popular ones, so this is our filtered list
REPOSITORIES = {
    # No suggestion yet: https://github.com/package-url/purl-spec/pulls?q=bsd
    # openbsd, pkgsrc
    # Probably worth adding: Scientific Linux
    "ubuntu_": {"type": "deb", "namespace": "ubuntu", "path": "deb/ubuntu.yaml"},
    "raspbian_": {"type": "deb", "namespace": "raspbian", "path": "deb/raspbian.yaml"},
    "opensuse_leap_": {"type": "rpm", "namespace": "opensuse", "path": "rpm/opensuse/opensuse.yaml"},
    # TODO: Validate path for gentoo
    # "gentoo": {"namespace": "gentoo", "type": "ebuild", "path": "deb/ubuntu.yaml"},
    "fedora_": {"type": "rpm", "namespace": "fedora", "path": "rpm/fedora.yaml"},
    "debian_": {"type": "deb", "namespace": "debian", "path": "deb/debian.yaml"},
    "devuan_": {"type": "deb", "namespace": "devuan", "path": "deb/devuan.yaml"},
    "centos_": {"type": "rpm", "namespace": "centos", "path": "rpm/centos.yaml"},
    "amazon_": {"type": "rpm", "namespace": "amazon", "path": "rpm/amazonlinux.yaml"},
    "homebrew": {"type": "brew", "path": "macosx/homebrew/*.yaml"},
    "alpine_": {"type": "apk", "namespace": "alpine", "path": "alpine/alpine.yaml"},
    "arch_": {"type": "arch", "namespace": "arch", "path": "arch/arch.yaml"},
}

def generate_purl(package_info):
    # Find the first key in REPOSITORIES that matches the package_info['repo']
    # using startswith
    k = next((k for k in REPOSITORIES if package_info["repo"].startswith(k)), None)
    distro_info = REPOSITORIES[k]
    name = package_info.get('name', package_info.get('srcname', package_info.get('binname')))
    if not name:
        return None
    q = {}

    if distro_info['namespace'] in ['debian', 'ubuntu']:
        q['distro'] = package_info['subrepo'].split('_').first()
    elif distro_info['namespace'] in ['fedora']:
        q['distro'] = package_info['repo'].replace('_', '-')


    # TODO: Deal with subpath
    t = namedtuple(
        type=distro_info['type'],
        namespace=distro_info.get('namespace'),
        name=name,
        version=package_info['origversion'],
        qualifiers=q
    )


def fetch_releases(repology_ids):
    releases = []

    # See https://repology.org/api
    # All 3 name fields are optional, so we check for all 3
    # we skip on license, maintainers, categories, summary, visiblename fields
    def filterPackageInfo(p):
        KEYS = [
            "name",
            "srcname",
            "binname",
            "repo",
            "subrepo",
            "version",
            "origversion",
            "status",
        ]
        return {k: p[k] for k in KEYS if k in p}

    for repology_id in repology_ids:
        url = "https://repology.org/api/v1/project/%s" % repology_id
        with urllib.request.urlopen(url, data=None, timeout=5) as response:
            data = json.loads(response.read().decode())
            for package in data:
                for r in REPOSITORIES:
                    if package["repo"].startswith(r):
                        releases.append(filterPackageInfo(package))
    return releases


def get_repology_identifiers(config):
    if "identifiers" in config:
        return [x["repology"] for x in config["identifiers"] if "repology" in x]
    return []


def update_releases(product_filter=None):
    for product_file in glob("website/products/*.md"):
        product_name = os.path.splitext(os.path.basename(product_file))[0]
        if product_filter and product_name != product_filter:
            continue
        with open(product_file, "r") as f:
            data = frontmatter.load(f)
            repology_ids = get_repology_identifiers(data)
            update_product(product_name, repology_ids)


def update_product(product_name, repology_ids):
    print("::group::%s" % product_name)
    r = fetch_releases(repology_ids)
    with open("packages/%s.json" % product_name, "w") as f:
        f.write(json.dumps(r, indent=2))
    print("::endgroup::")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        update_releases(sys.argv[1])
    else:
        update_releases()
