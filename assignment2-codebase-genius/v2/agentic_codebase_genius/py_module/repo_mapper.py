import os
import tempfile
import shutil
from git import Repo
from pathlib import Path
import re

# Ignored directories and files
IGNORED_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', 'build', 'dist', '.pytest_cache', '.mypy_cache'}
IGNORED_FILES = {'.DS_Store', 'Thumbs.db'}

def clone_repo(repo_url: str) -> str:
    """
    Clone the repository to a temporary directory.
    Returns the path to the cloned repo.
    """
    try:
        temp_dir = tempfile.mkdtemp()
        Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    except Exception as e:
        raise ValueError(f"Failed to clone repository: {str(e)}")

def generate_file_tree(repo_path: str) -> dict:
    """
    Generate a structured file tree from the repository path.
    Returns a dict with 'name', 'type', 'children' for directories, or 'name', 'type' for files.
    """
    def build_tree(path: Path) -> dict:
        if path.is_file():
            return {'name': path.name, 'type': 'file'}
        elif path.is_dir():
            children = []
            for child in sorted(path.iterdir()):
                if child.name in IGNORED_DIRS or child.name in IGNORED_FILES:
                    continue
                children.append(build_tree(child))
            return {'name': path.name, 'type': 'directory', 'children': children}
        return {}

    root_path = Path(repo_path)
    return build_tree(root_path)

def summarize_readme(repo_path: str) -> str:
    """
    Read README.md and provide a concise summary.
    If no README, return a default message.
    """
    readme_path = Path(repo_path) / 'README.md'
    if not readme_path.exists():
        return "No README.md found. This repository does not have a description."

    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Simple heuristic summary: extract first paragraph or headings
        lines = content.split('\n')
        summary = []
        for line in lines[:10]:  # First 10 lines
            line = line.strip()
            if line and not line.startswith('#') and len(line) > 10:
                summary.append(line)
                if len(summary) >= 3:  # Up to 3 sentences
                    break

        if summary:
            return ' '.join(summary)
        else:
            return "README.md exists but no clear description found."

    except Exception as e:
        return f"Error reading README: {str(e)}"

def map_repository(repo_url: str) -> dict:
    """
    Main function: clone repo, generate file tree, summarize README.
    Returns dict with 'repo_path', 'file_tree', 'readme_summary'.
    """
    repo_path = clone_repo(repo_url)
    file_tree = generate_file_tree(repo_path)
    readme_summary = summarize_readme(repo_path)
    return {
        'repo_path': repo_path,
        'file_tree': file_tree,
        'readme_summary': readme_summary
    }
