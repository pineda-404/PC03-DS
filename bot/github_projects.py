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
        """Ejecuta comando gh CLI y retorna JSON."""
        result = subprocess.run(
            ["gh"] + list(args), capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout) if result.stdout.strip() else {}

    def _ensure_project_metadata(self):
        """Cachea IDs del proyecto, field Status y sus opciones."""
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
        """
        Mueve una tarjeta a una columna específica.

        Args:
            issue_number: Número del issue
            column_name: Nombre de la columna (ej: "In Progress", "Done")
        """
        self._ensure_project_metadata()

        if column_name not in self._status_options:
            raise ValueError(f"Columna '{column_name}' no existe en el proyecto")

        # Primero agregar issue al proyecto si no está
        try:
            self._run_gh(
                "project",
                "item-add",
                str(self.project_number),
                "--owner",
                self.owner,
                "--url",
                f"https://github.com/{self.owner}/{self.repo}/issues/{issue_number}",
            )
        except subprocess.CalledProcessError:
            pass  # Ya está en el proyecto

        # Obtener item-id del issue
        items = self._run_gh(
            "project",
            "item-list",
            str(self.project_number),
            "--owner",
            self.owner,
            "--format",
            "json",
            "--limit",
            "100",
        )

        item_id = None
        for item in items["items"]:
            if item.get("content", {}).get("number") == issue_number:
                item_id = item["id"]
                break

        if not item_id:
            raise ValueError(f"Issue #{issue_number} no encontrado en proyecto")

        # Mover tarjeta
        self._run_gh(
            "project",
            "item-edit",
            "--id",
            item_id,
            "--project-id",
            self._project_id,
            "--field-id",
            self._status_field_id,
            "--single-select-option-id",
            self._status_options[column_name],
        )
