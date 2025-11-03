import unittest
import tempfile
import os
import shutil
from pathlib import Path

# Assuming the py_modules are in the parent directory
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'py_modules'))

from repo_mapper import build_file_tree, find_readme, summarize_readme, find_entry_points, map_repo

class TestRepoMapper(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_build_file_tree(self):
        # Create some structure
        subdir = Path(self.temp_dir) / 'subdir'
        subdir.mkdir()
        (Path(self.temp_dir) / 'file1.txt').write_text('test')
        (subdir / 'file2.py').write_text('print("hello")')

        tree = build_file_tree(self.temp_dir)
        self.assertIn('file1.txt', tree)
        self.assertIn('subdir', tree)
        self.assertIn('file2.py', tree['subdir'])

    def test_find_readme(self):
        readme_path = Path(self.temp_dir) / 'README.md'
        readme_path.write_text('# Test Readme')
        content = find_readme(self.temp_dir)
        self.assertEqual(content, '# Test Readme')

    def test_summarize_readme(self):
        content = "Line 1\nLine 2\nLine 3"
        summary = summarize_readme(content)
        self.assertIn('Summary:', summary)

    def test_find_entry_points(self):
        main_py = Path(self.temp_dir) / 'main.py'
        main_py.write_text('if __name__ == "__main__": pass')
        setup_py = Path(self.temp_dir) / 'setup.py'
        setup_py.write_text('from setuptools import setup')
        points = find_entry_points(self.temp_dir)
        self.assertIn(str(main_py), points)
        self.assertIn(str(setup_py), points)

    def test_map_repo(self):
        readme_path = Path(self.temp_dir) / 'README.md'
        readme_path.write_text('# Test')
        main_py = Path(self.temp_dir) / 'main.py'
        main_py.write_text('print("main")')

        result = map_repo(self.temp_dir)
        self.assertIn('file_tree', result)
        self.assertIn('readme_summary', result)
        self.assertIn('entry_points', result)

if __name__ == '__main__':
    unittest.main()