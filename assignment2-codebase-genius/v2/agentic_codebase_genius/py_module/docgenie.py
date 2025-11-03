import os
from pathlib import Path
import graphviz
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

def generate_diagram(ccg: dict, output_path: str):
    """Generate a Graphviz diagram from CCG."""
    dot = graphviz.Digraph(comment='Code Context Graph')
    for node, data in ccg['nodes']:
        shape = 'box' if data.get('type') == 'class' else 'ellipse'
        dot.node(node, shape=shape)
    for edge in ccg['edges']:
        dot.edge(edge[0], edge[1], label=edge[2].get('type', ''))
    dot.render(output_path, format='png', cleanup=True)

def generate_markdown(file_tree: dict, readme_summary: str, ccg: dict, repo_name: str, output_dir: str):
    """Generate markdown documentation."""
    md = f"# {repo_name} Documentation\n\n"
    md += f"## Overview\n\n{readme_summary}\n\n"

    # File Tree
    md += "## Project Structure\n\n"
    def render_tree(tree, indent=0):
        prefix = "  " * indent
        if tree['type'] == 'directory':
            result = f"{prefix}- **{tree['name']}/**\n"
            for child in tree.get('children', []):
                result += render_tree(child, indent + 1)
            return result
        else:
            return f"{prefix}- {tree['name']}\n"
    md += render_tree(file_tree) + "\n"

    # API Reference from CCG
    md += "## API Reference\n\n"
    classes = [n for n, d in ccg['nodes'] if d.get('type') == 'class']
    functions = [n for n, d in ccg['nodes'] if d.get('type') == 'function']
    if classes:
        md += "### Classes\n\n"
        for cls in classes:
            md += f"- **{cls}**\n"
    if functions:
        md += "### Functions\n\n"
        for func in functions:
            md += f"- **{func}**\n"

    # Diagram
    md += "## Code Relationships\n\n![Code Context Graph](diagram.png)\n\n"

    return md

def generate_docs(file_tree: dict, readme_summary: str, ccg: dict, repo_url: str, output_base: str = 'outputs'):
    """Main function to generate docs."""
    repo_name = repo_url.split('/')[-1]
    output_dir = Path(output_base) / repo_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate diagram
    diagram_path = output_dir / 'diagram'
    generate_diagram(ccg, str(diagram_path))

    # Generate markdown
    md_content = generate_markdown(file_tree, readme_summary, ccg, repo_name, str(output_dir))
    docs_path = output_dir / 'docs.md'
    with open(docs_path, 'w') as f:
        f.write(md_content)

    return str(docs_path)
