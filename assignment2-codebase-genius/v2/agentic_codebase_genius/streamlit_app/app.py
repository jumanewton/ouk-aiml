import streamlit as st
import requests
import sys
import os
from typing import Optional

# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

st.title('🤖 Agentic Codebase Genius')
st.markdown('### AI-Powered Documentation Generator')

# Sidebar configuration
st.sidebar.header('⚙️ Configuration')
api_mode = st.sidebar.selectbox(
    'API Mode',
    ['Jac Cloud (Recommended)', 'Flask API', 'Direct Python'],
    help='Choose how to generate documentation'
)

# API endpoints based on mode
if api_mode == 'Jac Cloud (Recommended)':
    base_url = 'http://localhost:8000'
    generate_endpoint = f'{base_url}/walker/generate_docs'
    health_endpoint = f'{base_url}/walker/health_check'
    server_command = 'jac serve jac/main.jac'
elif api_mode == 'Flask API':
    base_url = 'http://localhost:8000'
    generate_endpoint = f'{base_url}/generate-docs'
    health_endpoint = None  # Flask doesn't have health check
    server_command = 'python main.py'
else:  # Direct Python
    base_url = None
    generate_endpoint = None
    health_endpoint = None
    server_command = None

# Main interface
st.markdown('---')

repo_url = st.text_input(
    'GitHub Repository URL',
    placeholder='https://github.com/owner/repo',
    help='Enter a public GitHub repository URL'
)

col1, col2 = st.columns([1, 1])

with col1:
    generate_button = st.button('🚀 Generate Documentation', type='primary', use_container_width=True)

with col2:
    if api_mode != 'Direct Python':
        health_button = st.button('🔍 Check API Health', use_container_width=True)
    else:
        health_button = False

# Status indicators
status_container = st.container()

if api_mode != 'Direct Python':
    with status_container:
        st.markdown('### 📊 API Status')
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button('▶️ Start Server', help=f'Run: {server_command}'):
                st.info(f'Start the server with: `{server_command}`')
                st.code(server_command)

        with col2:
            if health_button:
                try:
                    if health_endpoint:
                        response = requests.get(health_endpoint, timeout=5)
                        if response.status_code == 200:
                            data = response.json()
                            # Handle Jac Cloud health response format
                            if api_mode == 'Jac Cloud (Recommended)' and 'reports' in data:
                                if len(data['reports']) > 0:
                                    health_data = data['reports'][0]
                                    st.success(f"✅ {health_data.get('status', 'OK')}")
                                else:
                                    st.warning("⚠️ No health data")
                            else:
                                # Flask or direct response
                                st.success(f"✅ {data.get('status', 'OK')}")
                        else:
                            st.error(f"❌ HTTP {response.status_code}")
                    else:
                        st.warning("⚠️ No health endpoint")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Connection failed: {str(e)}")

        with col3:
            st.info(f"🌐 {base_url}")

if generate_button:
    if not repo_url:
        st.error('Please enter a repository URL')
    else:
        with st.spinner('Generating documentation...'):
            try:
                if api_mode == 'Direct Python':
                    # Import and use directly
                    from py_module.supervisor import generate_docs
                    result = generate_docs(repo_url)
                else:
                    # Use HTTP API
                    response = requests.post(
                        generate_endpoint,
                        json={'repo_url': repo_url},
                        timeout=300  # 5 minutes timeout
                    )

                    if response.status_code == 200:
                        raw_result = response.json()

                        # Handle different API response formats
                        if api_mode == 'Jac Cloud (Recommended)':
                            # Jac Cloud wraps responses in a reports array
                            if 'reports' in raw_result and len(raw_result['reports']) > 0:
                                result = raw_result['reports'][0]  # Take first report
                            else:
                                result = {'status': 'error', 'error': 'No reports in Jac Cloud response'}
                        else:
                            # Flask API returns direct result
                            result = raw_result
                    else:
                        result = {
                            'status': 'error',
                            'error': f'HTTP {response.status_code}: {response.text}'
                        }

                # Display results
                if result.get('status') == 'success':
                    st.success('✅ Documentation generated successfully!')

                    # Show docs path
                    if 'docs_path' in result:
                        st.info(f"📁 Saved to: `{result['docs_path']}`")

                        # Try to read and display the generated docs
                        try:
                            with open(result['docs_path'], 'r') as f:
                                docs_content = f.read()

                            st.markdown('### 📄 Generated Documentation')
                            st.markdown(docs_content)

                            # Download button
                            st.download_button(
                                label="📥 Download Documentation",
                                data=docs_content,
                                file_name=f"{os.path.basename(repo_url)}.md",
                                mime="text/markdown"
                            )

                        except FileNotFoundError:
                            st.warning("Documentation file not found locally")
                        except Exception as e:
                            st.error(f"Error reading docs: {str(e)}")

                else:
                    st.error(f"❌ Failed to generate docs: {result.get('error', 'Unknown error')}")
                    st.json(result)  # Show full error details

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Network error: {str(e)}")
                st.info("Make sure the API server is running")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
                st.code(str(e))

# Footer
st.markdown('---')
st.markdown('### 📚 About')
st.markdown(f'''
**API Mode:** {api_mode}

- **Jac Cloud**: Modern agentic approach with automatic REST endpoints
- **Flask API**: Traditional web service implementation
- **Direct Python**: Local execution without server

**Features:**
- 📊 Code Context Graph (CCG) generation
- 🎨 Interactive diagrams with Graphviz
- 📝 Comprehensive markdown documentation
- 🔍 Repository structure analysis
''')

if api_mode != 'Direct Python':
    st.markdown(f'''
**Server Command:** `{server_command}`
**API Endpoint:** {generate_endpoint}
''')

st.markdown('**Dependencies:** GitPython, NetworkX, Graphviz, Pygments, Flask, Streamlit, Requests, Jac Cloud')