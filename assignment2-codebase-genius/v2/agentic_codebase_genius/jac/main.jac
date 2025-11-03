import * from "repo_mapper.jac";
import * from "code_analyzer.jac";
import * from "docgenie.jac";
import * from "supervisor.jac";

walker GenerateDocsAPI {
    can http.get, http.post;
    has repo_url: str?;

    with entry {
        if self.request.method == "POST" and "repo_url" in self.request.data {
            self.repo_url = self.request.data["repo_url"];
            result = spawn Supervisor(repo_url=self.repo_url);
            self.response = {"status": "success", "docs_path": result};
        } else {
            self.response = {"status": "error", "message": "Invalid request"};
        }
    }
}
