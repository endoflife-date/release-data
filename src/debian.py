import subprocess
from common import endoflife
from common.git import Git

"""Fetch Debian versions with their dates from www.debian.org source repository.
"""

PRODUCT = "debian"
REPO_URL = "https://salsa.debian.org/webmaster-team/webwml.git"


def extract_major_releases(releases, repo_dir):
    child = subprocess.Popen(
        f"grep -RhE -A 1 '<define-tag pagetitle>Debian [0-9]+.+</q> released' {repo_dir}/english/News "
        f"| cut -d '<' -f 2 "
        f"| cut -d '>' -f 2 "
        f"| grep -v -- '--'",
        shell=True, stdout=subprocess.PIPE)
    output = child.communicate()[0].decode('utf-8')

    is_release_line = True
    version = None
    for line in output.split('\n'):
        if line:
            if is_release_line:
                version = line.split(" ")[1]
                is_release_line = False
            else:
                date = line
                releases[version] = date
                print(f"{version}: {date}")
                is_release_line = True


def extract_point_releases(releases, repo_dir):
    child = subprocess.Popen(
        f"grep -Rh -B 10 '<define-tag revision>' {repo_dir}/english/News "
        "| grep -Eo '(release_date>(.*)<|revision>(.*)<)' "
        "| cut -d '>' -f 2,4 "
        "| tr -d '<' "
        "| sed 's/[[:space:]]+/ /' "
        "| paste -d ' ' - -",
        shell=True, stdout=subprocess.PIPE)
    output = child.communicate()[0].decode('utf-8')

    for line in output.split('\n'):
        if line:
            parts = line.split(' ')
            date = parts[0]
            version = parts[1]
            print(f"{version}: {date}")
            releases[version] = date

git = Git(REPO_URL)
git.setup()
git.checkout("master", file_list=["english/News"])

print(f"::group::{PRODUCT}")
all_releases = {}
extract_major_releases(all_releases, git.repo_dir)
extract_point_releases(all_releases, git.repo_dir)
endoflife.write_releases(PRODUCT, dict(
    # sort by date then version (desc)
    sorted(all_releases.items(), key=lambda x: (x[1], x[0]), reverse=True)
))
print("::endgroup::")
