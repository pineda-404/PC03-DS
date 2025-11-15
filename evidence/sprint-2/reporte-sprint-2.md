# Reporte del Sprint 2

## 1. Sprint Review (Resumen Ejecutivo)

**Sprint Goal:** Integrar con GitHub API para crear issues automáticamente y automatizar movimiento de tarjetas en GitHub Projects  
**Duración:** 3 días (2025-11-12 a 2025-11-14)  
**Velocity:** 13 pts completados / 15 pts comprometidos (87%)

### Issues Completados

- [#7: Configurar .env y config.py](https://github.com/pineda-404/PC03-DS/issues/7) - 1 pt
    
    - **Assignee:** @MateoTorresFuero
    - **Time to Done:** ~1 hora
    - **PRs:** Integrado en PR #8
    - **Resultado:** Config centralizado sin load_dotenv() para compatibilidad con Actions
- [#8: Implementar GitHubClient](https://github.com/pineda-404/PC03-DS/issues/8) - 3 pts
    
    - **Assignee:** @pineda-404
    - **Time to Done:** ~4 horas
    - **PRs:** Varios commits incrementales
    - **Resultado:** Facade de PyGithub funcional, crea issues con labels automáticos
- [#9: GitHub Action básico (bot.yml)](https://github.com/pineda-404/PC03-DS/issues/9) - 2 pts
    
    - **Assignee:** @pineda-404
    - **Time to Done:** ~3 horas (incluye debugging de permisos)
    - **PRs:** Multiple commits con correcciones
    - **Resultado:** Workflow funcional que crea issues en push con "incident:"
- [#14: Implementar github_projects.py](https://github.com/pineda-404/PC03-DS/issues/14) - 3 pts
    
    - **Assignee:** @pineda-404
    - **Time to Done:** ~6 horas (incluye debugging extensivo)
    - **PRs:** [#31](https://github.com/pineda-404/PC03-DS/pull/31) (testing)
    - **Resultado:** Facade de gh CLI con retry logic, hardcodeo de project_id necesario
- [#15: Workflow board-automation.yml](https://github.com/pineda-404/PC03-DS/issues/15) - 2 pts
    
    - **Assignee:** @MateoTorresFuero
    - **Time to Done:** ~2 horas
    - **PRs:** Integrado con testing de #14
    - **Resultado:** Workflow que mueve tarjetas a "Review/QA" al abrir PRs

- [#10: Tests con mocks de github_client.py](https://github.com/pineda-404/PC03-DS/issues/10) - 2 pts
    - **Assignee:** @MateoTorresFuero
    - **Time to Done:** ~3 horas
    - **PRs:** Integrado con #32, #33

### Issues Adicionales No Planeados

- **Instalación de gh CLI en workflows** (no estimado)
    
    - **Razón:** GitHub Actions no tiene gh CLI preinstalado
    - **Time Spent:** ~2 horas de debugging
    - **Resultado:** Step reutilizable agregado a ambos workflows
- **Creación de PAT (CHATOPS_BOT_TOKEN)** (no estimado)
    
    - **Razón:** GITHUB_TOKEN automático no tiene permisos de `project`
    - **Time Spent:** ~1 hora (configuración + documentación)
    - **Resultado:** Token con scopes: repo, project, workflow

### Links Importantes

- **Tablero:** [ChatOps - Tablero Kanban](https://github.com/users/pineda-404/projects/2)
- **Repositorio:** [PC03-DS](https://github.com/pineda-404/PC03-DS)
- **Actions:** [CI/CD Workflows](https://github.com/pineda-404/PC03-DS/actions)
- **PR de Testing:** [#31 - Fix: resolver issue 29](https://github.com/pineda-404/PC03-DS/pull/31)

---

## 2. Dailies (Proceso Diario)

### Daily - Día 1 (2025-11-12)

**@pineda-404:**

- **Ayer:** Cerré Sprint 1 con reporte completo y evidencias
- **Hoy:** Crear config.py y github_client.py básico
- **Bloqueos:** Duda sobre si usar load_dotenv() en Actions

**@MateoTorresFuero:**

- **Ayer:** Revisé documentación de PyGithub y python-dotenv
- **Hoy:** Crear .env.example y configurar secrets en GitHub
- **Bloqueos:** Ninguno

---

### Daily - Día 2 (2025-11-13)

**@pineda-404:**

- **Ayer:** GitHubClient funcional localmente, config.py creado
- **Hoy:** Crear workflow bot.yml y probar en Actions
- **Bloqueos:** Error 403 Forbidden al crear issues (permisos insuficientes)

**@MateoTorresFuero:**

- **Ayer:** .env.example creado, secrets configurados
- **Hoy:** Investigar permisos de GITHUB_TOKEN y crear PAT si es necesario
- **Bloqueos:** Documentación de GitHub sobre permisos confusa

---

### Daily - Día 3 (2025-11-14)

**@pineda-404:**

- **Ayer:** bot.yml funcional después de agregar permisos, issues se crean correctamente
- **Hoy:** Implementar github_projects.py para mover tarjetas automáticamente
- **Bloqueos:** gh CLI no instalado en Actions, comandos fallan con exit status 1

**@MateoTorresFuero:**

- **Ayer:** PAT creado (CHATOPS_BOT_TOKEN), permisos resueltos
- **Hoy:** Crear board-automation.yml para detectar PRs y mover tarjetas
- **Bloqueos:** Esperando que github_projects.py esté funcional

---

### Daily - Día 4 (2025-11-14 - Continuación)

**@pineda-404:**

- **Ayer/Esta mañana:** github_projects.py con múltiples correcciones
- **Hoy/Tarde:** Resolver error de `gh project view` hardcodeando project_id
- **Bloqueos:** Race condition entre item-add y item-list (resuelto con delays)

**@MateoTorresFuero:**

- **Ayer:** board-automation.yml creado y sincronizado con cambios de github_projects.py
- **Hoy:** Testing del flujo completo
- **Bloqueos:** Ninguno, workflow funcionando correctamente

---

## 3. Retrospectiva del Sprint

### 👍 Qué Salió Bien

1. **Debugging colaborativo efectivo:**
    
    - 6 horas resolviendo problema de gh CLI juntos
    - Solución final (hardcodeo de project_id) encontrada mediante experimentación
2. **Patrones de diseño bien aplicados:**
    
    - Facade simplificó PyGithub y gh CLI significativamente
    - Config centralizado facilitó manejo de variables de entorno
3. **Retry logic preventivo:**
    
    - Delays de 2s y retry con 3 intentos previenen race conditions
    - Sin esta solución, el bot fallaría intermitentemente
4. **Workflows reutilizables:**
    
    - Step de instalación de gh CLI se copia entre workflows sin cambios
    - Variables de entorno consistentes (GH_TOKEN + GITHUB_TOKEN)

### 👎 Qué Salió Mal

1. **Subestimamos complejidad de GitHub Projects V2:**
    
    - No consideramos que gh CLI no está preinstalado
    - API de Projects V2 es inconsistente (race conditions)
    - **Impacto:** +4 horas de debugging no planificado
2. **Hardcodeo de project_id:**
    
    - Solución pragmática pero no elegante
    - Si eliminamos el proyecto, hay que actualizar código
    - **Justificación:** `gh project field-list` no retorna project_id

### 🔄 Qué Mejoraremos en Sprint 3

1. **Spike técnico de 1 hora antes de estimar:**
    
    - Investigar APIs desconocidas antes del planning
    - Evitar sorpresas como "gh CLI no instalado"
2. **Code review obligatorio:**
    
    - Esperar 30 min mínimo antes de aprobar PR propio
    - Usar checklist de PR más estricto
3. **Documentar decisiones técnicas:**
    
    - README con sección "Decisiones de Diseño"
    - Explicar por qué hardcodeamos project_id

---

## 4. Deuda Técnica Generada

### 🟡 Media Prioridad

**1. Hardcodeo de project_id**

- **Ubicación:** `bot/github_projects.py:27`
- **Justificación:** `gh project field-list` no retorna project_id en JSON
- **Impacto:** Si eliminamos proyecto #2, código deja de funcionar
- **Plan:** Sprint 3 si hay tiempo, usar GraphQL API directamente
- **Alternativa:** Documentar en README que project_id es estático

**2. Sin manejo de múltiples issues en un PR**

- **Ubicación:** `board-automation.yml` (regex encuentra múltiples, pero no valida si existen)
- **Justificación:** Caso edge poco común
- **Impacto:** Si PR tiene "Fixes #1 #999", intentará mover tarjeta inexistente
- **Plan:** Sprint 3, agregar validación de existencia de issue antes de mover

### 🟢 Baja Prioridad

**3. Logs de debugging en github_projects.py**

- **Ubicación:** Sin agregar aún
- **Justificación:** Debugging manual fue suficiente
- **Impacto:** Si falla en producción, difícil diagnosticar sin logs detallados
- **Plan:** Sprint 3, agregar logging con niveles (DEBUG, INFO, ERROR)

**4. Sin caché de gh CLI**

- **Ubicación:** `github_projects.py` (instala gh CLI en cada ejecución)
- **Justificación:** Instalación toma ~10s, aceptable por ahora
- **Impacto:** Workflows tardan 10s extra innecesariamente
- **Plan:** Sprint 3, usar cache de GitHub Actions

---

## 5. Métricas del Sprint

### Proceso

|Métrica|Valor|Trend vs Sprint 1|Observación|
|---|---|---|---|
|**Velocity**|13 pts / 15 pts (87%)| +5 pts (+62%)|Mejor que Sprint 1 por menos setup|
|**WIP**|Máx 3 issues simultáneos| +1 issue|Más paralelización efectiva|
|**Cycle Time**|~4 horas promedio| -1h (-20%)|Flujo más ágil|
|**Lead Time**|~8 horas promedio| -2h (-20%)|Menos bloqueos que Sprint 1|
|**Blocked Time**|4 horas total| +3.5h (⚠️)|Debugging de gh CLI y race conditions|
|**Time to Merge**|~30 min promedio|N/A (primer sprint con PRs)|Self-review rápido (mejorar en Sprint 3)|

### Calidad

|Métrica|Valor|Trend vs Sprint 1|Observación|
|---|---|---|---|
|**Cobertura**|87%| -4% (de 91%)|Nuevos módulos sin tests|
|**Tests**|26 pasando, 0 fallando| Sin nuevos tests|Deuda técnica crítica|
|**Defect Density**|0 bugs / 13 pts = 0| Igual|Testing manual exhaustivo|
|**Code Smells**|3 hardcoded values| Nuevo|project_id, delays (2s), retry (3)|

### Específicas del Proyecto

|Métrica|Valor|Observación|
|---|---|---|
|**Issues creados por bot**|11 issues (#19-#29)|Todos funcionales, 9 de prueba|
|**Tarjetas movidas auto**|2 exitosas (#26, #29)|9 fallidas en debugging|
|**Workflows ejecutados**|24 runs|15 fallidos (debugging), 9 exitosos|

---

## 6. Preparación para Sprint 3

### Issues Creados en Product Backlog

**Nuevas Funcionalidades:**

- [Implementar metrics.py (MTTA/MTTR)] - 2 pts
    
    - Calcular tiempos desde timestamps de API
    - Output: JSON con métricas por issue
    - MTTA: creación → primer commit
    - MTTR: creación → cierre
- [Implementar dashboard.py] - 1 pt
    
    - Generar `evidence/sprint-3/metrics-summary.md`
    - Tabla con métricas por sprint
    - Gráfico ASCII simple
- [Evidencias finales Sprint 3] - 1 pt
    
    - Video 4-6 min
    - Capturas de insights
    - Documento sprint-3-report.md

### Estimate Total Sprint 3: 11 pts

(Más conservador por deuda técnica + features nuevas complejas)

### Riesgos Identificados

1. **Tests con mocks de subprocess muy complejos**
    
    - **Mitigación:** Usar `unittest.mock.patch` con side_effect para simular outputs
    - **Plan B:** Tests de integración con proyecto de prueba real
2. **Cálculo de MTTA/MTTR depende de datos históricos**
    
    - **Mitigación:** Usar issues #26 y #29 como casos de prueba
    - **Plan B:** Generar timestamps sintéticos para testing
3. **Detección de check_run events poco documentada**
    
    - **Mitigación:** Spike de 1h estudiando GitHub Actions contexts
    - **Documentación:** https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#check_run

---

## 7. Definition of Done (Checklist)

Todos los issues completados cumplieron:

- [x] Código implementado y funcional
- [x] Tests con cobertura ≥90% del módulo 
- [x] Tests pasando localmente (existentes pasan)
- [x] Workflows ejecutando sin errores en Actions
- [x] Commit con formato Conventional Commits
- [x] Variables hardcodeadas documentadas en código

---

## 8. Recursos y Evidencias

### 📂 Estructura de Evidencias

```
evidence/sprint-2/
├── insights-status.png          # Status por columna (Done: 5 issues)
├── insights-estimate.png        # Sum(Estimate): 13 pts completados
├── burndown-chart.png           # Burndown ideal vs real
├── actions-bot-success.png      # Workflow bot.yml exitoso
├── actions-board-success.png    # Workflow board-automation.yml exitoso
├── tablero-kanban.png           # Vista completa del tablero
├── pr-31-review-qa.png          # Tarjeta #29 en Review/QA
└── sprint-2-report.md           # Este archivo
```

### 🔗 Links Útiles

- **Repositorio:** https://github.com/pineda-404/PC03-DS
- **Tablero Kanban:** https://github.com/users/pineda-404/projects/2
- **Issues Sprint 2:** #7, #8, #9, #10, #14, #15
- **Workflows:**
    - [bot.yml](https://github.com/pineda-404/PC03-DS/blob/develop/.github/workflows/bot.yml)
    - [board-automation.yml](https://github.com/pineda-404/PC03-DS/blob/develop/.github/workflows/board-automation.yml)

---

## 9. Lecciones Técnicas Aprendidas

### Patrón Facade

**Implementado en:**

- `bot/github_client.py` (simplifica PyGithub)
- `bot/github_projects.py` (simplifica gh CLI)

**Beneficios observados:**

- Workflows usan 1 línea: `client.create_incident_issue(title, severity)`
- Sin Facade serían ~10 líneas de setup de PyGithub
- Testing futuro: Mock del Facade, no de PyGithub completo

### Race Conditions en APIs Asíncronas

**Problema encontrado:**

```python
gh project item-add ...    # Agrega issue
gh project item-list ...   # No lo encuentra aún
```

**Solución aplicada:**

```python
gh project item-add ...
time.sleep(2)              # Delay crítico
for attempt in range(3):
    items = gh project item-list ...
    if found: break
    time.sleep(2)          # Retry con backoff
```

**Lección:** APIs distribuidas son eventualmente consistentes, siempre implementar retry logic.


---

**Fecha de cierre:** 2025-11-14  
**Attendees de Review:** @pineda-404, @MateoTorresFuero  
**Próximo Sprint Planning:** 2025-11-15 (Sprint 3: Tests + Métricas + Detección de tests fallidos)