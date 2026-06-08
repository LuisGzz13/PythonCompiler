"""
Tests de la Maquina Virtual (Etapa 5).

Mientras test_codegen.py verifica que el codigo intermedio sea correcto,
estos tests verifican que la VM produzca el COMPORTAMIENTO correcto al
ejecutar programas Patito completos.

Usa capsys (fixture de pytest) para capturar stdout. Cada 'escribe(a, b)'
emite 2 PRINTs separados (uno por impElem), asi que cada elemento queda en
SU PROPIA LINEA. Los tests asumen ese formato.
"""

import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "generated"))
sys.path.insert(0, str(ROOT))

from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from PatitoLexer import PatitoLexer
from PatitoParser import PatitoParser
from semantico import SemanticAnalyzer
from vm import MaquinaVirtual


class _RaiseOnSyntaxError(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, col, msg, e):
        raise SyntaxError(f"linea {line}:{col} {msg}")


def correr(codigo):
    """Compila y ejecuta un string de Patito. stdout queda en capsys."""
    lex = PatitoLexer(InputStream(codigo))
    lex.removeErrorListeners()
    lex.addErrorListener(_RaiseOnSyntaxError())
    parser = PatitoParser(CommonTokenStream(lex))
    parser.removeErrorListeners()
    parser.addErrorListener(_RaiseOnSyntaxError())
    analizador = SemanticAnalyzer()
    ParseTreeWalker().walk(analizador, parser.programa())
    if analizador.errores > 0:
        raise RuntimeError(f"errores de compilacion: {analizador.errores}")
    MaquinaVirtual(analizador).ejecutar()


def _lineas(capsys):
    """Devuelve stdout como lista de lineas (sin newlines vacios al final)."""
    return capsys.readouterr().out.strip().split("\n")


# ======================================================================
# Grupo 1: Programas simples (aritmetica, prints)
# ======================================================================

def test_hello_world(capsys):
    correr('programa p; inicio { escribe("hola mundo"); } fin')
    assert _lineas(capsys) == ["hola mundo"]


def test_aritmetica_precedencia(capsys):
    # 2 + 3*4 = 14 (no 20, que seria con asociatividad incorrecta)
    correr('programa p; vars x : entero; inicio { x = 2 + 3 * 4; escribe(x); } fin')
    assert _lineas(capsys) == ["14"]


def test_division_entera_trunca(capsys):
    # 10 / 3 = 3 (no 3.33). Coherente con el cubo: int/int -> int.
    correr('programa p; vars x : entero; inicio { x = 10 / 3; escribe(x); } fin')
    assert _lineas(capsys) == ["3"]


def test_division_flotante(capsys):
    correr('programa p; vars x : flotante; inicio { x = 10.0 / 4.0; escribe(x); } fin')
    assert _lineas(capsys) == ["2.5"]


def test_signo_unario_negativo(capsys):
    correr('programa p; vars x : entero; inicio { x = -5; escribe(x); } fin')
    assert _lineas(capsys) == ["-5"]


# ======================================================================
# Grupo 2: Control de flujo
# ======================================================================

def test_si_toma_rama_verdadera(capsys):
    correr("""
        programa p; vars x : entero;
        inicio {
            x = 5;
            si (x > 0) { escribe("positivo"); } sino { escribe("negativo"); } ;
        } fin
    """)
    assert _lineas(capsys) == ["positivo"]


def test_si_toma_rama_falsa(capsys):
    correr("""
        programa p; vars x : entero;
        inicio {
            x = -5;
            si (x > 0) { escribe("positivo"); } sino { escribe("negativo"); } ;
        } fin
    """)
    assert _lineas(capsys) == ["negativo"]


def test_mientras_suma_1_a_5(capsys):
    # 1+2+3+4+5 = 15
    correr("""
        programa p; vars i, s : entero;
        inicio {
            i = 1; s = 0;
            mientras (i < 6) haz { s = s + i; i = i + 1; } ;
            escribe(s);
        } fin
    """)
    assert _lineas(capsys) == ["15"]


def test_mientras_no_entra_si_falso_inicial(capsys):
    correr("""
        programa p; vars i : entero;
        inicio {
            i = 0;
            mientras (i < 0) haz { escribe("dentro"); } ;
            escribe("fin");
        } fin
    """)
    assert _lineas(capsys) == ["fin"]


