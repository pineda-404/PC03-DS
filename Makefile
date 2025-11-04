.PHONY: help install test lint coverage run clean

PYTHON := python3
PIP := $(PYTHON) -m pip

help: ## Mostrar comandos disponibles
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | \
	awk 'BEGIN{FS=":.*?##"}{printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Instalar dependencias
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencias instaladas"

test: ## Ejecutar tests
	PYTHONPATH=. pytest tests/ -v

coverage: ## Ejecutar tests con reporte de cobertura
	PYTHONPATH=. pytest tests/ -v --cov=bot --cov-report=term-missing --cov-report=html
	@echo "📊 Reporte HTML generado en htmlcov/index.html"

lint: ## Verificar estilo de código
	flake8 bot/ tests/ --exclude=__pycache__
	@echo "✅ Código cumple estándares"

run: ## Ejecutar bot en modo CLI
	@echo "Ejemplo: make run MSG='incident: Test bug'"
	@if [ -z "$(MSG)" ]; then \
		echo "❌ Error: Variable MSG requerida"; \
		echo "   Uso: make run MSG='incident: API timeout'"; \
		exit 1; \
	fi
	PYTHONPATH=. $(PYTHON) bot/main.py --commit-msg "$(MSG)"

clean: ## Limpiar archivos temporales
	rm -rf __pycache__ .pytest_cache .coverage htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	@echo "✅ Archivos temporales eliminados"
