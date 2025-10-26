node RepoMapper {
    walker summarize_readme(readme_content: str) -> str {
        if not readme_content {
            return "No README found.";
        }
        
        prompt = "You are given the contents of a project's README. Return a concise (1-3 sentence) summary suitable for the top of generated documentation. Do not invent facts; if something is unclear use the phrase 'summary unclear from README'. Keep it neutral and factual.\n\nREADME:\n" + readme_content[:5000] + "\n\nSummary:";
        
        try {
            response = py_module.byllm.generate(prompt);
            if response and isinstance(response, str) and response.strip() {
                return response.strip();
            }
        } catch {
            # best-effort: continue to fallback
        }
        
        # Fallback: first non-empty lines up to a short character budget
        lines = [l.strip() for l in readme_content.split('\n') if l.strip()];
        if not lines {
            return "No README found.";
        }
        summary_lines = [];
        chars = 0;
        for l in lines[:10] {
            summary_lines.append(l);
            chars += len(l);
            if chars > 240 {
                break;
            }
        }
        return "Summary: " + " ".join(summary_lines);
    }
    
    walker map_repo(local_path: str) -> dict {
        file_tree = py_module.repo_mapper.build_file_tree(local_path);
        readme_content = py_module.repo_mapper.find_readme(local_path);
        readme_summary = self.summarize_readme(readme_content);
        entry_points = py_module.repo_mapper.find_entry_points(local_path);
        
        return {
            "file_tree": file_tree,
            "readme_summary": readme_summary,
            "entry_points": entry_points
        };
    }
}
