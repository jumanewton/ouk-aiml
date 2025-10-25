import unittest
import tempfile
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from parser_utils import parse_python_file, parse_jac_file

class TestParserUtils(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)

    def test_parse_python_file(self):
        code = '''
def hello(name: str = "world") -> str:
    """Say hello."""
    print(f"Hello {name}")
    return f"Hello {name}"

class Greeter:
    """A greeter class."""
    def greet(self):
        hello("there")

import os
from sys import path
'''
        file_path = os.path.join(self.temp_dir, 'test.py')
        with open(file_path, 'w') as f:
            f.write(code)

        result = parse_python_file(file_path)
        symbols = result['symbols']
        imports = result['imports']
        calls = result['calls']

        # Check symbols
        self.assertEqual(len(symbols), 3)  # hello func, Greeter class, greet method
        func_hello = next(s for s in symbols if s['name'] == 'hello')
        self.assertEqual(func_hello['kind'], 'function')
        self.assertIn("def hello(name: str='world')", func_hello['signature'])
        self.assertEqual(func_hello['docstring'], 'Say hello.')

        class_greeter = next(s for s in symbols if s['name'] == 'Greeter')
        self.assertEqual(class_greeter['kind'], 'class')

        # Check imports
        self.assertTrue(any(imp['name'] == 'os' for imp in imports))
        self.assertTrue(any(imp['name'] == 'sys.path' for imp in imports))

        # Check calls
        hello_calls = [c for c in calls if c['callee'] == 'hello']
        self.assertEqual(len(hello_calls), 1)
        self.assertEqual(hello_calls[0]['caller'], 'greet')

    def test_parse_jac_file(self):
        code = '''
def hello(name):
    """Say hello."""
    print("Hello")

class Greeter():
    """Greeter."""
    pass

import os
'''
        file_path = os.path.join(self.temp_dir, 'test.jac')
        with open(file_path, 'w') as f:
            f.write(code)

        result = parse_jac_file(file_path)
        symbols = result['symbols']
        imports = result['imports']

        self.assertEqual(len(symbols), 2)
        self.assertTrue(any(s['name'] == 'hello' for s in symbols))
        self.assertTrue(any(s['name'] == 'Greeter' for s in symbols))
        self.assertTrue(any(imp['name'] == 'os' for imp in imports))

if __name__ == '__main__':
    unittest.main()