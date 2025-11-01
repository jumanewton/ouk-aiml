"""
Codebase Genius - Multi-agent Documentation System
Main server file that exposes HTTP endpoints for documentation generation.
"""

import py_module.supervisor;
import py_module.repo_mapper;
import py_module.code_analyzer;
import py_module.docgenie;

node CodebaseGenius {
    walker init {
        can enter with root entry {
            report(root);
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }

    walker generate_docs {
        has repo_url: str;
        can enter with root entry {
            if not self.repo_url {
                return {
                    "success": False,
                    "error": "Missing repo_url parameter"
                };
            }
            result = py_module.supervisor.generate_docs(self.repo_url);
            return result;
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }

    walker health_check {
        can enter with root entry {
            return {
                "status": "healthy",
                "service": "Codebase Genius",
                "version": "1.0.0"
            };
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }
}