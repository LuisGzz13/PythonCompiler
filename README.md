# Patito — Compilador (Python)

Compilador para el lenguaje Patito escrito en Python, con ANTLR4 como generador
del lexer y parser. Incluye análisis sintáctico, semántico, generación de
código intermedio (cuádruplos) y una máquina virtual que ejecuta el código.

---

## 🚀 Setup inicial (una sola vez)

Desde la raíz del repo:

```bash
# 1. Crear entorno virtual de Python
python3 -m venv .venv

# 2. Activar el entorno virtual
source .venv/bin/activate

# 3. Instalar las dependencias
pip install -r requirements.txt
```

**Listo.** El compilador ya puede compilar y ejecutar programas Patito.

> 💡 Cada vez que abras una nueva terminal para trabajar con el proyecto,
> recuerda activar el entorno virtual: `source .venv/bin/activate`

---

## 🦆 Cómo ejecutar un programa Patito

### Ejecución básica (solo compilar)

```bash
python3 patito.py archivo.patito
```

Verifica sintaxis + semántica + genera cuádruplos. Si todo está bien, sale con
exit code `0`. Si hay errores, los reporta a `stderr` con exit code `1`.

### Las 3 flags útiles

| Flag | Qué hace |
|---|---|
| `--ejecutar` | Compila y **ejecuta** el programa en la máquina virtual |
| `--cuadruplos` | Imprime los cuádruplos generados (código intermedio) |
| `--dir` | Imprime el directorio de funciones (`func_dir`) |

### Ejemplos

**Ejecutar un programa:**

```bash
python3 patito.py --ejecutar tests/valid/31_pelos.patito
```

**Ver los cuádruplos antes de ejecutar:**

```bash
python3 patito.py --cuadruplos tests/valid/31_pelos.patito
```

**Ver el directorio de funciones:**

```bash
python3 patito.py --dir tests/valid/31_pelos.patito
```

**Combinar todas las flags** (muy útil para entender un programa end-to-end):

```bash
python3 patito.py --cuadruplos --dir --ejecutar tests/valid/31_pelos.patito
```

> 💡 Las flags pueden ir en cualquier orden y mezclarse libremente.

---

## 🧪 Correr los tests

Con el entorno virtual activo:

```bash
pytest -q                 # vista resumida (recomendado)
pytest -v                 # vista detallada, una línea por test
pytest -x                 # se detiene al primer fallo
pytest --lf               # solo corre los que fallaron la última vez
```

---

## 🔧 Regenerar ANTLR (solo si modificas `grammar/Patito.g4`)

Esto **no se necesita** para correr el compilador — los archivos generados ya
están en `generated/`. Solo es necesario si cambias la gramática.

**Instalar ANTLR** (una sola vez):

```bash
brew install antlr
```

**Regenerar** después de modificar la gramática:

```bash
( cd grammar && antlr -Dlanguage=Python3 -visitor Patito.g4 -o ../generated )
```

> 💡 Los paréntesis abren un sub-shell para que el `cd` no afecte tu shell.
> El `cd grammar` es necesario para que ANTLR no espeje la subcarpeta.

---

## 📦 Estructura del proyecto

```
patito-py/
├── patito.py                  # Driver / CLI
├── cubo.py                    # Cubo semántico de tipos
├── cuadruplos.py              # Cuádruplos + generador
├── semantico.py               # Analizador semántico + PNs
├── vm.py                      # Máquina virtual
├── grammar/Patito.g4          # Gramática ANTLR
├── generated/                 # Archivos generados por ANTLR
├── tests/                     # Suite de tests (pytest)
└── requirements.txt           # Dependencias Python
```