def test_si_anidado_dentro_de_mientras(capsys):
    # Imprime "par" o "impar" para i = 1..4. Por mitad simple: si i < 3 par.
    correr("""
        programa p; vars i : entero;
        inicio {
            i = 1;
            mientras (i < 5) haz {
                si (i < 3) { escribe("baja"); } sino { escribe("alta"); } ;
                i = i + 1;
            } ;
        } fin
    """)
    assert _lineas(capsys) == ["baja", "baja", "alta", "alta"]


# ======================================================================
# Grupo 3: Llamadas a funciones
# ======================================================================

def test_llamada_simple_con_param(capsys):
    correr("""
        programa p; vars n : entero;
        nula saludar(x : entero) { { escribe("hola ", x); } } ;
        inicio { n = 42; saludar(n); } fin
    """)
    assert _lineas(capsys) == ["hola ", "42"]


def test_llamada_no_corrompe_memoria_del_caller(capsys):
    # CRITICO: h tiene local 'a' en 5000; f tiene parametro 'y' tambien en 5000.
    # Si PARAM usara escribir() en lugar de escribir_en_prep(), f pisaria
    # la 'a' de h. La regla "PARAM lee caller, escribe callee" lo previene.
    correr("""
        programa p; vars r : entero;
        nula f(y : entero) { { escribe("f: ", y); } } ;
        nula h(a : entero) { { f(a); escribe("h despues: ", a); } } ;
        inicio { h(7); } fin
    """)
    assert _lineas(capsys) == ["f: ", "7", "h despues: ", "7"]


def test_llamada_anidada_f_de_g(capsys):
    # f(g(...)) verifica que pila_prep funcione como PILA (regla 3 del advisor).
    # Como g no tiene retorno real (limitacion documentada), el temp llega
    # como 0 (default del Frame). Esto NO es bug — confirma que degrada limpio.
    correr("""
        programa p;
        entero g(x : entero) { { escribe("en g"); } } ;
        nula f(y : entero) { { escribe("en f: ", y); } } ;
        inicio { f(g(7)); } fin
    """)
    assert _lineas(capsys) == ["en g", "en f: ", "0"]


def test_dos_funciones_distintas_no_se_pisan_locales(capsys):
    # Las dos funciones tienen sus parametros en 5000, pero corren en frames
    # distintos, asi que nunca se pisan.
    correr("""
        programa p;
        nula a(n : entero) { { escribe("a=", n); } } ;
        nula b(m : entero) { { escribe("b=", m); } } ;
        inicio { a(1); b(2); a(3); } fin
    """)
    assert _lineas(capsys) == ["a=", "1", "b=", "2", "a=", "3"]


# ======================================================================
# Grupo 4: Recursion (verifica la pila de frames)
# ======================================================================

def test_recursion_directa_con_caso_base(capsys):
    # contar(3) imprime 3, 2, 1 (recursion descendente con caso base).
    correr("""
        programa p;
        nula contar(n : entero) {
            {
                escribe(n);
                si (n > 1) { contar(n - 1); } ;
            }
        } ;
        inicio { contar(3); } fin
    """)
    assert _lineas(capsys) == ["3", "2", "1"]


def test_recursion_infinita_se_detiene_con_stack_overflow():
    # Sin caso base -> excede el limite de 1000 frames -> RuntimeError.
    with pytest.raises(RuntimeError, match="stack overflow"):
        correr("""
            programa p;
            nula loop(n : entero) { { loop(n); } } ;
            inicio { loop(1); } fin
        """)


# ======================================================================
# Grupo 5: Errores en runtime
# ======================================================================

def test_division_por_cero_constante():
    with pytest.raises(RuntimeError, match="division por cero"):
        correr("programa p; vars x : entero; inicio { x = 10 / 0; } fin")


def test_division_por_cero_via_variable():
    with pytest.raises(RuntimeError, match="division por cero"):
        correr("""
            programa p; vars x, y : entero;
            inicio { x = 0; y = 10 / x; } fin
        """)


# ======================================================================
# Grupo 6: Integracion CLI (--ejecutar)
# ======================================================================

PATITO = ROOT / "patito.py"


