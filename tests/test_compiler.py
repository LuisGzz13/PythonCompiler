"""
Suite de pruebas del compilador Patito (Python).

Cada test invoca `python patito.py archivo.patito` como subproceso y verifica el
exit code. Esto duplica el contrato del runner C++ (un programa valido sale con
0, uno con errores sale con != 0).

Las 6 carpetas representan las 3 capas del compilador, cada una con su variante
valida e invalida:

    valid/                 sintaxis OK    -> exit 0   (Etapa 1)
    invalid/               sintaxis FAIL  -> exit != 0 (Etapa 1)
    semantic_valid/        semantica OK   -> exit 0   (Etapa 2)
    semantic_invalid/      semantica FAIL -> exit != 0 (Etapa 2)
    cuadruplos_valid/      codigo OK      -> exit 0   (Etapa 3)
    cuadruplos_invalid/    codigo FAIL    -> exit != 0 (Etapa 3)

Mientras vas avanzando las sesiones, mas tests iran pasando:
    Sesion 1: pasan valid/, invalid/ (parser solo)
    Sesion 4: ademas semantic_valid/, semantic_invalid/
    Sesion 5: ademas cuadruplos_valid/, cuadruplos_invalid/

Uso:
    pytest -v                       # corre todo, output detallado
    pytest -v -k "sintaxis"         # solo tests de sintaxis (Etapa 1)
    pytest -v tests/test_compiler.py::test_cuadruplos_valid  # una sola suite
    pytest -x                       # se detiene al primer fallo
    pytest --lf                     # corre solo los que fallaron la vez pasada
"""

import subprocess
import sys
from pathlib import Path

import pytest

# ----------------------------------------------------------------------
# Localizacion de paths
# ----------------------------------------------------------------------
ROOT = Path(__file__).parent.parent          # carpeta Patito-Python/
PATITO = ROOT / "patito.py"                  # el compilador
TESTS = ROOT / "tests"                       # carpeta de fixtures


def _ejecutar(archivo: Path) -> int:
    """Corre el compilador contra `archivo` y devuelve el exit code."""
    r = subprocess.run(
        [sys.executable, str(PATITO), str(archivo)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return r.returncode


def _archivos(subdir: str) -> list[Path]:
    """Devuelve la lista ordenada de .patito en la subcarpeta."""
    return sorted((TESTS / subdir).glob("*.patito"))


def _id(p: Path) -> str:
    """ID legible que aparece en la salida de pytest (ej. '01_minimo.patito')."""
    return p.name


# ----------------------------------------------------------------------
# Etapa 1: Sintaxis
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("valid"), ids=_id)
def test_sintaxis_valida(archivo):
    """Programas sintacticamente correctos: el compilador debe aceptar (exit 0)."""
    assert _ejecutar(archivo) == 0, f"se esperaba exit 0 para {archivo.name}"


@pytest.mark.parametrize("archivo", _archivos("invalid"), ids=_id)
def test_sintaxis_invalida(archivo):
    """Programas con errores de sintaxis: el compilador debe rechazar (exit != 0)."""
    assert _ejecutar(archivo) != 0, f"se esperaba exit != 0 para {archivo.name}"


# ----------------------------------------------------------------------
# Etapa 2: Semantica
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("semantic_valid"), ids=_id)
def test_semantica_valida(archivo):
    """Sintaxis y semantica correctas: el compilador debe aceptar (exit 0)."""
    assert _ejecutar(archivo) == 0, f"se esperaba exit 0 para {archivo.name}"


@pytest.mark.parametrize("archivo", _archivos("semantic_invalid"), ids=_id)
def test_semantica_invalida(archivo):
    """Errores semanticos (variables/funciones duplicadas, etc.): exit != 0."""
    assert _ejecutar(archivo) != 0, f"se esperaba exit != 0 para {archivo.name}"


# ----------------------------------------------------------------------
# Etapa 3: Generacion de cuadruplos
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("cuadruplos_valid"), ids=_id)
def test_cuadruplos_valida(archivo):
    """Programas que generan codigo correctamente: exit 0."""
    assert _ejecutar(archivo) == 0, f"se esperaba exit 0 para {archivo.name}"


@pytest.mark.parametrize("archivo", _archivos("cuadruplos_invalid"), ids=_id)
def test_cuadruplos_invalida(archivo):
    """Errores en expresiones (var no declarada, tipos incompatibles, etc.): exit != 0."""
    assert _ejecutar(archivo) != 0, f"se esperaba exit != 0 para {archivo.name}"
