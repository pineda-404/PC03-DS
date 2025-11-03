import pytest

from bot.event_handlers import EventHandler


@pytest.fixture
def handler():
    return EventHandler()


class TestIntegrationFlow:
    """Tests de flujo end-to-end del Sprint 1."""

    def test_full_detection_flow(self, handler):
        """Test de flujo completo: commit → detección → resultado."""
        commits = [
            "feat: add login",
            "incident: P1 - Auth broken",
            "fix: typo",
            "incident: Cache miss",
        ]

        results = [handler.handle_commit(msg) for msg in commits]
        incidents = [r for r in results if r is not None]

        assert len(incidents) == 2
        assert incidents[0]["severity"] == "P1"
        assert incidents[0]["title"] == "Auth broken"
        assert incidents[1]["severity"] == "P3"
        assert incidents[1]["title"] == "Cache miss"

    def test_cli_workflow_simulation(self, handler):
        """Simula lo que haría el CLI sin ejecutarlo."""
        # Incidente detectado
        result1 = handler.handle_commit("incident: P0 - Critical failure")
        assert result1 is not None
        # En Sprint 2: aquí se llamaría a github_client.create_issue()

        # No es incidente
        result2 = handler.handle_commit("docs: update README")
        assert result2 is None
