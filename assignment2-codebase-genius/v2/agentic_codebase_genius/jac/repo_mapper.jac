import py_module.repo_mapper as rm;

node Repository {
    has repo_url: str;
    has repo_path: str?;
    has file_tree: dict?;
    has readme_summary: str?;
}

walker MapRepository {
    can repo_mapper.MapRepository;
    has repo_url: str;

    with entry {
        self.repo_url = here.repo_url;
        result = rm.map_repository(self.repo_url);
        here.repo_path = result['repo_path'];
        here.file_tree = result['file_tree'];
        here.readme_summary = result['readme_summary'];
    }
}
