import streamlit as st
import sys
import os

# Add parent directory to path to import py_modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from py_modules.supervisor import generate_docs

st.title('Agentic Codebase Genius — Documentation Generator Demo')

repo_url = st.text_input('GitHub repository URL', 'https://github.com/octocat/Hello-World')

if st.button('Generate Docs'):
    with st.spinner('Generating documentation...'):
        try:
            result = generate_docs(repo_url)
            if result.get("success"):
                st.success('Documentation generated')
                st.header('Generated Documentation')
                # Assuming result has docs_path, read and display
                if "docs_path" in result:
                    with open(result["docs_path"], 'r') as f:
                        docs_content = f.read()
                    st.write(docs_content)
                else:
                    st.write(result)
            else:
                # Show error and full diagnostics returned by supervisor for
                # faster debugging in the UI (scanned files sample, repo_map
                # summary, etc.). This helps users understand why their repo
                # didn't produce supported source files.
                st.error(f"Failed to generate docs: {result.get('error')}")
                st.write(result)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.info('This demo uses the Python API directly to generate full documentation.')
