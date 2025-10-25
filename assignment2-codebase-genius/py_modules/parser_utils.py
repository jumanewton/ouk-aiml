import ast
import re
from pathlib import Path
from typing import List, Dict, Any

def parse_python_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a Python file using AST to extract symbols: functions, classes, methods, imports, calls.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        return {'symbols': [], 'imports': [], 'calls': []}

    symbols = []
    imports = []
    calls = []

    def extract_signature(func_node):
        args = []
        for arg in func_node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {ast.unparse(arg.annotation)}"
            args.append(arg_str)
        if func_node.args.vararg:
            args.append(f"*{func_node.args.vararg.arg}")
        if func_node.args.kwarg:
            args.append(f"**{func_node.args.kwarg.arg}")
        defaults = [None] * (len(func_node.args.args) - len(func_node.args.defaults)) + func_node.args.defaults
        for i, default in enumerate(defaults):
            if default:
                args[i] += f"={ast.unparse(default)}"
        return f"({', '.join(args)})"

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            symbols.append({
                'name': node.name,
                'kind': 'function',
                'signature': f"def {node.name}{extract_signature(node)}",
                'docstring': ast.get_docstring(node) or '',
                'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),  # relative path
                'line': node.lineno
            })
        elif isinstance(node, ast.ClassDef):
            bases = [ast.unparse(base) for base in node.bases]
            symbols.append({
                'name': node.name,
                'kind': 'class',
                'signature': f"class {node.name}({', '.join(bases)})",
                'docstring': ast.get_docstring(node) or '',
                'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),
                'line': node.lineno
            })
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append({
                    'name': alias.name,
                    'as': alias.asname,
                    'module': str(Path(file_path).relative_to(Path(file_path).parent.parent))
                })
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            for alias in node.names:
                imports.append({
                    'name': f"{module}.{alias.name}",
                    'as': alias.asname,
                    'module': str(Path(file_path).relative_to(Path(file_path).parent.parent))
                })
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                calls.append({
                    'caller': None,  # will be set based on context
                    'callee': node.func.id,
                    'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),
                    'line': node.lineno
                })

    # Associate calls with containing functions
    symbols.sort(key=lambda x: x['line'])
    for call in calls:
        for sym in reversed(symbols):
            if sym['line'] <= call['line']:
                call['caller'] = sym['name']
                break

    return {'symbols': symbols, 'imports': imports, 'calls': calls}

def parse_jac_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a Jac file using regex heuristics to extract symbols.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
    except:
        return {'symbols': [], 'imports': [], 'calls': []}

    symbols = []
    imports = []
    calls = []

    # Regex for function defs
    func_pattern = r'def\s+(\w+)\s*\(([^)]*)\)\s*:\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|)'
    for match in re.finditer(func_pattern, source, re.DOTALL):
        name = match.group(1)
        args = match.group(2)
        doc = match.group(3) or match.group(4) or ''
        symbols.append({
            'name': name,
            'kind': 'function',
            'signature': f"def {name}({args})",
            'docstring': doc.strip(),
            'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),
            'line': source[:match.start()].count('\n') + 1
        })

    # Regex for class defs
    class_pattern = r'class\s+(\w+)\s*\(([^)]*)\)\s*:\s*(?:"""(.*?)"""|\'\'\'(.*?)\'\'\'|)'
    for match in re.finditer(class_pattern, source, re.DOTALL):
        name = match.group(1)
        bases = match.group(2)
        doc = match.group(3) or match.group(4) or ''
        symbols.append({
            'name': name,
            'kind': 'class',
            'signature': f"class {name}({bases})",
            'docstring': doc.strip(),
            'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),
            'line': source[:match.start()].count('\n') + 1
        })

    # Simple import regex
    import_pattern = r'import\s+(\w+)'
    for match in re.finditer(import_pattern, source):
        imports.append({
            'name': match.group(1),
            'as': None,
            'module': str(Path(file_path).relative_to(Path(file_path).parent.parent))
        })

    # Simple call regex (heuristic)
    call_pattern = r'(\w+)\s*\('
    for match in re.finditer(call_pattern, source):
        calls.append({
            'caller': None,
            'callee': match.group(1),
            'module': str(Path(file_path).relative_to(Path(file_path).parent.parent)),
            'line': source[:match.start()].count('\n') + 1
        })

    return {'symbols': symbols, 'imports': imports, 'calls': calls}

def parse_file(file_path: str) -> Dict[str, Any]:
    """
    Parse a file based on extension.
    """
    if file_path.endswith('.py'):
        return parse_python_file(file_path)
    elif file_path.endswith('.jac'):
        return parse_jac_file(file_path)
    else:
        return {'symbols': [], 'imports': [], 'calls': []}
