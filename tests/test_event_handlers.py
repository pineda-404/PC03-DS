import pytest

from bot.event_handlers import EventHandler


@pytest.fixture
def handler():
    return EventHandler()


class TestBasicFunctionality:
    @pytest.mark.parametrize(
        "commit_msg, expected_title, expected_severity",
        [
            ("incident: API timeout", "API timeout", "P3"),
            ("incident: Database connection lost", "Database connection lost", "P3"),
            ("incident: P0 - System down", "System down", "P0"),
            ("incident: P1 - Auth broken", "Auth broken", "P1"),
            ("incident: P2 - Slow queries", "Slow queries", "P2"),
            ("incident: P3 - Minor bug", "Minor bug", "P3"),
            ("incident:Cache miss", "Cache miss", "P3"),
            ("incident:P0-Critical", "Critical", "P0"),
        ],
    )
    def test_valid_incidents(
        self, handler, commit_msg, expected_title, expected_severity
    ):
        result = handler.handle_commit(commit_msg)
        assert result is not None
        assert result["title"] == expected_title
        assert result["severity"] == expected_severity


class TestInvalidCases:
    @pytest.mark.parametrize(
        "commit_msg",
        [
            "fix: corregir bug en parser",
            "feat: agregar nueva función",
            "docs: actualizar README",
            "refactor: limpiar código",
            "Incident: API caída",  # Mayúscula → no detecta
            "INCIDENT: bug crítico",  # Todo mayúsculas → no detecta
            "fix incident en código",  # En medio → no detecta
        ],
    )
    def test_non_incidents(self, handler, commit_msg):
        result = handler.handle_commit(commit_msg)
        assert result is None


class TestEdgeCases:
    @pytest.mark.parametrize(
        "commit_msg, expected",
        [
            ("incident:", None),
            ("incident: ", None),
            ("incident:  ", None),
            ("incident: P0", None),
            ("incident: P1 - ", None),
            ("incident:  API   timeout  ", {"title": "API timeout", "severity": "P3"}),
            ("incident: P0 -  Critical  ", {"title": "Critical", "severity": "P0"}),
        ],
    )
    def test_edge_cases(self, handler, commit_msg, expected):
        result = handler.handle_commit(commit_msg)
        if expected is None:
            assert result is None
        else:
            assert result == expected

    def test_very_long_title(self, handler):
        long_title = "X" * 250
        result = handler.handle_commit(f"incident: {long_title}")
        assert result is not None
        assert len(result["title"]) == 250

    def test_multiple_priorities_takes_first(self, handler):
        result = handler.handle_commit("incident: P0 - Critical P1 issue")
        assert result["severity"] == "P0"
        assert "P1" in result["title"]


class TestIntegration:
    def test_process_multiple_commits(self, handler):
        commits = [
            ("feat: add login", None),
            ("incident: P1 - Auth broken", {"title": "Auth broken", "severity": "P1"}),
            ("fix: resolve auth", None),
            ("incident: Cache miss", {"title": "Cache miss", "severity": "P3"}),
            ("incident: P0 - System down", {"title": "System down", "severity": "P0"}),
        ]

        results = [handler.handle_commit(msg) for msg, _ in commits]
        incidents = [r for r in results if r is not None]

        assert len(incidents) == 3
        severities = [i["severity"] for i in incidents]
        assert set(severities) == {"P0", "P1", "P3"}
