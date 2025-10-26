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
    
    walker summarize_module(module_path: str, symbols: list, code_snippet: str = "") -> str {
        prompt = "Return a Markdown fragment with heading equal to module path, then 2-3 sentence description, list exported functions/classes with one-line descriptions, and sample usage if a main entry point exists. If unsure about a function's behavior, use 'behaviour unclear from source'.\n\nModule: " + module_path + "\n\nSymbols:\n" + py_module.json.dumps(symbols, indent=2) + "\n\nCode snippet:\n" + code_snippet[:1000];
        
        try {
            response = py_module.byllm.generate(prompt);
            return response;
        } catch e {
            return "# " + module_path + "\nError summarizing: " + str(e);
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
        
        # Module summaries
        module_summaries = [];
        module_set = set();
        for sym in symbols:
            mod = sym['module'];
            if mod not in module_set:
                module_set.add(mod);
                # Get symbols for this module
                mod_symbols = [s for s in symbols if s['module'] == mod];
                summary = self.summarize_module(mod, mod_symbols, "");
                module_summaries.append(summary);
        
        module_summaries_section = "\n## Module Summaries\n\n" + "\n\n".join(module_summaries);
        
        full_docs = py_module.doc_template.assemble_docs(repo_name, repo_url, overview, installation, usage, api_reference, architecture, contributing) + module_summaries_section;
        
        with open(str(output_path), 'w') as f {
            f.write(full_docs);
        }
        
        return str(output_path);
    }
}
