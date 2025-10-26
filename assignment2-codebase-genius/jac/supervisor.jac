node CodeGenius {
    walker plan_documentation_targets(repo_map: dict, local_path: str) -> dict {
        readme_summary = repo_map.get('readme_summary', '');
        entry_points = repo_map.get('entry_points', []);
        file_tree = repo_map.get('file_tree', {});
        
        prompt = "Based on the repository summary and structure, prioritize the top 5-10 files that should be documented first for a comprehensive overview. Focus on entry points, main modules, and high-impact files.\n\nREADME Summary: " + readme_summary + "\n\nEntry Points: " + ', '.join(entry_points) + "\n\nFile Tree (top-level): " + str(file_tree)[:1000] + "\n\nReturn a JSON array of strings, where each string is a relative file path from the repository root (e.g., [\"main.py\", \"src/app.py\"]). Only include paths that exist in the repository. If no suitable files, return an empty array.";
        
        try {
            response = py_module.byllm.generate(prompt);
            # Try to parse as JSON
            prioritized = py_module.json.loads(response);
            if isinstance(prioritized, list) {
                # Validate and filter paths
                validated = [];
                for p in prioritized {
                    if isinstance(p, str) {
                        full_path = py_module.pathlib.Path(local_path) / p;
                        if full_path.exists() and full_path.is_file() {
                            validated.append(str(full_path));  # absolute path
                        }
                    }
                }
                return {"prioritized_files": validated};
            }
        } catch {
            # If JSON fails, try to extract JSON from response
            import re;
            json_match = re.search(r'\[.*\]', response);
            if json_match {
                try {
                    prioritized = py_module.json.loads(json_match.group(0));
                    if isinstance(prioritized, list) {
                        validated = [];
                        for p in prioritized {
                            if isinstance(p, str) {
                                full_path = py_module.pathlib.Path(local_path) / p;
                                if full_path.exists() and full_path.is_file() {
                                    validated.append(str(full_path));
                                }
                            }
                        }
                        return {"prioritized_files": validated};
                    }
                } catch {
                }
            }
        }
        
        # Fallback to entry points, validated
        validated = [];
        for ep in entry_points {
            full_path = py_module.pathlib.Path(local_path) / ep;
            if full_path.exists() and full_path.is_file() {
                validated.append(str(full_path));
            }
        }
        return {"prioritized_files": validated};
    }
    
    walker generate_docs(repo_url: str, outputs_dir: str = "./outputs") -> dict {
        clone_result = py_module.git_utils.clone_repo(repo_url);
        if not clone_result.get('success') {
            return {"success": False, "error": clone_result.get('error')};
        }
        
        local_path = clone_result.get('path');
        try {
            repo_map = py_module.repo_mapper.map_repo(local_path);
            
            plan = self.plan_documentation_targets(repo_map, local_path);
            targets = plan.get('prioritized_files', repo_map.get('entry_points') or []);
            if not targets {
                targets = [str(p) for p in py_module.pathlib.Path(local_path).rglob("*.py")][:10];
            }
            
            ccg = py_module.ccg.build_ccg(targets);
            
            symbols = [];
            for t in targets {
                parsed = py_module.parser_utils.parse_file(t);
                symbols.extend(parsed.get('symbols', []));
            }
            
            docs_path = py_module.docgenie.generate_docs(repo_url, repo_map, ccg, symbols, outputs_dir);
            return {"success": True, "docs_path": docs_path};
        } finally {
            try {
                py_module.shutil.rmtree(local_path);
            } catch {
            }
        }
    }
}
