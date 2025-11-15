# ChatOps Bot - Detección de incidentes y automatización de Kanban

Bot automatizado que detecta incidentes en mensajes de commit, crea issues en GitHub y automatiza el movimiento de tarjetas en GitHub Projects.

---

**Videos:**

- Sprint 1: https://www.youtube.com/watch?v=65h376t44N4&list=PLGdRjQWXBasLTSmo3mB0D766WS9W7qYaZ&index=2
- Spront 2: https://www.youtube.com/watch?v=C56K48SYO8c&list=PLGdRjQWXBasLTSmo3mB0D766WS9W7qYaZ&index=1

### Detección Automática de Incidentes

- Detecta commits con formato `incident: [P0-P3] - Descripción`
- Extrae automáticamente severidad (P0=crítico, P3=menor)
- Normaliza espacios y valida formato

### Creación Automática de Issues

- Crea issues en GitHub con título y descripción estructurada
- Asigna labels automáticamente: `incident`, `P0`/`P1`/`P2`/`P3`

### Automatización de Tablero Kanban

- **New Issue:** Al crear issue desde commit con "incident:"
- **In Progress:** Al abrir un issue manualmente
- **Review/QA:** Al abrir PR con "Fixes #N" en descripción
- Race conditions manejadas con retry logic (3 intentos, delays de 2s)

### Patrones de Diseño

- **Facade:** Simplifica PyGithub (GitHubClient) y gh CLI (GitHubProjects)
- **Separation of Concerns:** Detección → Creación → Organización
- **Retry Logic:** Manejo robusto de race conditions en GitHub Projects API

---

## Arquitectura

```
PC03-DS/
├── bot/
│   ├── __init__.py
│   ├── main.py                 # CLI para testing local
│   ├── event_handlers.py       # Detector de incidentes (parser)
│   ├── github_client.py        # Facade de PyGithub (crea issues)
│   ├── github_projects.py      # Facade de gh CLI (mueve tarjetas)
│   └── config.py               # Configuración centralizada
│
├── tests/
│   ├── conftest.py
│   ├── test_event_handlers.py  # 26 tests parametrizados (95% coverage)
│   ├── test_integration.py     # Tests end-to-end
│   ├── test_github_client.py   # Tests con mocks de PyGithub
│   └── test_github_projects.py # Tests con mocks de subprocess
│
├── .github/
│   └── workflows/
│        ├── bot.yml                    # Detección + creación + "New Issue"
│        └── board-automation.yml       # "In Progress" + "Review/QA"
│
├── evidence/
│   ├── sprint-1/               # Reportes y capturas Sprint 1
│   └── sprint-2/               # Reportes y capturas Sprint 2
│
├── .env.example
├── requirements.txt
├── Makefile
└── README.md
```

---

## 🚀 Preparación del Proyecto

### Requisitos Previos

- **Python 3.10+** instalado
- **Git** instalado
- **gh CLI** (solo para testing local de github_projects.py)
- Cuenta de **GitHub** con permisos de administrador en el repositorio

### 1. Clonar el Repositorio

```bash
git clone https://github.com/pineda-404/PC03-DS.git
cd PC03-DS
```

### 2. Crear Entorno Virtual

**En Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
make install
```

**Dependencias principales:**

- `PyGithub==2.8.1` - Interacción con GitHub API
- `pytest==8.4.2` - Framework de testing
- `pytest-cov==7.0.0` - Reporte de cobertura
- `python-dotenv==1.2.1` - Manejo de variables de entorno
- `flake8==7.1.1` - Linting

---

## ⚙️ Configuración

### 1. Configurar Variables de Entorno

Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

Edita `.env` con tus valores:

```bash
# Token de GitHub "fine-grained" con permisos de Read & Write para Issues y Projects
# Ve a https://github.com/settings/tokens?type=beta para generar uno
GITHUB_TOKEN=ghp_tu_token_aqui

