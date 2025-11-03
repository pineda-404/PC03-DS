import pytest


@pytest.fixture
def sample_commits():
    return {
        "valid": [
            "incident: API timeout",
            "incident: P0 - System down",
            "incident: P1 - Memory leak",
        ],
        "invalid": [
            "fix: bug",
            "feat: new feature",
            "docs: update",
        ],
        "edge": [
            "incident:",
            "incident: P1",
            "incident: P0 - ",
        ],
    }
