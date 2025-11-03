node CodeGenius {
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
                    "error": "Missing repo_url parameter. Please provide a GitHub repository URL."
                };
            }

            try {
                # Validate URL format
                if not (self.repo_url.startswith("https://github.com/") or self.repo_url.startswith("http://github.com/")) {
                    return {
                        "success": False,
                        "error": "Invalid repository URL. Only GitHub repositories are supported."
                    };
                }

                result = py_module.supervisor.generate_docs(self.repo_url);
                return result;
            } catch e {
                return {
                    "success": False,
                    "error": f"Server error during documentation generation: {str(e)}"
                };
            }
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }

    walker plan_documentation_targets {
        has repo_map: dict;
        can enter with root entry {
            readme_summary = self.repo_map.get('readme_summary', '');
            entry_points = self.repo_map.get('entry_points', []);
            file_tree = self.repo_map.get('file_tree', {});
            
            prompt = "Based on the repository summary and structure, prioritize the top 5-10 files that should be documented first for a comprehensive overview. Focus on entry points, main modules, and high-impact files.\n\nREADME Summary: " + readme_summary + "\n\nEntry Points: " + ', '.join(entry_points) + "\n\nFile Tree (top-level): " + str(file_tree)[:1000] + "\n\nReturn a JSON list of prioritized file paths (relative to repo root).";
            
            response = py_module.byllm.generate(prompt);
            prioritized = py_module.json.loads(response);
            if isinstance(prioritized, list) {
                return py_module.dict([["prioritized_files", prioritized]]);
            }
            
            # Fallback to entry points
            return py_module.dict([["prioritized_files", entry_points]]);
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }
}
