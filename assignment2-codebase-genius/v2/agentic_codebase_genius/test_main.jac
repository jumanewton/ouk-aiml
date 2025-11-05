import py_module.supervisor;
import py_module.repo_mapper;
import py_module.code_analyzer;
import py_module.docgenie;

node CodebaseGenius {
    walker generate_docs {
        has repo_url: str;
        can enter with root entry {
            if not self.repo_url {
                return {"success": False, "error": "Missing repo_url parameter"};
            }
            result = py_module.supervisor.generate_docs(self.repo_url);
            return result;
        }
    }
}

// Test the walker
walker test_walker {
    can CodebaseGenius.generate_docs(repo_url="https://github.com/octocat/Hello-World.git") as result {
        std.out("Test Result:", result);
    }
}