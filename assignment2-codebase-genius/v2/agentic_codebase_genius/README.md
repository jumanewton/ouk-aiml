# Agentic Codebase Genius

An AI-powered multi-agent system that generates high-quality documentation for software repositories using both Python and Jac implementations.

## Overview

This system implements a multi-agent pipeline to automatically generate documentation for GitHub repositories. It consists of:

- **Repo Mapper**: Clones repositories and extracts file trees and README summaries.
- **Code Analyzer**: Parses Python code to build a Code Context Graph (CCG) showing relationships between functions, classes, and modules.
- **DocGenie**: Generates markdown documentation with diagrams from the collected data.
- **Supervisor**: Orchestrates the pipeline.

**Available Implementations:**
- **Python/Flask API**: Traditional web service approach
- **Jac Cloud API**: Modern agentic approach with automatic REST endpoints

## Setup

1. Ensure Python 3.8+ is installed.

2. Create and activate virtual environment:
   ```bash
   cd /path/to/assignment2-codebase-genius/v2/agentic_codebase_genius
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt install graphviz

   # macOS
   brew install graphviz

   # Windows: Download from https://graphviz.org/download/
   ```

5. Set environment variables (optional for LLM features):
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if needed
   ```

## Running the System

### Option 1: Streamlit Web UI (Easiest)

For users who prefer a graphical interface:

1. Start the Streamlit app:
   ```bash
   # From the project root directory
   streamlit run streamlit_app/app.py --server.headless true
   # Or use the launcher script:
   ./run_streamlit.sh
   ```
   Opens in browser at http://localhost:8501

   > **Note**: Use `--server.headless true` to prevent browser auto-opening issues on some systems.

2. Choose your API mode (Jac Cloud, Flask API, or Direct Python)
3. Enter a repository URL and click "Generate Documentation"

### Option 2: Jac Cloud API (Recommended)

Jac Cloud automatically converts walkers to REST endpoints with zero configuration.

1. Start the Jac server:
   ```bash
   jac serve jac/main.jac
   ```
   Server runs on http://127.0.0.1:8000

2. Generate documentation:
   ```bash
   curl -X POST http://127.0.0.1:8000/walker/generate_docs \
        -H "Content-Type: application/json" \
        -d '{"repo_url": "https://github.com/your-org/your-repo"}'
   ```

3. Health check:
   ```bash
   curl http://127.0.0.1:8000/walker/health_check
   ```

### Option 3: Python Flask API

Traditional web service implementation.

1. Start the Flask server:
   ```bash
   python main.py
   ```
   Server runs on http://127.0.0.1:8000

2. Generate documentation:
   ```bash
   curl -X POST http://127.0.0.1:8000/generate-docs \
        -H "Content-Type: application/json" \
        -d '{"repo_url": "https://github.com/your-org/your-repo"}'
   ```

### Option 4: Direct Python Execution

For development and testing:

```bash
python -c "
from py_module.supervisor import generate_docs
result = generate_docs('https://github.com/your-org/your-repo')
print('Result:', result)
"
```

## Outputs

Documentation is saved in `outputs/<repo-name>/docs.md` with:
- Repository overview and file tree
- Code Context Graph (CCG) visualization
- Function/class relationship diagrams
- Generated using Graphviz

## Testing

Run integration tests:
```bash
python tests/test_integration.py
```

## Architecture

### Core Components
- **Python Modules**: Handle heavy computation (cloning, parsing, graph building, markdown generation)
- **CCG**: NetworkX-based graph representing code relationships
- **Diagrams**: Generated using Graphviz for visual representation

### Implementation Options

#### Streamlit Web UI
- **User Interface**: Modern web app for non-technical users
- **API Integration**: Can connect to Jac Cloud, Flask, or direct Python
- **Interactive**: Real-time status updates and document preview
- **Download**: Direct download of generated documentation

#### Jac Cloud (Modern Agentic)
- **Walkers**: Define business logic as graph walkers
- **Automatic APIs**: Walkers become REST endpoints automatically
- **Type Safety**: Built-in parameter validation
- **Scalability**: Zero-config deployment to cloud

#### Python/Flask (Traditional)
- **Modules**: Pure Python implementation
- **Flask API**: Manual route definitions
- **Flexibility**: Full control over HTTP handling

## External Dependencies

### Python Packages
- GitPython: Repository cloning
- NetworkX: Graph data structures
- Graphviz (python): Diagram generation
- Pygments: Code highlighting
- Flask: Web framework
- Streamlit: Web UI framework
- Requests: HTTP client library
- Jac Cloud: Agentic framework
- Python-dotenv: Environment variable management

### System Dependencies
- Graphviz: System package for diagram rendering
- Git: Version control system

All dependencies are open-source with permissive licenses (MIT, BSD, Apache 2.0).

## API Reference

### Jac Cloud Endpoints

#### POST /walker/generate_docs
Generate documentation for a repository.

**Request:**
```json
{
  "repo_url": "https://github.com/owner/repo"
}
```

**Response:**
```json
{
  "status": "success",
  "docs_path": "outputs/repo/docs.md"
}
```

#### GET /walker/health_check
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "CodebaseGenius",
  "version": "1.0"
}
```

### Flask API Endpoints

#### POST /generate-docs
Same as Jac endpoint above.

## Troubleshooting

### Streamlit Issues

**Error: `ModuleNotFoundError: No module named 'distutils'`**
- **Cause**: Python 3.12 removed `distutils`, but older Streamlit versions still try to use it
- **Solution**: `setuptools` is included in `requirements.txt` and provides compatibility
- **Alternative**: Run with `--server.headless true` flag to prevent browser auto-opening

**Streamlit command not found**
- **Cause**: Virtual environment not activated or not installed
- **Solution**: Run `source ../../../venv/bin/activate && pip install -r requirements.txt`

### Graphviz Issues

**Error: `graphviz` module not found**
- **Cause**: Python package missing
- **Solution**: `pip install graphviz` (already in requirements.txt)

**Error: `dot` command not found**
- **Cause**: System Graphviz package missing
- **Solution**: Install system package:
  ```bash
  # Ubuntu/Debian
  sudo apt install graphviz

  # macOS
  brew install graphviz

  # Windows: Download from https://graphviz.org/download/
  ```

### Jac Cloud Issues

**Error: `jac` command not found**
- **Cause**: Jac Cloud not installed
- **Solution**: `pip install jac-cloud`

**HTTP endpoints not accessible**
- **Cause**: Server not started or wrong port
- **Solution**: Ensure `jac serve jac/main.jac` is running and check port 8000

## Limitations

- Currently optimized for Python repositories
- README summarization is heuristic-based (can be enhanced with LLMs)
- No support for private repositories without authentication
- Graphviz system package required for diagram generation

## Future Improvements

- Add support for more languages (JavaScript, Java, Go, etc.)
- Integrate LLM calls for enhanced summarization
- Add web UI for easier interaction
- Support incremental updates for large repos
- Implement authentication for private repos
- Add real-time progress tracking
- Support for multiple output formats (PDF, HTML)
