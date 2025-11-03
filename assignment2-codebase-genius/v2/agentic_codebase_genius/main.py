from flask import Flask, request, jsonify
import sys
import os
sys.path.append('py_module')

from repo_mapper import map_repository
from code_analyzer import analyze_codebase
from docgenie import generate_docs

app = Flask(__name__)

@app.route('/generate-docs', methods=['POST'])
def generate_docs_endpoint():
    data = request.get_json()
    repo_url = data.get('repo_url')
    if not repo_url:
        return jsonify({"status": "error", "message": "repo_url required"}), 400

    try:
        # Map repository
        result = map_repository(repo_url)

        # Analyze code
        ccg = analyze_codebase(result['repo_path'])

        # Generate docs
        docs_path = generate_docs(result['file_tree'], result['readme_summary'], ccg, repo_url)

        return jsonify({"status": "success", "docs_path": docs_path})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)