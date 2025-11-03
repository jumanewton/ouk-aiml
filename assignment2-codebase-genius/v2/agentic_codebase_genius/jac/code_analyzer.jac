import py_module.code_analyzer as ca;

node Codebase {
    has repo_path: str;
    has ccg: dict?;
}

walker AnalyzeCode {
    can code_analyzer.AnalyzeCode;
    has repo_path: str;

    with entry {
        self.repo_path = here.repo_path;
        here.ccg = ca.analyze_codebase(self.repo_path);
    }
}
