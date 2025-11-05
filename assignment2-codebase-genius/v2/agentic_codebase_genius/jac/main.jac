import py_module.supervisor;
import py_module.repo_mapper;
import py_module.code_analyzer;
import py_module.docgenie;

node CodebaseGenius {
}

# Global walker for generate_docs endpoint
walker generate_docs {
    has repo_url: str;

    obj __specs__ {
        static has auth: bool = False;
    }

    can generate with entry {
        if not self.repo_url {
            report {"success": False, "error": "Missing repo_url parameter"};
            return;
        }
        result = py_module.supervisor.generate_docs(self.repo_url);
        report result;
    }
}

# Health check endpoint
walker health_check {
    obj __specs__ {
        static has auth: bool = False;
        static has methods: list = ["get"];
    }

    can check_health with entry {
        report {"status": "healthy", "service": "CodebaseGenius", "version": "1.0"};
    }
}
