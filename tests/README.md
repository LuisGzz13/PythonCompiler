# Tests del compilador Patito (Python)

51 casos de prueba organizados en 6 carpetas, una por capa-y-resultado:

| Carpeta | Cuantos | Etapa | Exit code esperado |
|---|---|---|---|
| `valid/` | 14 | 1 (sintaxis) | `0` |
| `invalid/` | 10 | 1 (sintaxis) | `!= 0` |
| `semantic_valid/` | 4 | 2 (semantica) | `0` |
| `semantic_invalid/` | 8 | 2 (semantica) | `!= 0` |
| `cuadruplos_valid/` | 12 | 3 (codigo) | `0` |
| `cuadruplos_invalid/` | 3 | 3 (codigo) | `!= 0` |
| **Total** | **51** | | |

## Como correr

Desde la raiz del repo (`Patito-Python/`):

```bash
pytest -v                       # todo, una linea por test
pytest                          # vista resumida
pytest -v -k "sintaxis"         # solo Etapa 1
pytest -v -k "semantica"        # solo Etapa 2
pytest -v -k "cuadruplos"       # solo Etapa 3
pytest -x                       # se detiene al primer fallo
pytest --lf                     # solo los que fallaron antes
```

## Que esperar mientras avanzas

| Despues de Sesion | Tests que ya pasan |
|---|---|
| 1 (lexico + sintaxis) | 24 (valid/ + invalid/) |
| 4 (semantica) | 36 (+ semantic_valid/ + semantic_invalid/) |
| 5 (cuadruplos) | 51 (todos) |

No te preocupes si al inicio fallan los de Etapas 2 y 3 — es esperado.
