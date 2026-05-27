# Patito — Compilador (Python)

Compilador para el lenguaje Patito, escrito en Python con ANTLR4 como generador
de lexer y parser. Es la migracion del compilador original en C++ (que vive en
el repo hermano `Patito/`), pensada para simplificar las Etapas 4 (control de
flujo) y 5 (maquina virtual).

## Stack

- **Python 3.9+** (probado con 3.9.20)
- **ANTLR 4.13.2** (la herramienta, instalada via Homebrew) — genera el lexer y parser
- **antlr4-python3-runtime 4.13.2** — runtime que usan los archivos generados
- **pytest 8.0.0** — suite de tests

## Setup inicial (una sola vez)

Desde la raiz del repo:

```bash
# 1. ANTLR (la herramienta, no el runtime de Python)
brew install antlr

# 2. Entorno virtual de Python
python3 -m venv .venv
source .venv/bin/activate

# 3. Dependencias de Python
pip install -r requirements.txt

# 4. Generar el lexer y parser desde la gramatica
( cd grammar && antlr -Dlanguage=Python3 -visitor Patito.g4 -o ../generated )
```

Cada vez que modifiques `grammar/Patito.g4` necesitas re-correr el paso 4.

### Por que `( cd grammar && ... )`

ANTLR espeja la subcarpeta del input dentro del output. Si corres
`antlr grammar/Patito.g4 -o generated` desde la raiz, ANTLR ve el input en
una subcarpeta `grammar/` y la replica, creando `generated/grammar/PatitoLexer.py`
(con un nivel extra que rompe los imports).

La solucion es entrar a `grammar/` primero: ahi adentro el input es solo
`Patito.g4` sin subcarpeta, asi que ANTLR no tiene nada que espejear y los
archivos caen directo en `generated/`. Los parentesis abren un sub-shell para
que el `cd` no afecte tu shell actual.

| Comando | Resultado |
|---|---|
| Parado en raiz: `antlr grammar/Patito.g4 -o generated` | `generated/grammar/PatitoLexer.py` ❌ |
| Parado en `grammar/`: `antlr Patito.g4 -o ../generated` | `generated/PatitoLexer.py` ✅ |

## Smoke test (verificar que ANTLR funciono)

Despues del setup, con el `.venv` activo, parado en la raiz:

```bash
python3 -c "
import sys; sys.path.insert(0, 'generated')
from antlr4 import FileStream, CommonTokenStream
from PatitoLexer import PatitoLexer
from PatitoParser import PatitoParser

stream = FileStream('tests/valid/01_minimo.patito')
lexer = PatitoLexer(stream)
tokens = CommonTokenStream(lexer)
parser = PatitoParser(tokens)
tree = parser.programa()
print('OK, raiz parseada:', tree.getText()[:60], '...')
"
```

Salida esperada:
```
OK, raiz parseada: programahola;inicio{}fin ...
```

Si esto imprime, la base esta lista — el lexer y parser de ANTLR pueden leer y
parsear tu lenguaje. Lo que sigue (analizador semantico, cubo, generador de
cuadruplos) es codigo que tu escribes en `patito.py` y `cubo.py`.

## Correr el compilador

```bash
python3 patito.py archivo.patito
```

Exit codes:
- `0` — programa valido (sintaxis + semantica + codigo generado sin errores)
- `!= 0` — al menos un error reportado a stderr

## Correr los tests

```bash
pytest -v                       # todos los tests, una linea por caso
pytest                          # vista resumida
pytest -v -k "sintaxis"         # solo Etapa 1
pytest -v -k "semantica"        # solo Etapa 2
pytest -v -k "cuadruplos"       # solo Etapa 3
pytest -x                       # se detiene al primer fallo
pytest --lf                     # solo los que fallaron antes
```

Ver `tests/README.md` para el detalle de las 6 suites y que esperar mientras
avanzas las sesiones.

## Estructura

```
patito-py/
├── README.md               este archivo
├── requirements.txt
├── .gitignore
├── grammar/
│   └── Patito.g4           gramatica ANTLR (input al generador)
├── generated/              autogenerado por ANTLR — no editar
│   ├── PatitoLexer.py
│   ├── PatitoParser.py
│   ├── PatitoListener.py
│   └── PatitoVisitor.py
├── patito.py               codigo del compilador (tablas, listener, codegen, main)
├── cubo.py                 cubo semantico (tabla de tipos)
├── tests/
│   ├── test_compiler.py    runner de pytest
│   ├── conftest.py
│   ├── README.md           explicacion de las 6 suites
│   └── {valid,invalid,semantic_valid,semantic_invalid,cuadruplos_valid,cuadruplos_invalid}/
│                           51 archivos .patito de fixtures
└── docs/                   documentacion por etapa (Markdown)
```

## Etapas del compilador

| Etapa | Que hace | Donde vive |
|---|---|---|
| 1 | Lexico + Sintaxis | autogenerado por ANTLR + driver minimo |
| 2 | Analisis semantico (tablas + cubo) | `patito.py` + `cubo.py` |
| 3 | Generacion de cuadruplos | `patito.py` |
| 4 | Control de flujo + llamadas | (pendiente) |
| 5 | Maquina virtual | (pendiente) |
