# 📄 Informe Final - Versión Estudiantes

```markdown
# Informe Final - Bot ChatOps para Gestión de Incidentes

**Curso:** Desarrollo de Software CC3S2  
**Equipo:** Diego Pineda Garcia+ Mateo Torres Fuero
**Fecha:** 15 de Noviembre 2025  
**Repositorio:** github.com/pineda-404/PC03-DS

---

## 1. Resumen del Proyecto

Desarrollamos un bot que automatiza la creación de issues y movimiento de tarjetas en GitHub Projects cuando detecta commits con formato `incident: [P0-P3] - título`.

**Resultados:**

- Bot funciona automáticamente en cada push
- Issues se crean con labels correctos
- Tarjetas se mueven solas entre columnas
- Tiempo de resolución mejoró de 45 min a 33 min

---

## 2. Arquitectura

### Estructura de archivos
```

bot/
├── event_handlers.py # Detecta incidentes en commits
├── github_client.py # Crea issues en GitHub
├── github_projects.py # Mueve tarjetas en el tablero
└── config.py # Variables de entorno

.github/workflows/
├── bot.yml # Action para crear issues
└── board-automation.yml # Action para mover tarjetas

````

### Patrones usados

**Facade:** Simplifica el uso de PyGithub y gh CLI. En vez de escribir 10 líneas para crear un issue, solo escribimos 1 línea.

**Mediator:** `EventHandler` coordina la detección sin que los workflows conozcan detalles del parser.

**DIP:** `Config` centraliza las variables de entorno para fácil testing.

---

## 3. Métricas

### Story points por sprint

- Sprint 1: 7 pts (parser + tests)
- Sprint 2: 8 pts (integración GitHub)
- Sprint 3: 10 pts (métricas + evidencias)
- **Total: 25 pts**

### Mejoras medibles

| Métrica | Sprint 2 | Sprint 3 | Cambio |
|---------|----------|----------|--------|
| MTTR | 45 min | 33 min | -27% |
| MTTA | 25 min | 20 min | -20% |

**MTTR** = tiempo desde que se crea el issue hasta que se cierra
**MTTA** = tiempo desde que se crea hasta primer comentario

### Cobertura de tests

- Global: 87% (objetivo era ≥85%)
- Total de tests: 61
- Todos los tests pasaron en CI

---

## 4. Problemas que Resolvimos

### Problema 1: Race conditions

**Qué pasaba:** Al agregar un issue al proyecto, a veces no aparecía inmediatamente en la lista.

**Solución:** Agregamos un delay de 2 segundos y retry logic (3 intentos).

```python
gh project item-add ...
time.sleep(2)  # Esperar que GitHub sincronice

# Intentar 3 veces si no lo encuentra
for attempt in range(3):
    items = gh project item-list ...
    if encontrado: break
    time.sleep(2)
````

### Problema 2: Permisos del token

**Qué pasaba:** El token automático `GITHUB_TOKEN` no tiene permisos para mover tarjetas.

**Solución:** Creamos un Personal Access Token con permisos `repo`, `project` y `workflow`.

### Problema 3: gh CLI no instalado

**Qué pasaba:** GitHub Actions no tiene `gh` CLI preinstalado.

**Solución:** Agregamos un step en el workflow para instalarlo.

---

## 5. Qué Aprendimos

### Lo bueno

- Los patrones de diseño sí ayudan (código más limpio)
- Tests parametrizados ahorran mucho tiempo
- Conventional Commits facilitan el historial
- La automatización reduce tiempo

### Lo difícil

- Race conditions tomaron 3 horas de debugging
- Hardcodear el `project_id` no nos gustó pero fue necesario

### Deuda técnica

- Falta implementar detección de tests fallidos (Issue #12)
- Faltan tests de `github_projects.py`
- Dashboard de métricas es estático (se genera manualmente)

---

---

## 6. Conclusión

Cumplimos todos los requisitos del examen:

- ✅ Bot detecta incidentes
- ✅ Crea issues automáticamente
- ✅ Mueve tarjetas por eventos
- ✅ Calcula métricas MTTA/MTTR
- ✅ Tests con cobertura ≥85%
