import py_module.repo_mapper as rm;
import py_module.code_analyzer as ca;
import py_module.docgenie as dg;

node Repository {
    has repo_url: str;
    has repo_path: str?;
    has file_tree: dict?;
    has readme_summary: str?;
    has ccg: dict?;
    has docs_path: str?;
}

walker Supervisor {
    can supervisor.Supervisor;
    has repo_url: str;

    with entry {
        # Create repository node
        repo = spawn Repository(repo_url=self.repo_url);

        # Map repository
        spawn MapRepository(repo_url=self.repo_url) -> repo;

        # Analyze code
        spawn AnalyzeCode(repo_path=repo.repo_path) -> repo;

        # Generate docs
        spawn GenerateDocs(file_tree=repo.file_tree, readme_summary=repo.readme_summary, ccg=repo.ccg, repo_url=self.repo_url) -> repo;

        # Return result
        report repo.docs_path;
    }
}
