# Métricas Simuladas Sprint 3

## Tabla de Issues con Métricas

| Issue | Título                          | Severity | Created | First Fix | Closed  | MTTA (min) | MTTR (min) |
| ----- | ------------------------------- | -------- | ------- | --------- | ------- | ---------- | ---------- |
| #49   | Cache timeout en producción     | P1       | 6:07 AM | 6:27 AM   | 6:47 AM | 20         | 40         |
| #39   | Timeout de API de autenticación | P2       | 5:20 AM | 5:45 AM   | 6:00 AM | 25         | 40         |
| #51   | Typo en documentación README    | P3       | 5:50 AM | 6:05 AM   | 6:10 AM | 15         | 20         |

---

## Promedios Sprint 3

```
MTTA promedio = (20 + 25 + 15) / 3 = 20 minutos
MTTR promedio = (40 + 40 + 20) / 3 = 33.3 minutos
```

---

## Métricas por Severidad

| Severidad | Count | MTTA Avg | MTTR Avg |
| --------- | ----- | -------- | -------- |
| P1        | 1     | 20 min   | 40 min   |
| P2        | 1     | 25 min   | 40 min   |
| P3        | 1     | 15 min   | 20 min   |

---

## Tendencias Sprint 2 vs Sprint 3

| Métrica         | Sprint 2 | Sprint 3 | Cambio |
| --------------- | -------- | -------- | ------ |
| MTTA promedio   | 25 min   | 20 min   | -20%   |
| MTTR promedio   | 45 min   | 33 min   | -27%   |
| Issues cerrados | 2        | 3        | +50%   |
| Velocity        | 8 pts    | 10 pts   | +25%   |

---

## Conclusiones

- **Mejora en MTTA:** Reducción del 20% indica respuesta más rápida
- **Mejora en MTTR:** Reducción del 27% demuestra mayor eficiencia en resolución
- **Throughput aumentó:** 50% más issues resueltos
- **P3 más rápido:** Issues de baja prioridad se resuelven en la mitad del tiempo

---
