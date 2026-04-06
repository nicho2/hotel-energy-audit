class ExecutiveReportBuilder:
    def build_context(self, project: dict, results: dict, branding: dict | None = None) -> dict:
        return {
            "project": project,
            "results": results,
            "branding": branding or {},
        }
