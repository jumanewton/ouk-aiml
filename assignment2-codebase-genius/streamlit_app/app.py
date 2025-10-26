import streamlit as st
import requests
import json

st.title('Agentic Codebase Genius — Documentation Generator Demo')

repo_url = st.text_input('GitHub repository URL', 'https://github.com/octocat/Hello-World')

if st.button('Generate Docs'):
    with st.spinner('Generating documentation...'):
        try:
            response = requests.post(
                'http://localhost:8000/walker/generate_docs/1',
                headers={'Content-Type': 'application/json'},
                data=json.dumps({'repo_url': repo_url})
            )
            if response.status_code == 200:
                docs = response.json()
                st.success('Documentation generated')
                st.header('Generated Documentation')
                st.write(docs)
            else:
                st.error(f"Failed to generate docs: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.info('This demo uses the Jac Cloud API to generate full documentation. Make sure jac serve is running.')
