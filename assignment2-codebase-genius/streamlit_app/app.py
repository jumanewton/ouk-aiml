import streamlit as st
import tempfile
import shutil
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from git_utils import clone_repo
from repo_mapper import map_repo

st.title('Agentic Codebase Genius — Repo Mapper Demo')

repo_url = st.text_input('GitHub repository URL', 'https://github.com/octocat/Hello-World')

if st.button('Analyze'):
    with st.spinner('Cloning repository...'):
        result = clone_repo(repo_url)
    if not result['success']:
        st.error(f"Clone failed: {result['error']}")
    else:
        local_path = result['path']
        try:
            with st.spinner('Mapping repository...'):
                repo_map = map_repo(local_path)
            st.success('Mapping complete')
            st.header('README Summary')
            st.write(repo_map.get('readme_summary'))
            st.header('Entry Points')
            for ep in repo_map.get('entry_points', []):
                st.write(ep)
            st.header('File Tree (top-level)')
            st.write(repo_map.get('file_tree'))
        finally:
            try:
                shutil.rmtree(local_path)
            except Exception:
                pass

st.info('This demo runs a quick clone and mapping locally; for full documentation generation run the Supervisor walker or integration_test.py')