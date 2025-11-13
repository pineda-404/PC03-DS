import json
import subprocess


class GitHubProjects:
    """Facade para mover tarjetas en GitHub Projects usando gh CLI."""

    def __init__(self, owner, repo, project_number):
        self.owner = owner
        self.repo = repo
        self.project_number = project_number
        self._project_id = None
        self._status_field_id = None
        self._status_options = {}

    def _run_gh(self, *args):
        result = subprocess.run(
            ["gh"] + list(args), capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def _ensure_project_metadata(self):
        if self._project_id:
            return

        data = self._run_gh(
            "project",
            "view",
            str(self.project_number),
            "--owner",
            self.owner,
            "--format",
            "json",
        )
        self._project_id = data["id"]

        fields = self._run_gh(
            "project",
            "field-list",
            str(self.project_number),
            "--owner",
            self.owner,
            "--format",
            "json",
        )

        for field in fields["fields"]:
            if field["name"] == "Status":
                self._status_field_id = field["id"]
                for option in field["options"]:
                    self._status_options[option["name"]] = option["id"]
                break

    def move_card(self, issue_number, column_name):
        self._ensure_project_metadata()

        if column_name not in self._status_options:
            raise ValueError(f"Columna '{column_name}' no existe en el proyecto")

        self._run_gh(
            "project",
            "item-edit",
            "--project-id",
            self._project_id,
            "--field-id",
            self._status_field_id,
            "--option-id",
            self._status_options[column_name],
            "--id",
            f"{self.owner}/{self.repo}#{issue_number}",
        )
