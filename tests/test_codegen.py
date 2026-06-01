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
    a = compilar("programa p; vars a, b, c, x : entero; inicio { x = a + b * c; } fin")
    assert _ops(a) == ["*", "+", "="]


def test_parentesis_cambian_precedencia():
    # (a + b) * c  ->  primero a+b, luego (a+b)*c
    a = compilar("programa p; vars a, b, c, x : entero; inicio { x = (a + b) * c; } fin")
    assert _ops(a) == ["+", "*", "="]


def test_asociatividad_izquierda():
    # 10 - 3 - 2  ->  (10-3)-2.  El temporal del 1er cuadruplo alimenta al 2do.
    a = compilar("programa p; vars x : entero; inicio { x = 10 - 3 - 2; } fin")
    fila = a.gen.fila
    assert _ops(a) == ["-", "-", "="]
    assert fila[1].opIzq == fila[0].resultado, "el 2do '-' debe operar sobre el temporal del 1ero"


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
