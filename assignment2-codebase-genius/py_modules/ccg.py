import networkx as nx
import json
from typing import List, Dict, Any
from pathlib import Path

class CodeContextGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_symbols(self, symbols: List[Dict]):
        for sym in symbols:
            node_id = f"{sym['module']}::{sym['name']}"
            self.graph.add_node(node_id, **sym)

    def add_calls(self, calls: List[Dict]):
        for call in calls:
            if call['caller']:
                caller_id = f"{call['module']}::{call['caller']}"
                callee_id = f"{call['module']}::{call['callee']}"  # assume same module for now
                if callee_id in self.graph:
                    self.graph.add_edge(caller_id, callee_id, type='calls')

    def add_inherits(self, symbols: List[Dict]):
        for sym in symbols:
            if sym['kind'] == 'class' and 'bases' in sym:
                child_id = f"{sym['module']}::{sym['name']}"
                for base in sym['bases']:
                    # Heuristic: if base is simple name, assume same module
                    base_id = f"{sym['module']}::{base}"
                    if base_id in self.graph:
                        self.graph.add_edge(child_id, base_id, type='inherits')

    def add_imports(self, imports: List[Dict]):
        for imp in imports:
            module_id = f"{imp['module']}"
            imported_id = imp['name']
            self.graph.add_edge(module_id, imported_id, type='imports')

    def build_from_parsed(self, parsed_files: List[Dict]):
        for parsed in parsed_files:
            self.add_symbols(parsed['symbols'])
            self.add_calls(parsed['calls'])
            self.add_inherits(parsed['symbols'])
            self.add_imports(parsed['imports'])

    def to_json(self) -> str:
        data = {
            'nodes': [{'id': n, **self.graph.nodes[n]} for n in self.graph.nodes],
            'edges': [{'source': u, 'target': v, **self.graph.edges[u, v]} for u, v in self.graph.edges]
        }
        return json.dumps(data, indent=2)

    def query_functions_calling(self, func_name: str) -> List[str]:
        callers = []
        for u, v, data in self.graph.in_edges(func_name, data=True):
            if data.get('type') == 'calls':
                callers.append(u)
        return callers

    def get_high_impact_functions(self) -> List[str]:
        # Simple: high in-degree (many callers)
        degrees = dict(self.graph.in_degree())
        sorted_funcs = sorted(degrees.items(), key=lambda x: x[1], reverse=True)
        return [f for f, d in sorted_funcs if d > 0][:10]  # top 10

def build_ccg(target_files: List[str]) -> CodeContextGraph:
    from parser_utils import parse_file  # import here to avoid circular

    ccg = CodeContextGraph()
    parsed_files = []
    for file_path in target_files:
        if Path(file_path).exists():
            parsed = parse_file(file_path)
            parsed_files.append(parsed)
    ccg.build_from_parsed(parsed_files)
    return ccg

def summarize_module(module_path: str, symbols: List[Dict], code_snippet: str = "") -> str:
    """
    Summarize a module using a simple fallback.
    LLM summarization is now handled in Jac.
    """
    return f"# {module_path}\n\nModule summary not available (LLM required for detailed summary).\n\nSymbols: {len(symbols)} found."
