from .repo_mapper import map_repository
from .code_analyzer import analyze_codebase
from .docgenie import generate_docs as generate_docs_internal


def generate_docs(repo_url: str):
    """Orchestrate the pipeline in Python and return a simple result dict."""
    result = map_repository(repo_url)
    repo_path = result['repo_path']
    file_tree = result['file_tree']
    readme_summary = result['readme_summary']

    ccg = analyze_codebase(repo_path)

    docs_path = generate_docs_internal(file_tree, readme_summary, ccg, repo_url)

    return {
        'status': 'success',
        'docs_path': docs_path
    }
