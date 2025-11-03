# Agentic Codebase Genius

This repository implements a multi-agent system to generate high-quality Markdown documentation for a public GitHub repository. The system components: Supervisor (CodeGenius), Repo Mapper, Code Analyzer, and DocGenie. The implementation uses Jac nodes + Python helper modules.

## What is included

- `jac/` — Jac nodes and walkers (supervisor, repo_mapper, code_analyzer, docgenie, utils)
- `py_modules/` — Python helper modules used by Jac `py_module` calls
  - `git_utils.py` — clone a GitHub repo
  - `repo_mapper.py` — build file tree, README summary, detect entry points
  - `parser_utils.py` — parse Python/Jac files to extract symbols
  - `ccg.py` — build Code Context Graph (NetworkX)
  - `diagram.py` — generate call/class diagrams
  - `doc_template.py` — Jinja2 templates for docs
  - `docgenie.py` — assemble final `docs.md` and call diagrams + LLM rewriting
- `streamlit_app/` — lightweight demo UI to run quick repo mapping
- `tests/` — unit tests for key modules
- `integration_test.py` — quick script to run clone + map or generate docs

## Quick setup

1. Create and activate a Python venv (recommended):

```bash
python3 -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure LLM credentials in `.env` (OpenRouter recommended):

```
BYLLM_BACKEND=openrouter
BYLLM_BASE_URL=https://openrouter.ai/api/v1
BYLLM_API_KEY=sk-or-v1-your-openrouter-api-key-here
BYLLM_MODEL=openai/gpt-4o
```

## Run unit tests

```bash
source venv/bin/activate
python -m unittest discover -v
```

## Quick demo (Streamlit)

Start the Streamlit demo to try the Repo Mapper quickly:

```bash
source venv/bin/activate
streamlit run streamlit_app/app.py
```

Enter a public GitHub URL and press Analyze. This demo clones the repo and shows the README summary, entry points, and a small file tree.

## Generate full documentation (Python primary)

The core logic is implemented in Python for reliability. Run the integration script:

```bash
source venv/bin/activate
python run_sample.py
```

This clones a repo, maps it, builds CCG, generates docs, and saves to `outputs/<repo>/docs.md`.

## Jac Integration (Experimental)

Jac files in `jac/` are placeholders for future graph-based orchestration. Due to syntax limitations in Jac 0.8.10, walkers cannot directly call py_module or use 'report' as assumed. The Python helpers in `py_modules/` handle all functionality.

To run Jac (limited):

```bash
source venv/bin/activate
jac run jac/supervisor.jac  # Runs Python script via subprocess
```

Jac-cloud HTTP endpoints are not functional due to parsing errors.