# (Opcional) Usuario y repositorio de GitHub
# Si no se especifican, se usarán los valores por defecto en bot/config.py
GITHUB_OWNER=tu-usuario
GITHUB_REPO=tu-repositorio
```

### 2. Crear Personal Access Token (PAT)

El bot necesita un **Fine-grained Personal Access Token** con los siguientes permisos:

1. Ve a [GitHub Settings > Tokens (beta)](https://github.com/settings/tokens?type=beta)
2. Click en **"Generate new token"**
3. Configura:

   - **Token name:** `CHATOPS_BOT_TOKEN`
   - **Expiration:** 90 días (o el que prefieras)
   - **Repository access:** Solo el repositorio del proyecto
   - **Permissions:**
     - ✅ **Issues:** Read and write
     - ✅ **Projects:** Read and write
     - ✅ **Contents:** Read and write
     - ✅ **Workflows:** Read and write

4. Copia el token generado y guárdalo en `.env`

**Importante:** El `GITHUB_TOKEN` automático de GitHub Actions **NO** tiene permisos de `project`. Debes usar un PAT.

### 3. Configurar Secrets en GitHub

Si usarás los workflows automáticos:

1. Ve a tu repositorio en GitHub
2. **Settings** > **Secrets and variables** > **Actions**
3. Click en **"New repository secret"**
4. Agrega:
   - **Name:** `CHATOPS_BOT_TOKEN`
   - **Secret:** Tu PAT generado en el paso anterior

### 4. Obtener Project ID (para github_projects.py)

El bot necesita el ID del proyecto para mover tarjetas. Este valor está **hardcodeado** en `bot/github_projects.py:27`.

Para obtener tu project_id:

```bash
# Instalar gh CLI (si no lo tienes)
# En Ubuntu/Debian:
sudo apt install gh

# Autenticarte
gh auth login

# Listar tus proyectos
gh project list --owner tu-usuario

# Ver detalles de un proyecto específico
gh project view NUMERO_PROYECTO --owner tu-usuario --format json | jq '.id'
```

Copia el ID (formato: `PVT_kwXXXXXXXXXXXX`) y actualiza `bot/github_projects.py`:

```python
def _ensure_project_metadata(self):
    if self._status_field_id:
        return

    # Hardcodeado - Actualiza con tu project_id
    self._project_id = "TU_PROJECT_ID_AQUI"
    # ...
```

---

## 💻 Uso

### Modo CLI (Testing Local)

Prueba la detección de incidentes localmente:

```bash
# Detectar incidente con severidad por defecto (P3)
make run MSG="incident: API timeout"

# Detectar incidente crítico (P0)
make run MSG="incident: P0 - Sistema caído"

