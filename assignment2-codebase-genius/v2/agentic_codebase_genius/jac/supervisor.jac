import py_module.repo_mapper;
import py_module.code_analyzer;
import py_module.docgenie;
import py_module.supervisor;

node Repository {
    has repo_url: str;
    has repo_path: str?;
    has file_tree: dict?;
    has readme_summary: str?;
    has ccg: dict?;
    has docs_path: str?;
}

walker Supervisor {
    has repo_url: str;

    with entry {
        # Use the Python supervisor wrapper for orchestration for now
        result = py_module.supervisor.generate_docs(self.repo_url);
        report(result);
    }
}
