import pytest
import sys
import os
sys.path.append('../py_module')

from repo_mapper import map_repository
from code_analyzer import analyze_codebase
from docgenie import generate_docs

def test_full_pipeline():
    repo_url = "https://github.com/octocat/Hello-World"
    
    # Map
    result = map_repository(repo_url)
    assert 'repo_path' in result
    assert 'file_tree' in result
    assert 'readme_summary' in result
    
    # Analyze
    ccg = analyze_codebase(result['repo_path'])
    assert 'nodes' in ccg
    assert 'edges' in ccg
    
    # Generate
    docs_path = generate_docs(result['file_tree'], result['readme_summary'], ccg, repo_url)
    assert os.path.exists(docs_path)
    
    print(f"Docs generated: {docs_path}")

if __name__ == "__main__":
    test_full_pipeline()