from jinja2 import Template

# Template for the full README
FULL_TEMPLATE = Template("""
# {{ repo_name }}

## Overview

{{ overview }}

## Installation

{{ installation }}

## Quickstart / Usage

{{ usage }}

## API Reference

{{ api_reference }}

## Architecture

{{ architecture }}

## Contributing

{{ contributing }}
""")

# Section templates
OVERVIEW_TEMPLATE = Template("""
{{ readme_summary }}

### Key Features
{% for feature in features %}
- {{ feature }}
{% endfor %}
""")

INSTALLATION_TEMPLATE = Template("""
### Prerequisites
- Python 3.8+

### Install from source
```bash
git clone {{ repo_url }}
cd {{ repo_name }}
pip install -r requirements.txt
```

{% if setup_py %}
### Or install package
```bash
pip install .
```
{% endif %}
""")

USAGE_TEMPLATE = Template("""
### Basic Usage

{% for example in examples %}
#### {{ example.title }}
```python
{{ example.code }}
```
{% endfor %}
""")

API_REFERENCE_TEMPLATE = Template("""
{% for module, symbols in api.items() %}
### {{ module }}

{% for symbol in symbols %}
#### `{{ symbol.signature }}`
{{ symbol.docstring }}

{% endfor %}
{% endfor %}
""")

ARCHITECTURE_TEMPLATE = Template("""
### System Architecture

![Call Graph](diagrams/call_graph.png)

### Class Hierarchy

![Class Diagram](diagrams/class_diagram.png)

{{ explanation }}
""")

CONTRIBUTING_TEMPLATE = Template("""
### Development Setup
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `python -m pytest`
5. Submit a pull request
""")

def render_overview(readme_summary, features=None):
    if features is None:
        features = []
    return OVERVIEW_TEMPLATE.render(readme_summary=readme_summary, features=features)

def render_installation(repo_url, repo_name, has_setup_py=False):
    return INSTALLATION_TEMPLATE.render(repo_url=repo_url, repo_name=repo_name, setup_py=has_setup_py)

def render_usage(examples):
    return USAGE_TEMPLATE.render(examples=examples)

def render_api_reference(api_data):
    return API_REFERENCE_TEMPLATE.render(api=api_data)

def render_architecture(explanation=""):
    return ARCHITECTURE_TEMPLATE.render(explanation=explanation)

def render_contributing():
    return CONTRIBUTING_TEMPLATE.render()

def assemble_docs(repo_name, repo_url, overview, installation, usage, api_reference, architecture, contributing):
    return FULL_TEMPLATE.render(
        repo_name=repo_name,
        overview=overview,
        installation=installation,
        usage=usage,
        api_reference=api_reference,
        architecture=architecture,
        contributing=contributing
    )
