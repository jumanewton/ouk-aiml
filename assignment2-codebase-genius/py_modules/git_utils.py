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
        if not repo_url.startswith("https://github.com/"):
            return {"success": False, "path": None, "error": "Invalid GitHub URL format"}

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp(prefix="repo_clone_")

        # Clone the repository
        Repo.clone_from(repo_url, temp_dir)

        return {"success": True, "path": temp_dir, "error": None}

    except GitCommandError as e:
        return {"success": False, "path": None, "error": f"Git command error: {str(e)}"}
    except InvalidGitRepositoryError as e:
        return {"success": False, "path": None, "error": f"Invalid repository: {str(e)}"}
    except Exception as e:
        return {"success": False, "path": None, "error": f"Unexpected error: {str(e)}"}
