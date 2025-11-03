node DocGenie {
    walker rewrite_section(section_name: str, content: str) -> str {
        prompt = "Rewrite the following " + section_name + " section to be more user-friendly and professional. Keep it concise but informative. Do not add new information.\n\nOriginal:\n" + content + "\n\nRewritten:";
        
        try {
            response = py_module.byllm.generate(prompt);
            return response.strip();
        } catch {
            return content;
        }
    }
    
    walker assemble_docs(repo_url: str, repo_map: dict, ccg: object, symbols: list, outputs_dir: str) -> str {
        repo_name = repo_url.split('/')[-1];
        output_path = py_module.pathlib.Path(outputs_dir) / repo_name / "docs.md";
        output_path.parent.mkdir(parents=True, exist_ok=True);
        
        diagrams = py_module.diagram.generate_diagrams(ccg, str(output_path.parent), repo_name);
        
        install_info = py_module.docgenie.detect_installation_info(repo_map['file_tree']);
        
        overview = py_module.doc_template.render_overview(repo_map['readme_summary']);
        overview = self.rewrite_section("Overview", overview);
        
        installation = py_module.doc_template.render_installation(repo_url, repo_name, install_info['has_setup_py']);
        
        examples = py_module.docgenie.generate_usage_examples(ccg, symbols);
        usage = py_module.doc_template.render_usage(examples);
        usage = self.rewrite_section("Usage", usage);
        
        api_data = py_module.docgenie.assemble_api_reference(symbols);
        api_reference = py_module.doc_template.render_api_reference(api_data);
        api_reference = self.rewrite_section("API Reference", api_reference);
        
        architecture = py_module.doc_template.render_architecture("This diagram shows the relationships between functions and classes in the codebase.");
        architecture = self.rewrite_section("Architecture", architecture);
        
        contributing = py_module.doc_template.render_contributing();
        
        full_docs = py_module.doc_template.assemble_docs(repo_name, repo_url, overview, installation, usage, api_reference, architecture, contributing);
        
        with open(str(output_path), 'w') as f {
            f.write(full_docs);
        }
        
        return str(output_path);
    }
}
