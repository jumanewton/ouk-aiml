import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, 'py_modules')

from git_utils import clone_repo
from repo_mapper import map_repo
from ccg import build_ccg
from parser_utils import parse_file
from docgenie import generate_docs

def main():
    repo_url = "https://github.com/octocat/Hello-World"

    # Clone repo
    clone_result = clone_repo(repo_url)
    if not clone_result["success"]:
        print(f"Error cloning repo: {clone_result['error']}")
        return

    local_path = clone_result["path"]
    print(f"Cloned to {local_path}")

    # Map repo
    repo_map = map_repo(local_path)
    print("Repo mapped")

    # Plan: prioritize entry points
    targets = repo_map["entry_points"]
    if not targets:
        # Fallback to all Python files
        targets = [str(p) for p in Path(local_path).rglob("*.py")][:10]  # limit

    print(f"Targets: {targets}")

    # Build CCG
    ccg = build_ccg(targets)
    print("CCG built")

    # Get symbols
    symbols = []
    for target in targets:
        parsed = parse_file(target)
        symbols.extend(parsed["symbols"])

    print(f"Symbols: {len(symbols)}")

    # Assemble docs
    docs_path = generate_docs(repo_url, repo_map, ccg, symbols, targets, "./outputs")
    print(f"Docs generated at {docs_path}")

    # Clean up temp dir
    shutil.rmtree(local_path)
    print("Cleaned up")

if __name__ == "__main__":
    main()