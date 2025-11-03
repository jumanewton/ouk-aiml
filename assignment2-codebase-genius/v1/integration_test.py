import sys
import os
import shutil

sys.path.insert(0, 'py_modules')

from git_utils import clone_repo
from repo_mapper import map_repo

url = "https://github.com/octocat/Hello-World"

result = clone_repo(url)

if result['success']:
    mapped = map_repo(result['path'])
    print("Success:")
    print(mapped)
    # Clean up
    shutil.rmtree(result['path'])
else:
    print("Error:", result['error'])