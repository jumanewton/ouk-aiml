node CodeGenius {
    walker init {
        can enter with root entry {
            report(root);
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }
    walker main {
        can enter with root entry {
            repo_url = py_module.os.environ.get('REPO_URL', "https://github.com/octocat/Hello-World");
            result = self.generate_docs(repo_url=repo_url);
            if result.get('success') {
                py_module.print("Docs generated at " + result.get('docs_path'));
            } else {
                py_module.print("Error: " + result.get('error'));
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
    
    walker generate_docs {
        has repo_url: str;
        has outputs_dir: str = "./outputs";
        can enter with root entry {
            clone_result = py_module.git_utils.clone_repo(self.repo_url);
            if not clone_result.get('success') {
                return py_module.dict([["success", False], ["error", clone_result.get('error')]]);
            }
            
            local_path = clone_result.get('path');
            repo_map = py_module.repo_mapper.map_repo(local_path);
            
            plan = self.plan_documentation_targets(repo_map=repo_map);
            targets = plan.get('prioritized_files');
            if not targets {
                targets = repo_map.get('entry_points');
            }
            if not targets {
                targets = py_module.list(py_module.pathlib.Path(local_path).rglob("*.py"));
            }
            
            ccg = py_module.ccg.build_ccg(targets);
            
            symbols = py_module.list();
            for t in targets {
                parsed = py_module.parser_utils.parse_file(t);
                symbols.extend(parsed.get('symbols', py_module.list()));
            }
            
            docs_path = py_module.docgenie.generate_docs(self.repo_url, repo_map, ccg, symbols, self.outputs_dir);
            py_module.shutil.rmtree(local_path);
            return py_module.dict([["success", True], ["docs_path", docs_path]]);
        }
        obj __specs__ {
            static has auth: bool = False;
        }
    }
}
