import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, 'py_modules')

from py_modules.supervisor import generate_docs

def main():
    if len(sys.argv) > 1:
        repo_url = sys.argv[1]
    else:
        repo_url = "https://github.com/octocat/Spoon-Knife"

    result = generate_docs(repo_url)
    if result["success"]:
        print(f"Docs generated at {result['docs_path']}")
    else:
        print(f"Error: {result['error']}")

if __name__ == "__main__":
    main()