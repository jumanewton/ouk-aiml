import py_module.repo_mapper;

node Repository {
    has repo_url: str;
    has repo_path: str?;
    has file_tree: dict?;
    has readme_summary: str?;
}

walker MapRepository {
    has repo_url: str;

    with entry {
        self.repo_url = here.repo_url;
        result = py_module.repo_mapper.map_repository(self.repo_url);
        here.repo_path = result['repo_path'];
        here.file_tree = result['file_tree'];
        here.readme_summary = result['readme_summary'];
    }
}
