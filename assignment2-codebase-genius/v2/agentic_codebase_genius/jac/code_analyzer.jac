import py_module.code_analyzer;

node Codebase {
    has repo_path: str;
    has ccg: dict?;
}

walker AnalyzeCode {
    has repo_path: str;

    with entry {
        self.repo_path = here.repo_path;
        here.ccg = py_module.code_analyzer.analyze_codebase(self.repo_path);
    }
}
