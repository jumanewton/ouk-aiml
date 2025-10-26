node CodeAnalyzer {
    walker build_ccg(targets: list) -> object {
        return py_module.ccg.build_ccg(targets);
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
}
