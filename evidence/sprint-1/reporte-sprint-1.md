# Reporte del Sprint 1

## 1. Sprint Review (Resumen Ejecutivo)

**Sprint Goal:** Implementar la detección básica de incidentes en commits y crear los tests respectivos  
**Duración:** 6 días (2025-11-02 a 2025-11-07)  
**Velocity:** 8 pts completados / 10 pts comprometidos (80%)

### Issues Completados

- [#2: Implementar parser de commits](https://github.com/pineda-404/PC03-DS/issues/2) - 3 pts
  - **Assignee:** @pineda-404
  - **Time to Done:** ~6 horas
  - **PRs:** Integrado directamente (sin PR formal en Sprint 1)
  - **Resultado:** Parser funcional que detecta "incident:" y extrae severidades P0-P3

- [#3: Tests parametrizados para parser](https://github.com/pineda-404/PC03-DS/issues/3) - 2 pts
  - **Assignee:** @pineda-404
  - **Time to Done:** ~4 horas
  - **PRs:** Integrado con #3
  - **Resultado:** 26 tests parametrizados con cobertura del 91%

- [#4: Prueba de CLI básico](https://github.com/pineda-404/PC03-DS/issues/4) - 2 pts
  - **Assignee:** @pineda-404
  - **Time to Done:** ~2 horas
  - **PRs:** Integrado
  - **Resultado:** CLI funcional con argparse, acepta --commit-msg

- [#5: Configurar Makefile inicial](https://github.com/pineda-404/PC03-DS/issues/5) - 1 pt
  - **Assignee:** @MateoTorresFuero
  - **Time to Done:** ~1 hora
  - **PRs:** [#1](https://github.com/pineda-404/PC03-DS/pull/1)
  - **Resultado:** Makefile con 6 targets: install, test, coverage, lint, run, clean

### Issues No Completados

- [#6: Documentar Sprint 1 y capturar evidencias](https://github.com/pineda-404/PC03-DS/issues/6) - 2 pts
  - **Razón:** En progreso, completándose al cierre del sprint
  - **Blocked Time:** 0 min
  - **Plan:** Completar con capturas, video y este reporte

### Links Importantes

- **Tablero:** [ChatOps - Tablero Kanban](https://github.com/users/pineda-404/projects/2)
- **Repositorio:** [PC03-DS](https://github.com/pineda-404/PC03-DS)
- **Burndown:** Ver `evidence/sprint-1/burndown-chart.png`
- **CI Status:** No configurado aún (Sprint 2)

---

## 2. Dailies (Proceso Diario)

### Daily - Día 1

**@pineda-404:**
- **Ayer:** Revisé las pautas del proyecto y creé la estructura del repositorio
- **Hoy:** Configurar estructura del proyecto (bot/, tests/), crear issues del Sprint 1
- **Bloqueos:** Ninguno

**@MateoTorresFuero:**
- **Ayer:** Revisé documentación de Makefile y pytest
- **Hoy:** Crear Makefile inicial con targets básicos
- **Bloqueos:** Ninguno

---

### Daily - Día 2

**@pineda-404:**
- **Ayer:** Estructura del proyecto creada, issues #1-5 creados en el tablero
- **Hoy:** Implementar parser básico que detecte "incident:" en commits
- **Bloqueos:** Configuración de venv en Ubuntu tomó más tiempo (problema con python vs python3)

**@MateoTorresFuero:**
- **Ayer:** Makefile creado con 6 targets funcionales
- **Hoy:** Probar todos los targets y crear PR
- **Bloqueos:** Ninguno

---

### Daily - Día 3

**@pineda-404:**
- **Ayer:** Parser básico funcionando, detecta "incident:" correctamente
- **Hoy:** Agregar extracción de severidades P0-P3 y normalización de espacios
- **Bloqueos:** Duda sobre cómo manejar múltiples espacios

---

### Daily - Día 4

**@pineda-404:**
- **Ayer:** Severidades P0-P3 implementadas, normalización de espacios funciona
- **Hoy:** Escribir tests parametrizados exhaustivos para el parser
- **Bloqueos:** Investigar cómo usar autospec correctamente

---

### Daily - Día 5

**@pineda-404:**
- **Ayer:** 26 tests parametrizados completados
- **Hoy:** CLI funcional
- **Bloqueos:** Ninguno

### Daily - Día 6

**@MateoTorresFuero:**
- **Ayer:** Revisar avance de los issues completados
- **Hoy:** Hacer la documentación del progreso respecto al sprint 1
- **Bloqueos:** Ninguno

---

## 3. Retrospectiva del Sprint

### 👍 Qué Salió Bien

1. **TDD desde el inicio:** Los tests parametrizados encontraron 3 bugs en edge cases:
   - Espacios vacíos después de "incident:"
   - Múltiples prioridades en un mismo mensaje
   - Normalización de espacios múltiples

2. **Cobertura alta:** Superamos el gate obligatorio de 85% sin problemas

3. **Makefile funcional desde día 2:** Automatización temprana facilitó el desarrollo
   - `make test` ejecutado ~50 veces durante desarrollo
   - `make coverage` usado para validar progreso

4. **Pair programming efectivo:** Aunque trabajamos por separado, coordinamos bien las tareas

5. **Estructura modular clara:** Separación bot/ y tests/ desde el inicio

### 👎 Qué Salió Mal

1. **Subestimamos configuración inicial:** 
   - Setup de Python (venv, python3 vs python)
   - Problema "externally-managed-environment" en Ubuntu

2. **Tablero Kanban no configurado correctamente:**
   - Custom fields (Estimate, Priority, Blocked Time) agregados tarde
   - Sin captura de Insights durante el desarrollo

3. **Sin GitHub Actions:** 
   - No implementamos CI automático en Sprint 1
   - Pruebas solo locales (sin validación en nube)

4. **Working solo en partes críticas:**
   - No hubo code review formal entre miembros del equipo
   - PRs creados pero sin proceso de aprobación establecido

5. **Flake8 warnings sin resolver:**
   - 8 warnings E501 (líneas >79 caracteres)
   - No crítico pero afecta calidad del código

### Qué Mejoraremos en Sprint 2

1. **Configurar custom fields ANTES del sprint:**
   - Estimate, Priority, Blocked Time, Sprint desde día 1
   - Capturar Insights diariamente para tener burndown real

2. **GitHub Actions como primera tarea:**
   - CI con lint + tests + cobertura como gate
   - Movimiento automático de tarjetas según eventos

3. **Process de PR más formal:**
   - Esperar 1 hora mínimo antes de merge (auto-review)
   - Usar checklist de PR para validar calidad

4. **Resolver warnings de flake8:**
   - Dividir líneas largas (PEP 8)
   - O configurar .flake8 con max-line-length=88

---

## 4. Deuda Técnica Generada

### 🟡 Media Prioridad

**1. Integración con GitHub API pendiente**
- **Ubicación:** `bot/github_client.py` (no existe aún)
- **Justificación:** Sprint 1 se enfocó en lógica de detección core
- **Impacto:** Bot no crea issues automáticamente todavía
- **Plan:** Primera tarea de Sprint 2 (5 pts)

**2. Sin manejo de errores de encoding**
- **Ubicación:** `bot/event_handlers.py`
- **Justificación:** Solo probamos commits en ASCII básico
- **Impacto:** Puede fallar con commits que contengan UTF-8 complejo o emojis
- **Plan:** Sprint 3, agregar tests parametrizados con diferentes encodings

**3. Warnings de flake8 (E501 - líneas largas)**
- **Ubicación:** `bot/main.py`, `tests/test_event_handlers.py`
- **Justificación:** Priorizamos funcionalidad sobre estilo en Sprint 1
- **Impacto:** 8 warnings (líneas >79 caracteres), no crítico pero afecta legibilidad
- **Plan:** Sprint 2, refactorizar líneas largas

### 🟢 Baja Prioridad

**4. CLI sin colores ni formato avanzado**
- **Ubicación:** `bot/main.py`
- **Justificación:** MVP funcional, sin tiempo para mejoras estéticas
- **Impacto:** Output básico, funciona pero no es "bonito"
- **Plan:** Sprint 3 si hay tiempo, usar librería como `rich` o `colorama`

**5. Sin tests de integración E2E**
- **Ubicación:** `tests/test_integration.py` (solo tiene tests unitarios agrupados)
- **Justificación:** Tests unitarios cubrieron casos críticos
- **Impacto:** No validamos flujo completo CLI → Parser → Output
- **Plan:** Sprint 2, agregar test E2E con subprocess

---

## 5. Métricas del Sprint

### Proceso

| Métrica           | Valor                    | Trend               | Observación |
| ----------------- | ------------------------ | ------------------- | ----------- |
| **Velocity**      | 8 pts / 10 pts (80%)     | N/A (primer sprint) | Conservador por setup inicial |
| **WIP**           | Máx 2 issues simultáneos | N/A                 | Solo 1-2 desarrolladores activos |
| **Cycle Time**    | ~5 horas promedio        | N/A                 | De "In Progress" a "Done" |
| **Lead Time**     | ~10 horas promedio       | N/A                 | De creación de issue a "Done" |
| **Blocked Time**  | 50 min total             | N/A                 | 20 min (espacios) + 30 min (autospec) |
| **Time to Merge** | N/A                      | N/A                 | Sin PRs formales aún (Sprint 2) |

### Calidad

| Métrica            | Valor                  | Trend               | Observación |
| ------------------ | ---------------------- | ------------------- | ----------- |
| **Cobertura**      | 91%                    | 📈 N/A (inicial)    | Supera gate de 85% |
| **Tests**          | 26 pasando, 0 fallando | N/A                 | Todos los casos críticos cubiertos |
| **Defect Density** | 0 bugs / 8 pts = 0     | N/A                 | Sin bugs post-testing |
| **Code Smells**    | 8 warnings (E501)      | ⚠️ Mejorar          | Líneas largas, no crítico |

### 📈 Insights (Capturas Adjuntas)

- **Status→Done:** 5 issues completados (ver `insights-done.png`)
- **Sum(Estimate):** 8 pts en Done (ver `insights-estimate.png`)
- **Burndown:** Líneas verde (Open) y morada (Completed) se cruzan en día 4 (ver `burndown-chart.png`)
  - Trabajo completado: 0→7 issues
  - Trabajo restante: 10→3 issues

---

## 6. Preparación para Sprint 2

### Issues Creados en Product Backlog

- [Implementar github_client.py (PyGithub)]
  - Crear issues automáticamente vía API
  - Asignar labels (incident, priority:PX)
  - Manejar autenticación con GITHUB_TOKEN

- [GitHub Action para automatización de tablero]
  - Detectar commits con "incident:"
  - Crear issue + mover tarjeta a In Progress
  - Workflow: on push → detectar → crear issue

- [Configurar GitHub Actions CI]
  - Workflow: lint + tests + coverage
  - Gate: cobertura ≥85% o falla
  - Badge en README

- [Tests E2E del flujo completo]
  - Subprocess para ejecutar CLI
  - Validar output esperado
  - Stubs de GitHub API

### Estimate Total Sprint 2: 12 pts

(Más ambicioso ahora que setup está completo, basado en velocity de 8 pts + capacidad extra)

### Riesgos Identificados

1. **PyGithub API desconocida**
   - **Mitigación:** Spike de 2 horas leyendo docs oficiales antes de estimar
   - **Plan B:** Usar `gh` CLI si API es muy compleja

2. **GitHub Actions con Projects V2**
   - **Mitigación:** Usar action oficial `actions/add-to-project@v0.5.0`
   - **Documentación:** https://github.com/actions/add-to-project

3. **Autenticación y secretos**
   - **Mitigación:** Usar GitHub Secrets para GITHUB_TOKEN
   - **Testing:** Crear repositorio de prueba privado

---

## 7. Definition of Done (Checklist)

Todos los issues completados cumplieron:

- [x] Código implementado y funcional
- [x] Tests con cobertura ≥90% del módulo
- [x] Tests pasando localmente (`make test`)
- [~] Tarjeta movida a "Done" en Projects ← **Completado al final del sprint**

---

## 8. Recursos y Evidencias

### 📂 Estructura de Evidencias

```
evidence/sprint-1/
├── insights-done.png           # Status por columna (Done destacado)
├── insights-estimate.png       # Sum(Estimate) por Status (8 pts en Done)
├── burndown-chart.png          # Trabajo Open (verde) vs Completed (morada)
├── tablero-final.png           # Vista Board del Kanban completo
└── reporte-sprint-1.md         # Este archivo
```

### 🔗 Links Útiles

- **Repositorio:** https://github.com/pineda-404/PC03-DS
- **Tablero Kanban:** https://github.com/users/pineda-404/projects/2
- **Issues Sprint 1:** #1, #2, #3, #4, #5, #6

---

**Fecha de cierre:** 2025-11-07  
**Attendees de Review:** @pineda-404, @MateoTorresFuero  
**Próximo Sprint Planning:** 2025-11-08 (Sprint 2: GitHub API + Actions)

---

## Apéndice: Comandos Útiles

```bash
# Setup
make install

# Desarrollo
make test
make coverage
make lint

# Probar bot
make run MSG="incident: P0 - Critical failure"
make run MSG="feat: add login"

# Limpieza
make clean
```

---
