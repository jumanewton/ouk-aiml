# Agentic Codebase Genius

An AI-powered multi-agent system that generates high-quality documentation for software repositories.

## Overview

This system implements a multi-agent pipeline to automatically generate documentation for GitHub repositories. It consists of:

- **Repo Mapper**: Clones repositories and extracts file trees and README summaries.
- **Code Analyzer**: Parses Python code to build a Code Context Graph (CCG) showing relationships between functions, classes, and modules.
- **DocGenie**: Generates markdown documentation with diagrams from the collected data.
- **Supervisor**: Orchestrates the pipeline via a Flask API.

## Setup

1. Ensure Python 3.8+ is installed.

2. Create and activate virtual environment:
   ```bash
   cd /path/to/assignment2-codebase-genius
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r v2/agentic_codebase_genius/requirements.txt
   ```

4. Set environment variables (optional for LLM features):
   ```bash
   cp v2/agentic_codebase_genius/.env.example v2/agentic_codebase_genius/.env
   # Edit .env with your API keys if needed
   ```

## Running the System

1. Navigate to the project directory:
   ```bash
   cd v2/agentic_codebase_genius
   ```

2. Start the API server:
   ```bash
   python main.py
   ```
   The server runs on http://127.0.0.1:8000

3. Generate documentation:
   ```bash
   curl -X POST http://127.0.0.1:8000/generate-docs \
        -H "Content-Type: application/json" \
        -d '{"repo_url": "https://github.com/your-org/your-repo"}'
   ```

4. Check outputs:
   Documentation is saved in `outputs/<repo-name>/docs.md` with diagrams.

## Testing

Run integration tests:
```bash
python tests/test_integration.py
```

## Architecture

- **Python Modules**: Handle heavy computation (cloning, parsing, graph building, markdown generation).
- **Flask API**: Provides HTTP interface for triggering documentation generation.
- **CCG**: NetworkX-based graph representing code relationships.
- **Diagrams**: Generated using Graphviz for visual representation of code structure.

## External Dependencies

- GitPython: Repository cloning
- NetworkX: Graph data structures
- Graphviz: Diagram generation (requires system package)
- Pygments: Code highlighting
- Flask: Web framework
- Python-dotenv: Environment variable management

All dependencies are open-source with permissive licenses (MIT, BSD).

## Limitations

- Currently optimized for Python repositories
- Jac integration attempted but Python implementation used due to syntax issues
- README summarization is heuristic-based (can be enhanced with LLMs)
- No support for private repositories

## Future Improvements

- Add support for more languages (JavaScript, Java, etc.)
- Integrate LLM calls for better summarization
- Implement Jac walkers fully
- Add web UI for easier interaction
- Support incremental updates for large repos
