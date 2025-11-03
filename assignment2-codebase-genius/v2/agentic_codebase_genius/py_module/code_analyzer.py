import ast
import networkx as nx
from pathlib import Path
import os

class CodeAnalyzer:
    def __init__(self):
        self.graph = nx.DiGraph()

    def analyze_file(self, file_path: str):
        """Analyze a single Python file and add to graph."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            tree = ast.parse(source, filename=file_path)
            self._visit_tree(tree, file_path)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")

    def _visit_tree(self, node, file_path, parent=None):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            self.graph.add_node(class_name, type='class', file=file_path)
            if parent:
                self.graph.add_edge(parent, class_name, type='contains')
            for base in node.bases:
                if isinstance(base, ast.Name):
                    self.graph.add_edge(base.id, class_name, type='inherits')
            for item in node.body:
                self._visit_tree(item, file_path, class_name)
        elif isinstance(node, ast.FunctionDef):
            func_name = node.name
            self.graph.add_node(func_name, type='function', file=file_path)
            if parent:
                self.graph.add_edge(parent, func_name, type='contains')
            # Add calls
            for child in ast.walk(node):
                if isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
                    self.graph.add_edge(func_name, child.func.id, type='calls')
        elif isinstance(node, ast.Module):
            module_name = Path(file_path).stem
            self.graph.add_node(module_name, type='module', file=file_path)
            for item in node.body:
                self._visit_tree(item, file_path, module_name)

    def get_graph(self):
        """Return the graph as a dict for serialization."""
        return {
            'nodes': list(self.graph.nodes(data=True)),
            'edges': list(self.graph.edges(data=True))
        }

    def query_relationships(self, entity: str):
        """Query relationships for an entity (function/class)."""
        if entity not in self.graph:
            return {}
        predecessors = list(self.graph.predecessors(entity))
        successors = list(self.graph.successors(entity))
        return {
            'called_by': predecessors,
            'calls': successors,
            'inherits_from': [p for p in predecessors if self.graph.get_edge_data(p, entity, {}).get('type') == 'inherits'],
            'inherited_by': [s for s in successors if self.graph.get_edge_data(entity, s, {}).get('type') == 'inherits']
        }

def analyze_codebase(repo_path: str) -> dict:
    """Analyze all Python files in repo_path."""
    analyzer = CodeAnalyzer()
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'node_modules'}]
        for file in files:
            if file.endswith('.py'):
                analyzer.analyze_file(os.path.join(root, file))
    return analyzer.get_graph()

def query_ccg(graph_data: dict, entity: str) -> dict:
    """Query the CCG."""
    G = nx.DiGraph()
    G.add_nodes_from(graph_data['nodes'])
    G.add_edges_from([(e[0], e[1], e[2]) for e in graph_data['edges']])
    analyzer = CodeAnalyzer()
    analyzer.graph = G
    return analyzer.query_relationships(entity)
