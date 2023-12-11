import re
from common import dates
from common import endoflife
from common.git import Git

"""Fetches Red Hat OpenShift versions from the documentation's git repository"""

VERSION_AND_DATE_PATTERN = re.compile(r"{product-title}\s(?P<version>\d+\.\d+\.\d+).*\n+Issued:\s(?P<date>\d{4}-\d\d-\d\d)$", re.MULTILINE)

product = endoflife.Product("red-hat-openshift")
print(f"::group::{product.name}")
git = Git("https://github.com/openshift/openshift-docs.git")
git.setup()

# only fetch v4+ branches, because the format was different in openshift v3
for branch in git.list_branches("refs/heads/enterprise-[4-9]*"):
    version = branch.split("-")[1].replace(".", "-")
    release_notes_filename = f"release_notes/ocp-{version}-release-notes.adoc"
    git.checkout(branch, file_list=[release_notes_filename])

    release_notes_file = git.repo_dir / release_notes_filename
    if not release_notes_file.exists():
        continue

    with open(release_notes_file, "rb") as f:
        content = f.read().decode("utf-8")
        for (version, date_str) in VERSION_AND_DATE_PATTERN.findall(content):
            product.declare_version(version, dates.parse_date(date_str))

product.write()
print("::endgroup::")
