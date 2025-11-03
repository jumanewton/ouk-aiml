import shutil
from pathlib import Path

# Bring in the existing helpers
from .git_utils import clone_repo
from .repo_mapper import map_repo
from .ccg import build_ccg
from .parser_utils import parse_file
from . import docgenie as docgenie_mod

def generate_docs(repo_url: str, outputs_dir: str = "./outputs"):
    """High-level wrapper to run the full pipeline and return a result dict or docs path.

    This function is intended to be called from Jac via py_module.supervisor.generate_docs(repo_url).
    """
    # Validate input
    if not repo_url or not isinstance(repo_url, str):
        return {"success": False, "error": "Invalid repository URL provided"}

    # Check if it's a GitHub URL
    if not (repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/")):
        return {"success": False, "error": "Only GitHub repository URLs are supported"}

    clone_result = clone_repo(repo_url)
    if not clone_result.get("success"):
        return {"success": False, "error": f"Failed to clone repository: {clone_result.get('error')}"}

    local_path = clone_result.get("path")
    try:
        repo_map = map_repo(local_path)
        if not repo_map.get('readme_summary') and not repo_map.get('entry_points'):
            return {"success": False, "error": "Repository appears to be empty or inaccessible"}

        targets = repo_map.get("entry_points") or []
        if not targets:
            # Fallback: a small set of Python/Jac files
            all_files = list(Path(local_path).rglob("*.py")) + list(Path(local_path).rglob("*.jac"))
            targets = [str(p) for p in all_files[:10]]

        if not targets:
            # Gather some diagnostics to help the UI and logs explain why there
            # were no supported source files. Return a small sample of scanned
            # files and a compact repo_map summary so callers can show useful
            # feedback to users instead of a terse message.
            scanned_files = [str(p) for p in Path(local_path).rglob("*") if p.is_file()]
            scanned_sample = scanned_files[:50]
            repo_map_summary = {
                "readme_summary_present": bool(repo_map.get("readme_summary")),
                "entry_points_count": len(repo_map.get("entry_points") or []),
            }

            return {
                "success": False,
                "error": "No supported source files found in repository",
                "scanned_files_count": len(scanned_files),
                "scanned_files_sample": scanned_sample,
                "repo_map_summary": repo_map_summary,
            }

        ccg = build_ccg(targets)

        symbols = []
        for t in targets:
            try:
                parsed = parse_file(t)
                symbols.extend(parsed.get("symbols", []))
            except Exception as e:
                # Continue with other files if one fails
                continue

        if not symbols:
            return {"success": False, "error": "Failed to parse any source files"}

        docs_path = docgenie_mod.generate_docs(repo_url, repo_map, ccg, symbols, targets, outputs_dir)
        return {"success": True, "docs_path": docs_path}
    except Exception as e:
        return {"success": False, "error": f"Documentation generation failed: {str(e)}"}
    finally:
        # best-effort cleanup
        try:
            shutil.rmtree(local_path)
        except Exception:
            pass
