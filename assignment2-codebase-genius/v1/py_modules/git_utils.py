import tempfile
import os
from git import Repo, GitCommandError, InvalidGitRepositoryError

def clone_repo(repo_url: str) -> dict:
    """
    Clone a GitHub repository to a temporary directory.

    Args:
        repo_url (str): The GitHub repository URL to clone.

    Returns:
        dict: {"success": bool, "path": str or None, "error": str or None}
    """
    try:
        # Validate URL format (basic check)
        if not (repo_url.startswith("https://github.com/") or repo_url.startswith("http://github.com/")):
            return {"success": False, "path": None, "error": "Invalid GitHub URL format. Only https://github.com/ URLs are supported."}

        # Basic URL validation
        parts = repo_url.replace("https://github.com/", "").replace("http://github.com/", "").split("/")
        if len(parts) < 2:
            return {"success": False, "path": None, "error": "Invalid GitHub URL format. Expected format: https://github.com/owner/repo"}

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp(prefix="repo_clone_")

        # Clone the repository (shallow clone for speed)
        Repo.clone_from(repo_url, temp_dir, depth=1)

        return {"success": True, "path": temp_dir, "error": None}

    except GitCommandError as e:
        error_msg = str(e)
        if "Repository not found" in error_msg or "does not exist" in error_msg:
            return {"success": False, "path": None, "error": "Repository not found or access denied. Please check the URL and ensure the repository is public."}
        elif "Authentication failed" in error_msg:
            return {"success": False, "path": None, "error": "Authentication failed. Private repositories are not supported."}
        else:
            return {"success": False, "path": None, "error": f"Git operation failed: {error_msg}"}
    except InvalidGitRepositoryError as e:
        return {"success": False, "path": None, "error": f"Invalid repository: {str(e)}"}
    except Exception as e:
        return {"success": False, "path": None, "error": f"Unexpected error during cloning: {str(e)}"}
