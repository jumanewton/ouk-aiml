#!/usr/bin/env python3
import sys
sys.path.append('py_module')

from repo_mapper import map_repository
from code_analyzer import analyze_codebase
from docgenie import generate_docs

# Test with a small public repo
repo_url = "https://github.com/octocat/Hello-World"
result = map_repository(repo_url)
print("Repo Path:", result['repo_path'])
print("File Tree:", result['file_tree'])
print("README Summary:", result['readme_summary'])

# Analyze code
ccg = analyze_codebase(result['repo_path'])
print("CCG Nodes:", len(ccg['nodes']))
print("CCG Edges:", len(ccg['edges']))

# Generate docs
docs_path = generate_docs(result['file_tree'], result['readme_summary'], ccg, repo_url)
print("Docs generated at:", docs_path)