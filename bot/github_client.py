from github import (
    BadCredentialsException,
    Github,
    RateLimitExceededException,
)


class GitHubClient:
    """Facade para interactuar con la API de GitHub (issues)."""

    def __init__(self, token, owner, repo):
        self.client = Github(token)
        self.owner = owner
        self.repo = repo
        self._repo = None

    def create_incident_issue(self, title, severity):
        try:
            if not self._repo:
                self._repo = self.client.get_repo(f"{self.owner}/{self.repo}")

            body = f" Incidente detectado automaticamente por el bot\n\n**Severidad:** {severity}"
            labels = [severity, "incident"]

            issue = self._repo.create_issue(title=title, body=body, labels=labels)

            return issue.number

        except BadCredentialsException:
            raise BadCredentialsException(
                status=401, data={"message": "Token de GitHub inválido o sin permisos"}
            )
        except RateLimitExceededException:
            raise RateLimitExceededException(
                status=403, data={"message": "Límite de rate limit alcanzado"}
            )
