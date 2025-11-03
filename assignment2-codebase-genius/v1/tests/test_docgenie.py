import unittest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from doc_template import render_overview, render_installation, render_usage, assemble_docs

class TestDocTemplate(unittest.TestCase):

    def test_render_overview(self):
        result = render_overview("Test summary", ["Feature 1", "Feature 2"])
        self.assertIn("Test summary", result)
        self.assertIn("Feature 1", result)

    def test_render_installation(self):
        result = render_installation("https://github.com/user/repo", "repo", True)
        self.assertIn("git clone https://github.com/user/repo", result)
        self.assertIn("pip install .", result)

    def test_render_usage(self):
        examples = [{"title": "Example 1", "code": "print('hello')"}]
        result = render_usage(examples)
        self.assertIn("Example 1", result)
        self.assertIn("print('hello')", result)

    def test_assemble_docs(self):
        result = assemble_docs("Repo", "url", "overview", "install", "usage", "api", "arch", "contrib")
        self.assertIn("# Repo", result)
        self.assertIn("overview", result)

if __name__ == '__main__':
    unittest.main()