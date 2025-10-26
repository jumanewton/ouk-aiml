import os
import json
from pathlib import Path
from typing import Dict, List, Any
import byllm

IGNORE_PATTERNS = {".git", "node_modules", ".venv", "__pycache__", ".DS_Store"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def build_file_tree(root_path: str) -> Dict[str, Any]:
    """
    Build a nested dictionary representing the file tree, ignoring certain patterns and large files.
    """
    root = Path(root_path)
    if not root.is_dir():
        return {}
    tree = {}

    def add_to_tree(path: Path, tree_dict: Dict):
        if path.name in IGNORE_PATTERNS or path.is_file() and path.stat().st_size > MAX_FILE_SIZE:
            return
        if path.is_dir():
            tree_dict[path.name] = {}
            for child in sorted(path.iterdir()):
                add_to_tree(child, tree_dict[path.name])
        else:
            tree_dict[path.name] = {"type": "file", "size": path.stat().st_size}

    for child in sorted(root.iterdir()):
        add_to_tree(child, tree)
    return tree

def find_readme(root_path: str) -> str:
    """
    Find and read the README file (README.md, README.rst, etc.).
    """
    readme_names = ["README.md", "README.rst", "README.txt", "README", "readme.md"]
    for name in readme_names:
        readme_path = Path(root_path) / name
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except Exception:
                pass
    return ""

def summarize_readme(readme_content: str) -> str:
    """
    Summarize the README content using LLM if available.
    Falls back to a simple heuristic summary when LLM isn't configured or fails.
    """
    if not readme_content:
        return "No README found."

    # Try using a language model if available (byllm). Fall back to a short heuristic
    try:
        prompt = (
            """
You are given the contents of a project's README. Return a concise (1-3 sentence) summary suitable for the top of generated documentation. Do not invent facts; if something is unclear use the phrase 'summary unclear from README'. Keep it neutral and factual.

README:
"""
            + readme_content[:5000]
            + "\n\nSummary:"
        )
        response = byllm.generate(prompt)
        if response and isinstance(response, str) and response.strip():
            return response.strip()
    except Exception:
        # best-effort: continue to fallback
        pass

    # Fallback: first non-empty lines up to a short character budget
    lines = [l.strip() for l in readme_content.split('\n') if l.strip()]
    if not lines:
        return "No README found."
    summary_lines = []
    chars = 0
    for l in lines[:10]:
        summary_lines.append(l)
        chars += len(l)
        if chars > 240:
            break
    return "Summary: " + " ".join(summary_lines).strip()

def find_entry_points(root_path: str) -> List[str]:
    """
    Find candidate entry points based on heuristics.
    """
    entry_files = []
    root = Path(root_path)

    # Specific files (top-level)
    candidates = ["main.py", "app.py", "__main__.py", "setup.py", "pyproject.toml", "Procfile"]
    for cand in candidates:
        p = root / cand
        if p.exists():
            entry_files.append(str(p))

    # .jac files
    for jac_file in root.rglob("*.jac"):
        entry_files.append(str(jac_file))

    # Top-level package __init__.py
    for init_file in root.glob("*/__init__.py"):
        entry_files.append(str(init_file))

    # Files with if __name__ == "__main__"
    for py_file in root.rglob("*.py"):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'if __name__ == "__main__":' in content:
                    entry_files.append(str(py_file))
        except Exception:
            pass

    # Dedupe while preserving order
    seen = set()
    deduped = []
    for p in entry_files:
        if p not in seen:
            deduped.append(p)
            seen.add(p)

    # Limit results to a reasonable number (keep top candidates)
    return deduped[:50]

def map_repo(local_path: str) -> Dict[str, Any]:
    """
    Map the repository: build file tree, summarize README, find entry points.
    """
    file_tree = build_file_tree(local_path)
    readme_content = find_readme(local_path)
    readme_summary = summarize_readme(readme_content)
    entry_points = find_entry_points(local_path)

    return {
        "file_tree": file_tree,
        "readme_summary": readme_summary,
        "entry_points": entry_points
    }