"""
Tests de CONTENIDO de los cuadruplos (Etapa 3).

A diferencia de test_compiler.py (que solo verifica exit codes via subproceso),
estos tests manejan el compilador PROGRAMATICAMENTE: compilan un string de codigo
y revisan la fila de cuadruplos generada. Asi verificamos que el codigo intermedio
sea CORRECTO, no solo que "no truene".

El helper compilar() usa InputStream (codigo en memoria, no archivo) y devuelve el
analizador para inspeccionar analizador.gen.fila y analizador.cte directamente.
Esto es exactamente lo que hara la VM de Etapa 5: consumir la fila.

Las direcciones se verifican por RANGO (no por valor exacto) para que el test sea
robusto y, de paso, compruebe la distribucion de direcciones virtuales:
  global entero 1000s | temporal entero 9000s | temporal bool 11000s | cte entera 13000s
"""

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


class _RaiseOnSyntaxError(ErrorListener):
    """Si el codigo de prueba tiene un error de sintaxis, fallar ruidosamente."""
    def syntaxError(self, recognizer, offendingSymbol, line, col, msg, e):
        raise SyntaxError(f"linea {line}:{col} {msg}")


def compilar(codigo):
    """
    Compila un string de codigo Patito y devuelve el SemanticAnalyzer.
    Inspecciona analizador.gen.fila (cuadruplos) y analizador.errores.
    Lanza SyntaxError si el codigo no parsea (para atrapar typos en los tests).
    """
    stream = InputStream(codigo)
    lexer = PatitoLexer(stream)
    lexer.removeErrorListeners()
    lexer.addErrorListener(_RaiseOnSyntaxError())

    tokens = CommonTokenStream(lexer)
    parser = PatitoParser(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(_RaiseOnSyntaxError())

    tree = parser.programa()
    analizador = SemanticAnalyzer()
    walker = ParseTreeWalker()
    walker.walk(analizador, tree)
    return analizador


def _ops(analizador):
    """Secuencia de operadores en la fila, en orden de emision."""
    return [q.op for q in analizador.gen.fila]


# ----------------------------------------------------------------------
# Grupo 1: precedencia y asociatividad
# ----------------------------------------------------------------------

def test_precedencia_mult_antes_de_suma():
    # a + b * c  ->  primero b*c, luego a+(b*c)
    # [1:] salta el GOTO-main que Etapa 4 emite en el indice 0 de todo programa.
    a = compilar("programa p; vars a, b, c, x : entero; inicio { x = a + b * c; } fin")
    assert _ops(a)[1:] == ["*", "+", "="]


def test_parentesis_cambian_precedencia():
    # (a + b) * c  ->  primero a+b, luego (a+b)*c
    a = compilar("programa p; vars a, b, c, x : entero; inicio { x = (a + b) * c; } fin")
    assert _ops(a)[1:] == ["+", "*", "="]


def test_asociatividad_izquierda():
    # 10 - 3 - 2  ->  (10-3)-2.  El temporal del 1er cuadruplo alimenta al 2do.
    # Con el GOTO-main en fila[0], el 1er '-' esta en fila[1] y el 2do en fila[2].
    a = compilar("programa p; vars x : entero; inicio { x = 10 - 3 - 2; } fin")
    fila = a.gen.fila
    assert _ops(a)[1:] == ["-", "-", "="]
    assert fila[2].opIzq == fila[1].resultado, "el 2do '-' debe operar sobre el temporal del 1ero"


# ----------------------------------------------------------------------
# Grupo 2: deduplicacion de constantes
# ----------------------------------------------------------------------

def test_dedup_letrero():
    a = compilar('programa p; inicio { escribe("hola"); escribe("mundo"); escribe("hola"); } fin')
    prints = [q.resultado for q in a.gen.fila if q.op == "PRINT"]
    assert prints[0] == prints[2], "el mismo letrero debe compartir direccion"
    assert prints[1] != prints[0], "letreros distintos, direcciones distintas"


def test_dedup_constante_entera():
    a = compilar("programa p; vars x : entero; inicio { x = 5; x = 5; } fin")
    asignaciones = [q for q in a.gen.fila if q.op == "="]
    assert len(asignaciones) == 2
    assert asignaciones[0].opIzq == asignaciones[1].opIzq, "la cte 5 debe reusar su direccion"


# ----------------------------------------------------------------------
# Grupo 3: distribucion de direcciones virtuales (por rango)
# ----------------------------------------------------------------------

def test_rangos_de_direcciones():
    a = compilar("programa p; vars g : entero; inicio { g = 1 + 2; } fin")
    suma = [q for q in a.gen.fila if q.op == "+"][0]
    asigna = [q for q in a.gen.fila if q.op == "="][0]
    assert 1000 <= asigna.resultado < 2000, "global entero -> 1000s"
    assert 9000 <= suma.resultado < 10000, "temporal entero -> 9000s"
    assert 13000 <= suma.opIzq < 14000, "constante entera -> 13000s"
    assert 13000 <= suma.opDer < 14000, "constante entera -> 13000s"


def test_temporal_relacional_es_bool():
    # el resultado de una comparacion vive en el rango bool (11000s)
    a = compilar("programa p; vars a, b : entero; inicio { escribe(a < b); } fin")
    comp = [q for q in a.gen.fila if q.op == "<"][0]
    assert 11000 <= comp.resultado < 12000, "temporal relacional (bool) -> 11000s"


# ----------------------------------------------------------------------
# Grupo 4: robustez del flujo
# ----------------------------------------------------------------------

def test_leak_no_contamina_estatuto_siguiente():
    # imp(a+1) deja un temporal en la pila (leak conocido de Etapa 3, sin PARAM aun).
    # El siguiente estatuto x=5 debe seguir asignando la CONSTANTE 5, sin contaminarse.
    src = (
        "programa p; vars a, x : entero; "
        "nula imp(n : entero) { { escribe(n); } } ; "
        "inicio { imp(a + 1); x = 5; } fin"
    )
    a = compilar(src)
    asigna_x = [q for q in a.gen.fila if q.op == "="][-1]
    assert a.errores == 0
    assert 1000 <= asigna_x.resultado < 2000, "x global -> 1000s"
    assert 13000 <= asigna_x.opIzq < 14000, "debe asignar la cte 5, NO el temporal del leak"


def test_var_no_declarada_un_solo_error_por_variable():
    # x = y + z  con y,z no declaradas: exactamente 2 errores (uno por var),
    # SIN un 3er error de "tipos incompatibles" en cascada.
    a = compilar("programa p; vars x : entero; inicio { x = y + z; } fin")
    assert a.errores == 2, "debe haber 1 error por cada var no declarada, sin cascada"


# ----------------------------------------------------------------------
# Grupo 5 (Etapa 4): control de flujo  (si / sino / mientras)
#   Los DESTINOS de los saltos se afirman estructuralmente (== indice del
#   cuadruplo a donde deben brincar), no con numeros adivinados.
# ----------------------------------------------------------------------

def _por_op(analizador, op):
    """Todos los cuadruplos con un operador dado, en orden de emision."""
    return [q for q in analizador.gen.fila if q.op == op]


def test_goto_main_en_el_indice_0():
    # Todo programa arranca con un GOTO que salta a 'main'.
    a = compilar("programa p; vars x : entero; inicio { x = 1; } fin")
    fila = a.gen.fila
    assert fila[0].op == "GOTO"
    assert fila[fila[0].resultado].op == "=", "el GOTO-main apunta al 1er cuadruplo de main"


def test_si_sin_sino_gotof_brinca_el_cuerpo():
    # si (1 > 0) { x = 1; } ;   ->  GOTOF salta al final del cuerpo.
    a = compilar("programa p; vars x : entero; inicio { si (1 > 0) { x = 1; } ; } fin")
    fila = a.gen.fila
    gotof = _por_op(a, "GOTOF")[0]
    assert _ops(a)[1:] == [">", "GOTOF", "="]
    assert gotof.resultado == len(fila), "GOTOF brinca a despues del cuerpo del si"
    assert a.errores == 0


def test_si_con_sino_dos_saltos():
    # si (1>0) { x=1; } sino { x=2; } ;  -> GOTOF al sino, GOTO brinca el sino.
    a = compilar(
        "programa p; vars x : entero; inicio { si (1 > 0) { x = 1; } sino { x = 2; } ; } fin")
    fila = a.gen.fila
    assert _ops(a)[1:] == [">", "GOTOF", "=", "GOTO", "="]
    gotof = _por_op(a, "GOTOF")[0]
    goto_brinca = _por_op(a, "GOTO")[-1]   # [0] es el GOTO-main
    assert fila[gotof.resultado].op == "=", "GOTOF -> 1er cuadruplo del sino (la asignacion x=2)"
    assert goto_brinca.resultado == len(fila), "GOTO -> despues del sino"
    assert a.errores == 0


def test_mientras_regresa_a_la_condicion():
    # mientras (x < 10) haz { x = x + 1; } ;
    a = compilar(
        "programa p; vars x : entero; inicio { mientras (x < 10) haz { x = x + 1; } ; } fin")
    fila = a.gen.fila
    idx_condicion = [i for i, q in enumerate(fila) if q.op == "<"][0]
    gotof = _por_op(a, "GOTOF")[0]
    goto_regreso = _por_op(a, "GOTO")[-1]
    assert goto_regreso.resultado == idx_condicion, "el GOTO final regresa a re-evaluar la condicion"
    assert gotof.resultado == len(fila), "el GOTOF sale del ciclo"
    assert a.errores == 0


def test_si_anidado_backpatch_lifo():
    # si externo con sino que contiene un si interno: los saltos no se cruzan.
    src = (
        "programa p; vars x, y : entero; "
        "inicio { si (x < 10) { si (x > 0) { y = x; } ; } sino { y = 0; } ; } fin"
    )
    a = compilar(src)
    assert a.errores == 0
    # 2 GOTOF (uno por cada si) y 2 GOTO (el GOTO-main + el brinco del sino externo).
    assert len(_por_op(a, "GOTOF")) == 2
    assert len(_por_op(a, "GOTO")) == 2


# ----------------------------------------------------------------------
# Grupo 6 (Etapa 4): llamada a funciones  (ERA / PARAM / GOSUB)
# ----------------------------------------------------------------------

_FUENTE_F = (
    "programa p; vars r : entero; "
    "nula f(a : entero) {{ {{ escribe(a); }} }} ; "
    "inicio {{ {cuerpo} }} fin"
)


def test_llamada_emite_era_param_gosub_en_orden():
    a = compilar(_FUENTE_F.format(cuerpo="f(7); r = 0;"))
    secuencia = [q.op for q in a.gen.fila if q.op in ("ERA", "PARAM", "GOSUB")]
    assert secuencia == ["ERA", "PARAM", "GOSUB"]
    assert a.errores == 0


def test_param_apunta_a_direccion_del_parametro_y_gosub_a_cuad_inicio():
    a = compilar(_FUENTE_F.format(cuerpo="f(7); r = 0;"))
    f = a.func_dir["f"]
    era = _por_op(a, "ERA")[0]
    param = _por_op(a, "PARAM")[0]
    gosub = _por_op(a, "GOSUB")[0]
    assert era.resultado == "f"
    assert param.resultado == f.params[0].direccion, "PARAM destino = direccion del parametro"
    assert gosub.resultado == f.cuad_inicio, "GOSUB salta al inicio del cuerpo de f"
    assert a.errores == 0


def test_endfunc_cierra_cada_funcion():
    a = compilar(_FUENTE_F.format(cuerpo="f(7); r = 0;"))
    assert len(_por_op(a, "ENDFUNC")) == 1, "una funcion declarada -> un ENDFUNC"


def test_funcion_tipada_como_factor_deja_temporal():
    # x = obtener() + 1   ->  el '+' opera sobre el temporal del retorno (9000s).
    src = (
        "programa p; vars x : entero; "
        "entero obtener() { { } } ; "
        "inicio { x = obtener() + 1; } fin"
    )
    a = compilar(src)
    suma = _por_op(a, "+")[0]
    assert 9000 <= suma.opIzq < 10000, "lado izq del + = temporal fantasma del retorno"
    assert a.errores == 0


def test_llamada_anidada_pasa_el_temporal_de_la_interna():
    # f(g())  con g:entero, f(a:entero).  f recibe el retorno de g.
    src = (
        "programa p; vars r : entero; "
        "entero g() { { } } ; "
        "nula f(a : entero) { { escribe(a); } } ; "
        "inicio { f(g()); r = 0; } fin"
    )
    a = compilar(src)
    assert a.errores == 0
    assert len(_por_op(a, "ERA")) == 2
    assert len(_por_op(a, "GOSUB")) == 2
    params = _por_op(a, "PARAM")
    assert len(params) == 1, "f recibe exactamente 1 argumento"
    assert 9000 <= params[0].opIzq < 10000, "el argumento de f es el temporal de g()"


# ----------------------------------------------------------------------
# Grupo 7 (Etapa 4): validaciones estrictas
# ----------------------------------------------------------------------

def test_args_de_mas_es_error():
    a = compilar(_FUENTE_F.format(cuerpo="f(1, 2); r = 0;"))
    assert a.errores >= 1, "demasiados argumentos debe ser error"


def test_args_de_menos_es_error():
    src = (
        "programa p; vars r : entero; "
        "nula f(a : entero, b : entero) { { escribe(a); } } ; "
        "inicio { f(1); r = 0; } fin"
    )
    a = compilar(src)
    assert a.errores >= 1, "faltan argumentos debe ser error"


def test_arg_tipo_estrechamiento_es_error():
    # pasar flotante a parametro entero -> error (estrechamiento prohibido)
    a = compilar(_FUENTE_F.format(cuerpo="f(3.5); r = 0;"))
    assert a.errores >= 1, "flotante a parametro entero debe ser error"


def test_arg_widening_entero_a_flotante_es_valido():
    src = (
        "programa p; vars r : entero; "
        "nula f(p : flotante) { { escribe(p); } } ; "
        "inicio { f(3); r = 0; } fin"
    )
    a = compilar(src)
    assert a.errores == 0, "entero a parametro flotante es valido (ensanchamiento)"


def test_condicion_no_bool_es_error():
    # si (x) con x entero: la condicion no es booleana -> error.
    a = compilar("programa p; vars x : entero; inicio { si (x) { x = 1; } ; } fin")
    assert a.errores >= 1, "condicion entera (no bool) debe ser error"


def test_condicion_aritmetica_no_bool_es_error():
    # mientras (x + 1) ...  -> entero, no bool -> error.
    a = compilar("programa p; vars x : entero; inicio { mientras (x + 1) haz { x = 1; } ; } fin")
    assert a.errores >= 1