# No es un incidente (debe fallar)
make run MSG="feat: nueva funcionalidad"
```

**Salida esperada:**

```bash
$ make run MSG="incident: P0 - Sistema caído"
[INFO] Incidente detectado:
✓ Título: Sistema caído
✓ Severidad: P0
```

### Formato de Commits

Para que el bot detecte un incidente, el commit debe seguir este formato:

```
incident: [P0-P3] - Descripción del problema
```

**Ejemplos válidos:**

```bash
git commit -m "incident: API timeout"                    # → P3 (default)
git commit -m "incident: P0 - Sistema caído"             # → P0 (crítico)
git commit -m "incident: P1 - Autenticación rota"        # → P1 (alto)
git commit -m "incident: P2 - Queries lentas"            # → P2 (medio)
git commit -m "incident:Cache miss"                      # → P3 (sin espacio)
```

**Ejemplos NO válidos:**

```bash
git commit -m "fix: corregir bug"              # No empieza con "incident:"
git commit -m "Incident: bug crítico"          # Mayúscula (case-sensitive)
git commit -m "incident:"                      # Sin descripción
git commit -m "incident: P0"                   # Sin título después de P0
```

### Severidades

| Código | Significado                     | Tiempo de respuesta esperado |
| ------ | ------------------------------- | ---------------------------- |
| **P0** | Crítico - Sistema caído         | Inmediato (<15 min)          |
| **P1** | Alto - Funcionalidad core rota  | <1 hora                      |
| **P2** | Medio - Degradación de servicio | <4 horas                     |
| **P3** | Bajo - Bug menor                | <24 horas                    |

---

## 🤖 Workflows Automáticos

### bot.yml - Detección y Creación

**Trigger:** `push` a branches `develop`, `main`, `feature/**`, `hotfix/**`, `fix/**`

**Flujo:**

1. Detecta mensaje de commit con `EventHandler`
2. Si contiene "incident:", crea issue con `GitHubClient`
3. Mueve tarjeta a columna "New Issue" con `GitHubProjects`
4. Genera summary markdown en Actions

**Ejemplo:**

```bash
git commit -m "incident: P1 - Auth broken"
git push origin develop

# → Bot detecta → Crea issue #42 → Mueve a "New Issue"
```

### board-automation.yml - Movimiento de Tarjetas

**Triggers:**

- `issues.opened` → Mueve a "In Progress"
- `pull_request.opened` → Detecta "Fixes #N" → Mueve a "Review/QA"

**Flujo de PR:**

```bash
# Crear branch y hacer cambios
git checkout -b fix/issue-42
# ... hacer cambios ...
git commit -m "fix: resolver autenticación rota"
git push origin fix/issue-42

# Crear PR con descripción que incluya "Fixes #42"
gh pr create --title "Fix: resolver issue 42" --body "Fixes #42"

# → Bot detecta "Fixes #42" → Mueve tarjeta #42 a "Review/QA"
```

---

## 🧪 Testing

### Ejecutar Todos los Tests

```bash
make test
```

📊 Reporte HTML generado en htmlcov/index.html

````

### Linting (Verificar Estilo)

```bash
make lint
````

### Limpiar Archivos Temporales

```bash
make clean
```

### Tests por Módulo

```bash
# Solo tests de event_handlers
pytest tests/test_event_handlers.py -v

# Solo tests de github_client
pytest tests/test_github_client.py -v

# Solo tests de github_projects
pytest tests/test_github_projects.py -v

# Solo tests de integración
pytest tests/test_integration.py -v
```

### Tests Parametrizados

Los tests usan `@pytest.mark.parametrize` para probar múltiples casos:

```python
@pytest.mark.parametrize(
    "commit_msg, expected_title, expected_severity",
    [
        ("incident: API timeout", "API timeout", "P3"),
        ("incident: P0 - System down", "System down", "P0"),
        ("incident: P1 - Auth broken", "Auth broken", "P1"),
        # ... 26 casos en total
    ],
)
def test_valid_incidents(handler, commit_msg, expected_title, expected_severity):
    result = handler.handle_commit(commit_msg)
    assert result["title"] == expected_title
    assert result["severity"] == expected_severity
```

---

## Decisiones de Diseño

### 1. Hardcodeo de `project_id`

**Ubicación:** `bot/github_projects.py:27`

**Problema:**

- `gh project view` falla en GitHub Actions con error de autenticación
- `gh project field-list` retorna metadata pero NO incluye `project_id`

**Alternativas evaluadas:**

| Alternativa  | Tiempo estimado | Pros               | Contras                                | Decisión         |
| ------------ | --------------- | ------------------ | -------------------------------------- | ---------------- |
| Hardcodear   | 5 min           | Simple, funciona   | No portable                            | ✅ **Elegida**   |
| GraphQL API  | 3-4 horas       | Elegante, dinámico | Complejidad alta, biblioteca adicional | ❌ Descartada    |
| Variable ENV | 30 min          | Configurable       | Usuario debe obtener ID manualmente    | 🔄 Futura mejora |

**Justificación:**

- El `project_id` es **estático** (no cambia a menos que elimines el proyecto)
- Prioridad en Sprint 2: funcionalidad sobre elegancia
- Documentado en código y README para futuros desarrolladores

**Cómo actualizar:**

```python
# bot/github_projects.py línea 27
self._project_id = "TU_NUEVO_PROJECT_ID"
```

### 2. Delays de 2 segundos en `github_projects.py`

**Ubicación:** `bot/github_projects.py:64, 77, 91`

**Problema:** Race conditions en GitHub Projects V2 API

- `gh project item-add` agrega item al proyecto
- `gh project item-list` NO lo encuentra inmediatamente (eventual consistency)
- Sin delay: ~40% de fallas intermitentes

**Solución:**

```python
gh project item-add ...
time.sleep(2)              # Delay para propagación

for attempt in range(3):   # Retry logic
    items = gh project item-list ...
    if found: break
    time.sleep(2)
```

**Valores probados:**

- `time.sleep(1)` → 20% de fallas
- `time.sleep(2)` → 0% de fallas en 20+ intentos ✅
- `time.sleep(3)` → 0% de fallas pero innecesariamente lento

**Futura mejora:** Variable de entorno `GH_PROJECTS_DELAY` con default 2.0

### 3. Patrón Facade

**Implementado en:**

- `bot/github_client.py` - Simplifica PyGithub
- `bot/github_projects.py` - Simplifica gh CLI

**Beneficios:**

```python
# Sin Facade (acoplado a PyGithub):
from github import Github
client = Github(token)
repo = client.get_repo(f"{owner}/{repo}")
issue = repo.create_issue(
    title=title,
    body=f"🚨 Incidente detectado\n\n**Severidad:** {severity}",
    labels=[severity, "incident"]
)

# Con Facade (abstracción limpia):
from bot.github_client import GitHubClient
client = GitHubClient(token, owner, repo)
issue_number = client.create_incident_issue(title, severity)
```

**Ventajas:**

- Workflows usan 1 línea en lugar de 10+
- Testing: mockear Facade es más simple que mockear PyGithub
- Fácil cambiar implementación sin afectar workflows

### 4. Sin `load_dotenv()` en producción

**Ubicación:** `bot/config.py`

**Decisión:** NO usar `load_dotenv()` en `config.py`

**Razón:**

- GitHub Actions inyecta variables de entorno directamente desde Secrets
- `load_dotenv()` buscaría archivo `.env` que no existe en Actions
- `.env` solo para desarrollo local

**Uso correcto:**

```python
# Desarrollo local
export $(cat .env | xargs)  # Cargar .env manualmente
python bot/main.py --commit-msg "incident: test"

# GitHub Actions
# Variables ya están en el entorno desde Secrets
# No necesita load_dotenv()
```

### Conventional Commits

```
tipo(scope): descripción corta

[cuerpo opcional]

[footer opcional: Fixes #123]
```

**Tipos:**

- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `test`: Agregar o modificar tests
- `refactor`: Refactorización sin cambio de funcionalidad
- `chore`: Cambios en build, CI, etc.

**Ejemplos:**

```bash
feat(github_client): add support for custom labels
fix(github_projects): resolve race condition with 2s delay
docs(readme): add installation instructions
test(event_handlers): add edge case for empty titles
```

---

## 📊 Reportes de Sprints

- [Sprint 1 - Parser y Tests Básicos](evidence/sprint-1/reporte-sprint-1.md)
- [Sprint 2 - Integración GitHub API y Projects](evidence/sprint-2/sprint-2-report.md)

---

## 📝 Licencia

Este proyecto es parte de un trabajo académico para el curso de Desarrollo de Software.

---

## 👥 Autores

- **@pineda-404** - Desarrollo principal, integración GitHub API
- **@MateoTorresFuero** - Configuración, testing, workflows

---

- **PyGithub** - Biblioteca para interactuar con GitHub API
- **gh CLI** - Herramienta oficial de GitHub para Projects V2
- **pytest** - Framework de testing robusto y flexible

---
