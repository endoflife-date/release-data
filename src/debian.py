from subprocess import run

from common import dates, endoflife
from common.git import Git

"""Fetch Debian versions by parsing news in www.debian.org source repository."""


def extract_major_versions(product, repo_dir):
    child = run(
        f"grep -RhE -A 1 '<define-tag pagetitle>Debian [0-9]+.+</q> released' {repo_dir}/english/News "
        f"| cut -d '<' -f 2 "
        f"| cut -d '>' -f 2 "
        f"| grep -v -- '--'",
        capture_output=True, timeout=300, check=True, shell=True)

    is_release_line = True
    version = None
    for line in child.stdout.decode("utf-8").strip().split("\n"):
        if is_release_line:
            version = line.split(" ")[1]
            is_release_line = False
        else:
            product.declare_version(version, dates.parse_date(line))
            is_release_line = True


def extract_point_versions(product, repo_dir):
    child = run(
        f"grep -Rh -B 10 '<define-tag revision>' {repo_dir}/english/News "
        "| grep -Eo '(release_date>(.*)<|revision>(.*)<)' "
        "| cut -d '>' -f 2,4 "
        "| tr -d '<' "
        "| sed 's/[[:space:]]+/ /' "
        "| paste -d ' ' - -",
        capture_output=True, timeout=300, check=True, shell=True)

    for line in child.stdout.decode("utf-8").strip().split("\n"):
        (date, version) = line.split(' ')
        product.declare_version(version, dates.parse_date(date))


product = endoflife.Product("debian")
print(f"::group::{product.name}")
git = Git("https://salsa.debian.org/webmaster-team/webwml.git")
git.setup()
git.checkout("master", file_list=["english/News"])

extract_major_versions(product, git.repo_dir)
extract_point_versions(product, git.repo_dir)

product.write()
print("::endgroup::")
