import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from docgenie import rewrite_section_with_llm

class TestDocgenieLLM(unittest.TestCase):
    
    def test_rewrite_section_with_llm(self):
        section = "Overview"
        content = "This is the original content."
        result = rewrite_section_with_llm(section, content)
        # Since it's fallback, should return content unchanged
        self.assertEqual(result, content)

if __name__ == '__main__':
    unittest.main()