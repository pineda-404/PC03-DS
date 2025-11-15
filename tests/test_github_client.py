import pytest
from github import BadCredentialsException, RateLimitExceededException

from bot.github_client import GitHubClient


@pytest.fixture
def mock_github(mocker):
    """Mock de la clase Github de PyGithub con autospec."""
    mock = mocker.patch("bot.github_client.Github", autospec=True)
    return mock


@pytest.fixture
def mock_repo(mocker):
    """Mock del repositorio con autospec."""
    mock = mocker.MagicMock()
    mock.create_issue = mocker.MagicMock()
    return mock


@pytest.fixture
def client(mock_github, mock_repo):
    """Fixture que crea un GitHubClient con mocks configurados."""
    # Configurar el mock para que get_repo devuelva mock_repo
    mock_instance = mock_github.return_value
    mock_instance.get_repo.return_value = mock_repo

    client = GitHubClient(
        token="fake-token",
        owner="test-owner",
        repo="test-repo"
    )
    return client


class TestGitHubClient:
    """Tests esenciales para GitHubClient - 8 tests totales."""

    def test_client_initialization(self, mock_github):
        """Test 1: Inicialización correcta del cliente.

        Valida: creación del cliente con token, owner y repo correctos.
        """
        client = GitHubClient(
            token="test-token",
            owner="test-owner",
            repo="test-repo"
        )

        # Verificar que Github se instanció con el token correcto
        mock_github.assert_called_once_with("test-token")
        assert client.owner == "test-owner"
        assert client.repo == "test-repo"
        assert client._repo is None

    def test_create_issue_success_and_call_args(
        self, client, mock_repo, mock_github
    ):
        """Test 2: Creación exitosa de issue y verificación de call_args.

        Valida:
        - Issue se crea correctamente
        - Retorna el número de issue
        - get_repo se llama con formato correcto
        - create_issue recibe title, body y labels correctos
        """
        # Configurar mock del issue creado
        mock_issue = (mock_github.return_value.get_repo.return_value
                      .create_issue.return_value)
        mock_issue.number = 42

        # Ejecutar
        issue_number = client.create_incident_issue(
            title="API timeout",
            severity="P1"
        )

        # Verificar resultado
        assert issue_number == 42

        # Verificar que se llamó get_repo correctamente
        mock_github.return_value.get_repo.assert_called_once_with(
            "test-owner/test-repo"
        )

        # Verificar call_args de create_issue
        mock_repo.create_issue.assert_called_once()
        call_args = mock_repo.create_issue.call_args

        assert call_args.kwargs["title"] == "API timeout"
        assert "P1" in call_args.kwargs["body"]
        assert call_args.kwargs["labels"] == ["P1", "incident"]

    def test_repo_caching_optimization(
        self, client, mock_repo, mock_github
    ):
        """Test 3: El repositorio se cachea después de la primera llamada.

        Valida: Optimización importante - get_repo solo se llama una vez.
        """
        mock_issue = (mock_github.return_value.get_repo.return_value
                      .create_issue.return_value)
        mock_issue.number = 10

        # Primera llamada
        client.create_incident_issue("First issue", "P0")

        # Segunda llamada
        mock_issue.number = 20
        client.create_incident_issue("Second issue", "P2")

        # get_repo solo debe llamarse una vez (cacheo)
        mock_github.return_value.get_repo.assert_called_once()

        # create_issue debe llamarse dos veces
        assert mock_repo.create_issue.call_count == 2

    @pytest.mark.parametrize("severity,expected_labels", [
        ("P0", ["P0", "incident"]),
        ("P1", ["P1", "incident"]),
        ("P2", ["P2", "incident"]),
        ("P3", ["P3", "incident"]),
    ])
    def test_labels_by_severity(
        self, client, mock_repo, mock_github, severity, expected_labels
    ):
        """Test 4: Labels correctos según severidad (parametrizado P0-P3).

        Valida: Lógica de negocio core - asignación de labels por
        severidad. Este test parametrizado cuenta como 4 ejecuciones.
        """
        mock_issue = (mock_github.return_value.get_repo.return_value
                      .create_issue.return_value)
        mock_issue.number = 100

        # Ejecutar
        client.create_incident_issue(
            title=f"Test issue {severity}",
            severity=severity
        )

        # Verificar labels - esto es lo más importante
        call_args = mock_repo.create_issue.call_args
        assert call_args.kwargs["labels"] == expected_labels

    def test_bad_credentials_exception(self, mock_github):
        """Test 5: Error de autenticación (401).

        Valida: Manejo correcto de credenciales inválidas.
        """
        # Configurar mock para lanzar BadCredentialsException
        mock_github.return_value.get_repo.side_effect = (
            BadCredentialsException(
                status=401,
                data={"message": "Bad credentials"}
            )
        )

        client = GitHubClient(
            token="invalid-token",
            owner="owner",
            repo="repo"
        )

        # Verificar que la excepción se propaga correctamente
        with pytest.raises(BadCredentialsException) as exc_info:
            client.create_incident_issue("Test", "P0")

        assert exc_info.value.status == 401

    def test_rate_limit_exception(self, mock_github):
        """Test 6: Error de rate limit (403).

        Valida: Manejo correcto cuando se excede el límite de API.
        """
        # Configurar mock para lanzar RateLimitExceededException
        mock_instance = mock_github.return_value
        mock_repo = mock_instance.get_repo.return_value
        mock_repo.create_issue.side_effect = (
            RateLimitExceededException(
                status=403,
                data={"message": "API rate limit exceeded"}
            )
        )

        client = GitHubClient(
            token="valid-token",
            owner="owner",
            repo="repo"
        )

        # Verificar que la excepción se propaga correctamente
        with pytest.raises(RateLimitExceededException) as exc_info:
            client.create_incident_issue("Test", "P1")

        assert exc_info.value.status == 403

    def test_bad_credentials_on_get_repo(self, mock_github):
        """Test 7: Error de autenticación al obtener el repositorio.

        Valida: Fallo antes de crear issue (token sin permisos de
        lectura).
        """
        # Simular error al intentar obtener el repo
        mock_github.return_value.get_repo.side_effect = (
            BadCredentialsException(
                status=401,
                data={"message": "Token sin permisos"}
            )
        )

        client = GitHubClient(
            token="limited-token",
            owner="owner",
            repo="repo"
        )

        with pytest.raises(BadCredentialsException):
            client.create_incident_issue("Test", "P2")

    def test_call_args_list_multiple_calls(
        self, client, mock_repo, mock_github
    ):
        """Test 8: Verificar call_args_list con múltiples llamadas.

        Valida: Historial completo de llamadas y sus argumentos.
        """
        mock_issue = (mock_github.return_value.get_repo.return_value
                      .create_issue.return_value)
        mock_issue.number = 111

        # Crear múltiples issues con diferentes severidades
        client.create_incident_issue("Critical failure", "P0")
        mock_issue.number = 222
        client.create_incident_issue("Minor bug", "P3")

        # Verificar call_args_list
        calls = mock_repo.create_issue.call_args_list
        assert len(calls) == 2

        # Primera llamada (P0)
        first_call = calls[0]
        assert first_call.kwargs["title"] == "Critical failure"
        assert first_call.kwargs["labels"] == ["P0", "incident"]
        assert "P0" in first_call.kwargs["body"]

        # Segunda llamada (P3)
        second_call = calls[1]
        assert second_call.kwargs["title"] == "Minor bug"
        assert second_call.kwargs["labels"] == ["P3", "incident"]
        assert "P3" in second_call.kwargs["body"]
