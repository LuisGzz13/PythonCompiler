"""
Suite de pruebas del compilador Patito (Python).

Cada test invoca `python patito.py archivo.patito` como subproceso y verifica:
  1. exit code esperado (0 para valido, != 0 para invalido)
  2. stderr esperado (vacio para valido, con al menos un error para invalido)

Esto cierra el hueco de que pytest solo veia exit codes y no se daba cuenta
si los mensajes de error salian bien (o si salia ruido en programas validos).
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
PATITO = ROOT / "patito.py"
TESTS = ROOT / "tests"


def _ejecutar(archivo: Path):
    """Corre el compilador y devuelve (exit_code, stdout, stderr)."""
    r = subprocess.run(
        [sys.executable, str(PATITO), str(archivo)],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return r.returncode, r.stdout, r.stderr


def _archivos(subdir: str):
    return sorted((TESTS / subdir).glob("*.patito"))


def _id(p: Path) -> str:
    return p.name


def _check_valido(archivo: Path):
    """Helper: programa valido debe salir 0 con stderr limpio."""
    code, _, stderr = _ejecutar(archivo)
    assert code == 0, f"esperado exit 0, hubo {code}. stderr: {stderr[:200]}"
    assert stderr.strip() == "", \
        f"esperado stderr vacio para programa valido, pero hubo: {stderr[:200]}"


def _check_invalido(archivo: Path):
    """Helper: programa invalido debe salir != 0 con al menos un error en stderr."""
    code, _, stderr = _ejecutar(archivo)
    assert code != 0, f"esperado exit != 0 para programa invalido"
    assert stderr.strip() != "", \
        f"programa invalido salio con exit {code} pero sin reportar error en stderr"


# ----------------------------------------------------------------------
# Etapa 1: Sintaxis
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("valid"), ids=_id)
def test_sintaxis_valida(archivo):
    _check_valido(archivo)


@pytest.mark.parametrize("archivo", _archivos("invalid"), ids=_id)
def test_sintaxis_invalida(archivo):
    _check_invalido(archivo)


# ----------------------------------------------------------------------
# Etapa 2: Semantica
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("semantic_valid"), ids=_id)
def test_semantica_valida(archivo):
    _check_valido(archivo)


@pytest.mark.parametrize("archivo", _archivos("semantic_invalid"), ids=_id)
def test_semantica_invalida(archivo):
    _check_invalido(archivo)


# ----------------------------------------------------------------------
# Etapa 3: Generacion de cuadruplos
# ----------------------------------------------------------------------
@pytest.mark.parametrize("archivo", _archivos("cuadruplos_valid"), ids=_id)
def test_cuadruplos_valida(archivo):
    _check_valido(archivo)


@pytest.mark.parametrize("archivo", _archivos("cuadruplos_invalid"), ids=_id)
def test_cuadruplos_invalida(archivo):
    _check_invalido(archivo)