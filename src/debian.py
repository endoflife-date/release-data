import json
import pathlib
import subprocess
from hashlib import sha1
from os.path import exists
from subprocess import call

"""Fetch Debian versions with their dates from www.debian.org source repository.
"""

PRODUCT = "debian"
REPO_URL = "https://salsa.debian.org/webmaster-team/webwml.git"
REPO_SHA1 = sha1(REPO_URL.encode()).hexdigest()
REPO_DIR = pathlib.Path(f"~/.cache/git/debian.md_{REPO_SHA1}").expanduser()


# Checkout the Debian website repository.
def clone_repository():
    git_opts = f"--git-dir={REPO_DIR}/.git --work-tree={REPO_DIR}"
    REPO_DIR.mkdir(parents=True, exist_ok=True)

    if not exists(f"{REPO_DIR}/.git"):
        call(f"git {git_opts} init", shell=True)
        call(f"git {git_opts} remote add origin {REPO_URL}", shell=True)

    call(f"git {git_opts} config core.sparseCheckout true", shell=True)
    with open(f"{REPO_DIR}/.git/info/sparse-checkout", "w") as f:
        f.write("english/News/")

    ret_code = call(f"git {git_opts} pull --depth 1 origin master", shell=True)
    exit(-ret_code) if ret_code < 0 else None

def extract_major_releases(releases):
    child = subprocess.Popen(
        f"grep -RhE -A 1 '<define-tag pagetitle>Debian [0-9]+.+</q> released' {REPO_DIR}/english/News "
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
                print(f"{date} : {version}")
                releases[version] = date
                is_release_line = True


def extract_point_releases(releases):
    child = subprocess.Popen(
        f"grep -Rh -B 10 '<define-tag revision>' {REPO_DIR}/english/News "
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
            print(f"{date} : {version}")
            releases[version] = date


def main():
    print(f"::group::{PRODUCT}")
    clone_repository()

    releases = {}
    extract_major_releases(releases)
    extract_point_releases(releases)
    print("::endgroup::")

    with open(f"releases/{PRODUCT}.json", "w") as f:
        f.write(json.dumps(dict(sorted(releases.items())), indent=2))


if __name__ == '__main__':
    main()
