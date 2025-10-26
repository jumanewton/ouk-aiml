import shutil
from pathlib import Path
import byllm
import json

# Bring in the existing helpers
from git_utils import clone_repo
from repo_mapper import map_repo
from ccg import build_ccg
from parser_utils import parse_file
import docgenie as docgenie_mod

def plan_documentation_targets(repo_map: dict) -> dict:
    """
    Use LLM to plan which files to document first based on repo map.
    """
    readme_summary = repo_map.get("readme_summary", "")
    entry_points = repo_map.get("entry_points", [])
    file_tree = repo_map.get("file_tree", {})
    
    prompt = f"""Based on the repository summary and structure, prioritize the top 5-10 files that should be documented first for a comprehensive overview. Focus on entry points, main modules, and high-impact files.

README Summary: {readme_summary}

Entry Points: {', '.join(entry_points)}

File Tree (top-level): {json.dumps(file_tree, indent=2)[:1000]}

Return a JSON list of prioritized file paths (relative to repo root).
"""
    try:
        response = byllm.generate(prompt)
        # Assume response is a JSON list of file paths
        prioritized = json.loads(response)
        if isinstance(prioritized, list):
            return {"prioritized_files": prioritized}
    except Exception:
        # Fall through to fallback
        pass

    # Fallback to entry points (ensure list)
    return {"prioritized_files": entry_points}


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
        
        # High-level planning
        plan = plan_documentation_targets(repo_map)
        targets = plan.get("prioritized_files", repo_map.get("entry_points") or [])
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
