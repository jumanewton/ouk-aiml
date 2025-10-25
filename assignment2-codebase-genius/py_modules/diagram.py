import os
from pathlib import Path
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt

def generate_call_graph(ccg: 'CodeContextGraph', output_dir: str, repo_name: str):
    """
    Generate call graph diagram from CCG.
    """
    # Create subgraph of function nodes and call edges
    call_graph = nx.DiGraph()
    for u, v, data in ccg.graph.edges(data=True):
        if data.get('type') == 'calls':
            call_graph.add_edge(u, v)

    if call_graph.number_of_nodes() == 0:
        return None

    plt.figure(figsize=(12, 8))
    pos = graphviz_layout(call_graph, prog='dot')
    nx.draw(call_graph, pos, with_labels=True, node_color='lightblue', 
            node_size=2000, font_size=10, arrows=True)
    plt.title(f"Call Graph - {repo_name}")

    output_path = Path(output_dir) / "diagrams" / "call_graph.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return str(output_path)

def generate_class_diagram(ccg: 'CodeContextGraph', output_dir: str, repo_name: str):
    """
    Generate class inheritance diagram from CCG.
    """
    class_graph = nx.DiGraph()
    for u, v, data in ccg.graph.edges(data=True):
        if data.get('type') == 'inherits':
            class_graph.add_edge(u, v)

    if class_graph.number_of_nodes() == 0:
        return None

    plt.figure(figsize=(12, 8))
    pos = graphviz_layout(class_graph, prog='dot')
    nx.draw(class_graph, pos, with_labels=True, node_color='lightgreen', 
            node_size=2000, font_size=10, arrows=True)
    plt.title(f"Class Inheritance - {repo_name}")

    output_path = Path(output_dir) / "diagrams" / "class_diagram.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    return str(output_path)

def generate_diagrams(ccg: 'CodeContextGraph', output_dir: str, repo_name: str):
    """
    Generate all diagrams and return paths.
    """
    call_graph_path = generate_call_graph(ccg, output_dir, repo_name)
    class_diagram_path = generate_class_diagram(ccg, output_dir, repo_name)
    return {
        'call_graph': call_graph_path,
        'class_diagram': class_diagram_path
    }
