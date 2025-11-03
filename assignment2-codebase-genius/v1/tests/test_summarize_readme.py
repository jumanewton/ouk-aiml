import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from repo_mapper import summarize_readme

class TestSummarizeReadme(unittest.TestCase):
    
    def test_summarize_readme_no_content(self):
        result = summarize_readme("")
        self.assertEqual(result, "No README found.")
    
    def test_summarize_readme_short_content(self):
        content = "This is a test README.\nIt has two lines."
        result = summarize_readme(content)
        self.assertIn("Summary:", result)
        self.assertIn("This is a test README.", result)
    
    def test_summarize_readme_long_content(self):
        content = "Line 1\n" * 20  # Long content
        result = summarize_readme(content)
        self.assertIn("Summary:", result)
        # Should limit to ~240 chars
        self.assertLess(len(result), 300)

if __name__ == '__main__':
    unittest.main()