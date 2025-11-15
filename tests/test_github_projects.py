import pytest
import json
from unittest.mock import MagicMock

from bot.github_projects import GitHubProjects


@pytest.fixture
def mock_subprocess(mocker):
    """Mock de subprocess.run con autospec."""
    mock = mocker.patch("bot.github_projects.subprocess.run", autospec=True)
    return mock


@pytest.fixture
def projects(mock_subprocess):
    """Fixture que crea GitHubProjects con mocks configurados."""
    project_data = {
        "id": "PVT_kwDOABCD123",
        "title": "ChatOps - Tablero Kanban",
        "number": 2,
        "url": "https://github.com/users/pineda-404/projects/2"
    }
    
    fields_data = {
        "fields": [
            {
                "id": "PVTF_status_123",
                "name": "Status",
                "dataType": "SINGLE_SELECT",
                "options": [
                    {"id": "opt_new", "name": "New Issues"},
                    {"id": "opt_progress", "name": "In Progress"},
                    {"id": "opt_review", "name": "Review/QA"},
                    {"id": "opt_done", "name": "Done"}
                ]
            }
        ]
    }
    
    def side_effect_fn(*args, **kwargs):
        """Simula respuestas de gh CLI según el comando."""
        cmd = args[0]
        
        if "project" in cmd and "view" in cmd:
            result = MagicMock()
            result.stdout = json.dumps(project_data)
            return result
        elif "field-list" in cmd:
            result = MagicMock()
            result.stdout = json.dumps(fields_data)
            return result
        elif "item-edit" in cmd:
            result = MagicMock()
            result.stdout = ""
            return result
        
        result = MagicMock()
        result.stdout = "{}"
        return result
    
    mock_subprocess.side_effect = side_effect_fn
    
    return GitHubProjects(owner="test-owner", repo="test-repo", project_number=2)


class TestGitHubProjects:
    """Suite de pruebas para GitHubProjects."""
    
    def test_initialization_sets_attributes(self):
        """Test 1: Inicialización correcta con atributos."""
        projects = GitHubProjects(
            owner="pineda-404",
            repo="PC03-DS",
            project_number=2
        )
        
        assert projects.owner == "pineda-404"
        assert projects.repo == "PC03-DS"
        assert projects.project_number == 2
        assert projects._project_id is None
        assert projects._status_field_id is None
        assert projects._status_options == {}
    
    def test_ensure_metadata_loads_project_data(self, projects, mock_subprocess):
        """Test 2: Carga de metadata del proyecto (ID, field_id y opciones)."""
        projects._ensure_project_metadata()
        
        # Verificar project_id
        assert projects._project_id == "PVT_kwDOABCD123"
        
        # Verificar status field_id
        assert projects._status_field_id == "PVTF_status_123"
        
        # Verificar opciones de columnas
        assert projects._status_options == {
            "New Issues": "opt_new",
            "In Progress": "opt_progress",
            "Review/QA": "opt_review",
            "Done": "opt_done"
        }
        
        # Verificar que se llamó a gh CLI
        calls = mock_subprocess.call_args_list
        assert any("view" in str(c) for c in calls)
        assert any("field-list" in str(c) for c in calls)
    
    def test_metadata_caching(self, projects, mock_subprocess):
        """Test 3: Metadata se cachea y no se recarga en llamadas posteriores."""
        projects._ensure_project_metadata()
        first_call_count = mock_subprocess.call_count
        
        projects._ensure_project_metadata()
        second_call_count = mock_subprocess.call_count
        
        assert first_call_count == second_call_count
        assert projects._project_id == "PVT_kwDOABCD123"
