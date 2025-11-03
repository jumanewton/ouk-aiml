import os
from pathlib import Path
from typing import Dict, Any, List, Optional


def build_file_tree(root_path: str) -> Dict[str, Any]:
    """Build a nested dict representing files and folders under root_path.

    Directories are represented as dicts; files map to None.
    """
    root = Path(root_path)
    tree: Dict[str, Any] = {}

    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root)
        # normalize root
        if rel_dir == ".":
            container = tree
        else:
            parts = rel_dir.split(os.sep)
            container = tree
            for p in parts:
                container = container.setdefault(p, {})

        for d in dirnames:
            container.setdefault(d, {})
        for f in filenames:
            # store files as True (or could store metadata)
            container[f] = None

    return tree


def find_readme(root_path: str) -> Optional[str]:
    """Search for a README file (README.md, README.rst, README) and return its text.

    Search prefers top-level README, case-insensitive.
    """
    root = Path(root_path)
    candidates = ["README.md", "README.rst", "README"]

    # check top-level first
    for name in candidates:
        p = root / name
        if p.exists():
            try:
                return p.read_text(encoding="utf-8")
            except Exception:
                return None

    # fallback: walk and find first match
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            if fn.upper().startswith("README"):
                try:
                    return Path(dirpath, fn).read_text(encoding="utf-8")
                except Exception:
                    return None

    return None


def summarize_readme(content: str) -> str:
    """Return a lightweight summary for the README content.

    For now produce a deterministic short summary placeholder expected by tests.
    """
    if not content:
        return "No README found."

    # simple heuristic: first non-empty line + a short excerpt
    lines = [l.strip() for l in content.splitlines() if l.strip()]
    first = lines[0] if lines else ""
    excerpt = (" ").join(lines[1:4]) if len(lines) > 1 else ""
    summary = f"Summary: {first}"
    if excerpt:
        summary += f" — {excerpt[:240]}"
    return summary


def find_entry_points(root_path: str) -> List[str]:
    """Find probable entry points in the repository.

    Looks for files named setup.py, pyproject.toml, and any .py containing
    "if __name__ == '__main__'". Returns absolute paths as strings.
    """
    root = Path(root_path)
    entry_points: List[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            lower = fn.lower()
            full = os.path.join(dirpath, fn)
            if lower in ("setup.py", "pyproject.toml"):
                entry_points.append(os.path.abspath(full))
                continue
            if lower.endswith(".py"):
                try:
                    text = Path(full).read_text(encoding="utf-8")
                except Exception:
                    continue
                if "if __name__" in text:
                    entry_points.append(os.path.abspath(full))

    # deduplicate while preserving order
    seen = set()
    filtered: List[str] = []
    for p in entry_points:
        if p not in seen:
            seen.add(p)
            filtered.append(p)

    return filtered


def map_repo(local_path: str) -> Dict[str, Any]:
    """High-level mapping of a local repo into a small metadata structure.

    Returns keys: file_tree, readme_summary, entry_points
    """
    file_tree = build_file_tree(local_path)
    readme = find_readme(local_path)
    readme_summary = summarize_readme(readme or "")
    entry_points = find_entry_points(local_path)

    return {
        "file_tree": file_tree,
        "readme_summary": readme_summary,
        "entry_points": entry_points,
    }


if __name__ == "__main__":
    import json
    import sys

    root = sys.argv[1] if len(sys.argv) > 1 else "."
    print(json.dumps(map_repo(root), indent=2))
