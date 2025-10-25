import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from ccg import CodeContextGraph

class TestCCG(unittest.TestCase):

    def test_build_graph(self):
        ccg = CodeContextGraph()

        symbols = [
            {'name': 'hello', 'kind': 'function', 'signature': 'def hello()', 'docstring': '', 'module': 'test.py', 'line': 1},
            {'name': 'Greeter', 'kind': 'class', 'signature': 'class Greeter()', 'docstring': '', 'module': 'test.py', 'line': 5, 'bases': []},
            {'name': 'greet', 'kind': 'function', 'signature': 'def greet()', 'docstring': '', 'module': 'test.py', 'line': 7}
        ]

        calls = [
            {'caller': 'greet', 'callee': 'hello', 'module': 'test.py', 'line': 8}
        ]

        imports = [
            {'name': 'os', 'as': None, 'module': 'test.py'}
        ]

        ccg.add_symbols(symbols)
        ccg.add_calls(calls)
        ccg.add_inherits(symbols)
        ccg.add_imports(imports)

        self.assertIn('test.py::hello', ccg.graph.nodes)
        self.assertIn('test.py::greet', ccg.graph.nodes)
        self.assertTrue(ccg.graph.has_edge('test.py::greet', 'test.py::hello'))
        self.assertTrue(ccg.graph.has_edge('test.py', 'os'))

    def test_query_functions_calling(self):
        ccg = CodeContextGraph()
        ccg.graph.add_edge('caller', 'hello', type='calls')
        callers = ccg.query_functions_calling('hello')
        self.assertIn('caller', callers)

    def test_get_high_impact_functions(self):
        ccg = CodeContextGraph()
        ccg.graph.add_edge('a', 'hello', type='calls')
        ccg.graph.add_edge('b', 'hello', type='calls')
        ccg.graph.add_edge('c', 'world', type='calls')
        high = ccg.get_high_impact_functions()
        self.assertIn('hello', high)

if __name__ == '__main__':
    unittest.main()