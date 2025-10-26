import os
from pathlib import Path
from typing import Dict, Any, List
from doc_template import (
    render_overview, render_installation, render_usage, 
    render_api_reference, render_architecture, render_contributing,
    assemble_docs
)
from diagram import generate_diagrams
from ccg import CodeContextGraph, summarize_module

def rewrite_section_with_llm(section_name: str, content: str) -> str:
    """
    Rewrite a section using a simple fallback.
    LLM rewriting is now handled in Jac.
    """
    return content

def generate_usage_examples(ccg: 'CodeContextGraph', symbols: List[Dict]) -> List[Dict]:
    """
    Generate usage examples from high-impact functions.
    """
    high_impact = ccg.get_high_impact_functions()
    examples = []
    for func in high_impact[:3]:  # limit to 3
        # Find the symbol
        symbol = next((s for s in symbols if f"{s['module']}::{s['name']}" == func), None)
        if symbol and symbol['kind'] == 'function':
            # Simple example generation
            sig = symbol['signature']
            if 'def ' in sig:
                func_name = symbol['name']
                example_code = f"from {symbol['module'].replace('.py', '')} import {func_name}\n\n# Example usage\nresult = {func_name}()"
                examples.append({
                    'title': f"Using {func_name}",
                    'code': example_code
                })
    return examples

def detect_installation_info(file_tree: Dict) -> Dict:
    """
    Detect installation info from file tree.
    """
    has_setup_py = 'setup.py' in file_tree
    has_requirements = 'requirements.txt' in file_tree
    has_pyproject = 'pyproject.toml' in file_tree
    return {
        'has_setup_py': has_setup_py,
        'has_requirements': has_requirements,
        'has_pyproject': has_pyproject
    }

def assemble_api_reference(symbols: List[Dict], targets: List[str]) -> Dict[str, str]:
    """
    Group symbols by module and generate LLM summaries for each module.
    """
    api = {}
    for sym in symbols:
        module = sym['module']
        if module not in api:
            api[module] = []
        api[module].append(sym)
    
    # Generate summaries
    summaries = {}
    for module, syms in api.items():
        # Find a target file that matches the module
        code_snippet = ""
        for target in targets:
            if module in target:
                try:
                    with open(target, 'r', encoding='utf-8') as f:
                        code_snippet = f.read()[:1000]  # First 1000 chars
                    break
                except:
                    pass
        summary = summarize_module(module, syms, code_snippet)
        summaries[module] = summary
    
    return summaries

def generate_docs(repo_url: str, repo_map: Dict, ccg: 'CodeContextGraph', symbols: List[Dict], targets: List[str], output_dir: str) -> str:
    """
    Generate the full documentation.
    """
    repo_name = repo_url.split('/')[-1]
    output_path = Path(output_dir) / repo_name / "docs.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate diagrams
    diagrams = generate_diagrams(ccg, str(output_path.parent), repo_name)

    # Detect installation
    install_info = detect_installation_info(repo_map['file_tree'])

    # Sections
    overview = render_overview(repo_map['readme_summary'])
    overview = rewrite_section_with_llm("Overview", overview)

    installation = render_installation(repo_url, repo_name, install_info['has_setup_py'])

    examples = generate_usage_examples(ccg, symbols)
    usage = render_usage(examples)
    usage = rewrite_section_with_llm("Usage", usage)

    api_data = assemble_api_reference(symbols, targets)
    api_reference = render_api_reference(api_data)
    api_reference = rewrite_section_with_llm("API Reference", api_reference)

    architecture = render_architecture("This diagram shows the relationships between functions and classes in the codebase.")
    architecture = rewrite_section_with_llm("Architecture", architecture)

    contributing = render_contributing()

    # Assemble
    full_docs = assemble_docs(
        repo_name, repo_url, overview, installation, usage, 
        api_reference, architecture, contributing
    )

    # Save
    with open(output_path, 'w') as f:
        f.write(full_docs)

    return str(output_path)