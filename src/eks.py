import pygit2
import re
from datetime import datetime
import json

PATH = 'doc_source/kubernetes-versions.md'
TEMP_REPO_PATH = '/tmp/eks-docs'
REGEX = r"^\+ (?P<major>\d+)\\\.(?P<minor>\d+)\\\.(?P<patch>\d+)$"

versions = {}

def add_versions(c_versions, commit):
  for v in c_versions:
    if v not in versions:
      version_string = "%s.%s.%s" % v
      date = datetime.fromtimestamp(commit.commit_time).strftime('%Y-%m-%d')
      versions[version_string] = date

def get_versions(markdown):
  return re.findall(REGEX, markdown, re.MULTILINE)

repo = pygit2.Repository(TEMP_REPO_PATH)
prev = None
tree_list = []
for cur in repo.walk(repo.head.target):
  if prev is not None:
    for d in cur.tree.diff_to_tree(prev.tree).deltas:
      if(d.new_file.path ==  PATH and PATH in cur.tree):
        contents = cur.tree[PATH].data.decode('UTF-8')
        add_versions(get_versions(contents), cur)

  if cur.parents:
    prev = cur
    cur = cur.parents[0]

with open('releases/eks.json', 'w') as f:
  f.write(json.dumps(versions, indent=2))

