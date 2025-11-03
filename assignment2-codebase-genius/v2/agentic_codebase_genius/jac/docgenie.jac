import py_module.docgenie as dg;

node Documentation {
    has file_tree: dict;
    has readme_summary: str;
    has ccg: dict;
    has repo_url: str;
    has docs_path: str?;
}

walker GenerateDocs {
    can docgenie.GenerateDocs;
    has file_tree: dict;
    has readme_summary: str;
    has ccg: dict;
    has repo_url: str;

    with entry {
        self.file_tree = here.file_tree;
        self.readme_summary = here.readme_summary;
        self.ccg = here.ccg;
        self.repo_url = here.repo_url;
        here.docs_path = dg.generate_docs(self.file_tree, self.readme_summary, self.ccg, self.repo_url);
    }
}