import shutil
from pathlib import Path

# Bring in the existing helpers
from git_utils import clone_repo
from repo_mapper import map_repo
from ccg import build_ccg
from parser_utils import parse_file
import docgenie as docgenie_mod

def generate_docs(repo_url: str, outputs_dir: str = "./outputs"):
    """High-level wrapper to run the full pipeline and return a result dict or docs path.

    This function is intended to be called from Jac via py_module.supervisor.generate_docs(repo_url).
    """
    clone_result = clone_repo(repo_url)
    if not clone_result.get("success"):
        return {"success": False, "error": clone_result.get("error")}

    local_path = clone_result.get("path")
    try:
        repo_map = map_repo(local_path)
        targets = repo_map.get("entry_points") or []
        if not targets:
            # Fallback: a small set of Python files
            targets = [str(p) for p in Path(local_path).rglob("*.py")][:10]

        ccg = build_ccg(targets)

        symbols = []
        for t in targets:
            parsed = parse_file(t)
            symbols.extend(parsed.get("symbols", []))

        docs_path = docgenie_mod.generate_docs(repo_url, repo_map, ccg, symbols, outputs_dir)
        return {"success": True, "docs_path": docs_path}
    finally:
        # best-effort cleanup
        try:
            shutil.rmtree(local_path)
        except Exception:
            pass
