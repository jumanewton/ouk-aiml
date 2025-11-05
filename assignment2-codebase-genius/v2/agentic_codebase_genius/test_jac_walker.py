#!/usr/bin/env python3
"""Test script to run the Jac CodebaseGenius walker."""

import sys
import os
sys.path.append('.')

# Import Jac runtime
from jaclang import JacMachine

def test_jac_walker():
    """Test the Jac walker by loading the main.jac file and calling the walker."""
    try:
        # Create Jac machine
        machine = JacMachine()

        # Load the Jac file
        jac_file = 'jac/main.jac'
        if not os.path.exists(jac_file):
            print(f"Error: {jac_file} not found")
            return

        # Execute the Jac file
        machine.exec_file(jac_file)

        # Try to call the walker
        result = machine.walk('CodebaseGenius.generate_docs', {'repo_url': 'https://github.com/octocat/Hello-World.git'})
        print("Jac Walker Result:", result)

    except Exception as e:
        print(f"Error running Jac walker: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_jac_walker()