def test_cli_ejecutar_demo_corre_correctamente():
    archivo = ROOT / "tests" / "valid" / "15_ejecutar_demo.patito"
    r = subprocess.run(
        [sys.executable, str(PATITO), "--ejecutar", str(archivo)],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 0
    assert r.stderr == ""
    # 3 iteraciones de "i = " + 1, 2, 3
    lineas = r.stdout.strip().split("\n")
    assert lineas == ["i = ", "1", "i = ", "2", "i = ", "3"]


def test_cli_runtime_error_sale_con_exit_1(tmp_path):
    # Division por cero al ejecutar -> exit 1 + mensaje en stderr.
    archivo = tmp_path / "divcero.patito"
    archivo.write_text("programa p; vars x : entero; inicio { x = 10 / 0; } fin")
    r = subprocess.run(
        [sys.executable, str(PATITO), "--ejecutar", str(archivo)],
        capture_output=True, text=True, timeout=10,
    )
    assert r.returncode == 1
    assert "division por cero" in r.stderr

# ======================================================================
# Grupo 7: Escribe bool imprime 0 o 1
# ======================================================================

    
def test_escribe_bool_imprime_0_o_1(capsys):
    correr('programa p; vars a, b : entero; inicio { a = 5; b = 3; escribe(a > b); escribe(a < b); } fin')
    assert _lineas(capsys) == ["1", "0"]


# ======================================================================
# Grupo 8: Retorno de funciones tipadas (retorna)
# ======================================================================

def test_retorna_funcion_simple_entero(capsys):
    """Funcion tipada entero que retorna x*2."""
    correr('''
        programa p; vars r : entero;
        entero doble(x : entero) { { retorna x * 2; } } ;
        inicio { r = doble(7); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["14"]


def test_retorna_funcion_simple_flotante(capsys):
    """Funcion tipada flotante que retorna a/b."""
    correr('''
        programa p; vars r : flotante;
        flotante division(a : flotante, b : flotante) { { retorna a / b; } } ;
        inicio { r = division(15.0, 4.0); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["3.75"]


def test_retorna_recursion_factorial(capsys):
    """factorial(5) = 120 — recursion directa con retorna."""
    correr('''
        programa p; vars r : entero;
        entero factorial(n : entero) {
            {
                si (n == 0) { retorna 1; } ;
                retorna n * factorial(n - 1);
            }
        } ;
        inicio { r = factorial(5); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["120"]


def test_retorna_fibonacci(capsys):
    """fib(10) = 55 — recursion DOBLE (rama 2 con 2 llamadas), prueba estres."""
    correr('''
        programa p; vars r : entero;
        entero fib(n : entero) {
            {
                si (n == 0) { retorna 0; } ;
                si (n == 1) { retorna 1; } ;
                retorna fib(n - 1) + fib(n - 2);
            }
        } ;
        inicio { r = fib(10); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["55"]


def test_retorna_llamada_anidada(capsys):
    """doble(triple(5)) = 30 — anidacion con dos retornos diferentes."""
    correr('''
        programa p; vars r : entero;
        entero doble(x : entero) { { retorna x * 2; } } ;
        entero triple(y : entero) { { retorna y * 3; } } ;
        inicio { r = doble(triple(5)); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["30"]


def test_retorna_misma_funcion_dos_veces(capsys):
    """doble(2) + doble(3) = 10 — misma funcion con dos call sites distintos."""
    correr('''
        programa p; vars r : entero;
        entero doble(x : entero) { { retorna x * 2; } } ;
        inicio { r = doble(2) + doble(3); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["10"]


def test_retorna_early_exit_en_si(capsys):
    """retorna dentro de si termina la funcion antes — no llega al retorna final."""
    correr('''
        programa p; vars r : entero;
        entero absoluto(x : entero) {
            {
                si (x < 0) {
                    retorna 0 - x;
                } ;
                retorna x;
            }
        } ;
        inicio {
            r = absoluto(-7);
            escribe(r);
            r = absoluto(7);
            escribe(r);
        } fin
    ''')
    assert _lineas(capsys) == ["7", "7"]


def test_retorna_entero_a_flotante_ensancha(capsys):
    """retorna entero en funcion flotante — cubo permite ensanchamiento int->float."""
    correr('''
        programa p; vars r : flotante;
        flotante mitad(x : entero) { { retorna x; } } ;
        inicio { r = mitad(42); escribe(r); } fin
    ''')
    assert _lineas(capsys) == ["42"]