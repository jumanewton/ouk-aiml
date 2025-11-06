import streamlit as st
import requests
import sys
import os
import json
import traceback
import logging
from datetime import datetime
from typing import Optional

# Add current directory to path for local imports
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Logging / diagnostics
LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'last_error.log')
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s'
)

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
        st.markdown('### API Status')
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
            result = None
            exc_info = None
            try:
                # Call into the chosen API/mode
                if api_mode == 'Direct Python':
                    from py_module.supervisor import generate_docs
                    result = generate_docs(repo_url)
                else:
                    response = requests.post(
                        generate_endpoint,
                        json={'repo_url': repo_url},
                        timeout=300,
                    )

                    # Try to parse JSON safely
                    try:
                        raw_result = response.json()
                    except Exception:
                        raw_result = {'status': 'error', 'error': f'Invalid JSON response (HTTP {response.status_code})', 'raw_text': response.text}

                    if response.status_code == 200:
                        # Normalize Jac Cloud vs Flask formats
                        if api_mode == 'Jac Cloud (Recommended)':
                            if isinstance(raw_result, dict) and 'reports' in raw_result and len(raw_result['reports']) > 0:
                                result = raw_result['reports'][0]
                            else:
                                result = {'status': 'error', 'error': 'No reports in Jac Cloud response', 'raw': raw_result}
                        else:
                            result = raw_result
                    else:
                        result = {'status': 'error', 'error': f'HTTP {response.status_code}: {response.text}'}

                # Ensure we have a dict result
                if not isinstance(result, dict):
                    result = {'status': 'error', 'error': 'Unexpected response type', 'raw': str(result)}

                # Success path
                if str(result.get('status')).lower() == 'success' or result.get('status') is True:
                    st.success('✅ Documentation generated successfully!')

                    docs_path = result.get('docs_path')
                    if docs_path:
                        st.info(f"📁 Saved to: `{docs_path}`")
                        try:
                            with open(docs_path, 'r') as f:
                                docs_content = f.read()
                            st.markdown('### 📄 Generated Documentation')
                            st.markdown(docs_content)
                            st.download_button(
                                label="📥 Download Documentation",
                                data=docs_content,
                                file_name=f"{os.path.basename(repo_url)}.md",
                                mime="text/markdown",
                            )
                        except FileNotFoundError:
                            st.warning("Documentation file not found locally")
                        except Exception as e:
                            # Minor read error: show brief message and log full trace
                            short_msg = str(e)
                            st.error(f"❌ Error reading docs: {short_msg}")
                            trace = traceback.format_exc()
                            logging.exception('Error reading docs')
                            with st.expander('Details (click to expand)'):
                                st.code(trace)
                    else:
                        st.warning('No docs_path returned by the service')

                else:
                    # User-facing short message
                    user_msg = result.get('error') or result.get('message') or str(result.get('status')) or 'Unknown error'
                    short_user_msg = user_msg if len(user_msg) <= 200 else user_msg[:200] + '...'
                    st.error(f"❌ Failed to generate docs: {short_user_msg}")

                    # Log full details with timestamp
                    timestamp = datetime.utcnow().isoformat()
                    try:
                        logging.error('Generation failed: %s | result=%s', repo_url, json.dumps(result, default=str))
                    except Exception:
                        logging.exception('Failed to log result for repo: %s', repo_url)

                    # Provide expandable full details for debugging (collapsed by default)
                    with st.expander('Details (click to expand)'):
                        # Show the full result JSON safely
                        try:
                            st.json(result)
                        except Exception:
                            st.text(str(result))

            except requests.exceptions.RequestException as e:
                # Network-specific friendly message
                short_msg = str(e)
                st.error(f"❌ Network error: {short_msg}")
                logging.exception('Network error while generating docs')
                with st.expander('Details (click to expand)'):
                    st.code(traceback.format_exc())
            except Exception as e:
                # Unexpected exception: show short message, log full traceback
                short_msg = str(e)
                st.error(f"❌ Unexpected error: {short_msg}")
                logging.exception('Unexpected error in Streamlit app')
                with st.expander('Details (click to expand)'):
                    st.code(traceback.format_exc())

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