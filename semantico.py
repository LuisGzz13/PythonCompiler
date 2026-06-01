"""
Analisis semantico de Patito.

Contiene:
  - Registros de datos: VarInfo, ParamInfo, FuncInfo
  - AsignadorMemoria: direcciones virtuales por (segmento x tipo)
  - Helpers para aplanar subreglas recursivas de la gramatica
  - SemanticAnalyzer(PatitoListener): los puntos neuralgicos

Los puntos neuralgicos estan marcados con headers "PN-x" para referencia
con los diagramas de la documentacion.

Importa de cuadruplos.py y de PatitoListener (generado). NO importa de
patito.py, por eso no hay ciclo: patito.py importa de aqui, no al reves.
"""

import sys
sys.path.insert(0, 'generated')

from PatitoListener import PatitoListener
from cuadruplos import Cuadruplo, TablaConstantes, GeneradorCuadruplos


# ============================================================
# REGISTROS DE DATOS (esquemas de las tablas)
# ============================================================

class VarInfo:
    """Info de una variable: tipo, linea de declaracion, direccion virtual."""
    def __init__(self, tipo, linea, direccion=None):
        self.tipo = tipo
        self.linea = linea
        self.direccion = direccion # direccion virtual asignada.


class ParamInfo:
    """Info de un parametro: nombre, tipo, direccion (el orden importa)."""
    def __init__(self, nombre, tipo, direccion=None):
        self.nombre = nombre
        self.tipo = tipo
        self.direccion = direccion # direccion virtual asignada.


class FuncInfo:
    """
    Info de una funcion (o el programa principal):
      - tipo_retorno: 'entero', 'flotante', 'nula' o 'programa'
      - params: lista de ParamInfo en orden
      - variables: dict {nombre -> VarInfo} de locales + parametros
      - linea: donde se declaro
      - cuad_inicio: indice del primer cuadruplo del cuerpo (Etapa 4 lo poblara)
    """
    # clave distingui el NULA es solamente aplicable a declarar funciones, el lenguaje patito no tiene retorno nulo.
    def __init__(self, tipo_retorno, linea):
        self.tipo_retorno = tipo_retorno # 'entero', 'flotante', 'nulo' o 'programa' de la funcion
        self.params = [] # iniciliza lista de parametros vacias
        self.variables = {} # iniciliza diccionario de variables vacio
        self.linea = linea # asigna la linea de declaracion de la funcion
        self.cuad_inicio = None 


# ============================================================
# ASIGNADOR DE MEMORIA VIRTUAL
# ============================================================

class AsignadorMemoria:
    """
    Asigna direcciones virtuales por (segmento x tipo).

    Rangos:
      GLOBAL    entero  1000-1999     flotante  2000-2999     bool  3000-3999
      LOCAL     entero  5000-5999     flotante  6000-6999     bool  7000-7999
      TEMPORAL  entero  9000-9999     flotante 10000-10999    bool 11000-11999

    Huecos (4000, 8000, 12000) intencionales: espaciamos en segmentos de 1000 direcciones para cada tipo. y ademas reservamos por si se ocupa en un futuro.

    - Globales: nunca se resetean (zona estatica unica)
    - Locales y temporales: se resetean al entrar a cada funcion
    """

    _BASE = {
        ("global", "entero"):    1000,
        ("global", "flotante"):  2000,
        ("global", "bool"):      3000,
        ("local", "entero"):     5000,
        ("local", "flotante"):   6000,
        ("local", "bool"):       7000,
        ("temp", "entero"):      9000,
        ("temp", "flotante"):   10000,
        ("temp", "bool"):       11000,
    }

    def __init__(self):
        self._contadores = {k: v for k, v in self._BASE.items()}

    def reset_scope_local(self):
        """Resetea locales y temporales. Llamar al entrar a cada funcion."""
        for seg in ("local", "temp"):
            for tipo in ("entero", "flotante", "bool"):
                self._contadores[(seg, tipo)] = self._BASE[(seg, tipo)]

    def nueva_global(self, tipo):
        return self._asignar("global", tipo)

    def nueva_local(self, tipo):
        return self._asignar("local", tipo)

    def nuevo_temporal(self, tipo):
        return self._asignar("temp", tipo)

    def _asignar(self, seg, tipo):
        clave = (seg, tipo)
        dir_actual = self._contadores[clave]
        self._contadores[clave] += 1
        return dir_actual


# ============================================================
# HELPERS: aplanan subreglas recursivas de la gramatica
# ============================================================

def _ids_de_idLista(idLista_ctx):
    """
    Aplana 'idLista : ID idResto' + 'idResto : COMA ID idResto | epsilon'
    en una lista de TerminalNode ID.
    """
    if idLista_ctx is None:
        return []
    ids = [idLista_ctx.ID()]
    resto = idLista_ctx.idResto()
    while resto is not None and resto.ID() is not None:
        ids.append(resto.ID())
        resto = resto.idResto()
    return ids


def _params_de_paramsOpc(paramsOpc_ctx):
    """
    Aplana paramsOpc -> paramLista + paramResto en lista de tuplas (ID_node, tipo_str).

    Gramatica:
      paramsOpc  : paramLista | epsilon
      paramLista : ID DPUNTOS tipo paramResto
      paramResto : COMA ID DPUNTOS tipo paramResto | epsilon
    """
    if paramsOpc_ctx is None or paramsOpc_ctx.paramLista() is None:
        return []
    paramLista = paramsOpc_ctx.paramLista()
    params = [(paramLista.ID(), paramLista.tipo().getText())]
    resto = paramLista.paramResto()
    while resto is not None and resto.ID() is not None:
        params.append((resto.ID(), resto.tipo().getText()))
        resto = resto.paramResto()
    return params


# ============================================================
# ANALIZADOR SEMANTICO (LISTENER) - PUNTOS NEURALGICOS
# ============================================================

class SemanticAnalyzer(PatitoListener):
    """
    Subclase de PatitoListener (ANTLR4).
    Implementa 13 puntos neuralgicos:
      Etapa 2 (4): enterPrograma, enterFuncs, exitFuncs, enterDeclaracion
      Etapa 3 (9): exitFactor, enter/exitExp, enter/exitTermino,
                   enterRelOpc, exitExpresion, exitAsigna, exitImpElem
    """

    def __init__(self):
        self.func_dir = {} # diccionario de funciones {nombre -> FuncInfo}
        self.scope_actual = None # puntero al scope actual 
        self.nombre_programa = None # nombre del programa principal
        self.errores = 0
        self.en_func_duplicada = False # flag para detectar funciones duplicadas
        self.mem = AsignadorMemoria() 
        self.cte = TablaConstantes() 
        self.gen = GeneradorCuadruplos(self.mem, self.cte) #  de cuadruplos

    def error(self, linea, col, msg):
        """Reporta error semantico a stderr y suma al contador."""
        print(f"linea {linea}:{col}  semantica: {msg}", file=sys.stderr)
        self.errores += 1

    # --- Helpers de scope ---
    def _buscar_var(self, nombre):
        """Busca variable: primero local, luego global. Devuelve VarInfo o None."""
        if nombre in self.scope_actual.variables:
            return self.scope_actual.variables[nombre]
        programa = self.func_dir[self.nombre_programa]
        if self.scope_actual is not programa and nombre in programa.variables:
            return programa.variables[nombre]
        return None

    def scope_actual_nombre(self):
        """Nombre del scope actual, para mensajes de error."""
        for nombre, info in self.func_dir.items():
            if info is self.scope_actual:
                return nombre
        return "?"

    # ========================================================
    # PN-1 (Etapa 2): enterPrograma -> registra el programa global
    # ========================================================
    def enterPrograma(self, ctx):
        nombre = ctx.ID().getText()
        linea = ctx.ID().getSymbol().line
        self.nombre_programa = nombre
        self.func_dir[nombre] = FuncInfo(tipo_retorno="programa", linea=linea)
        self.scope_actual = self.func_dir[nombre]

    # ========================================================
    # PN-2 (Etapa 2): enterFuncs -> registra funcion + parametros
    # ========================================================
    def enterFuncs(self, ctx):
        if ctx.ID() is None:
            return

        nombre = ctx.ID().getText()
        linea = ctx.ID().getSymbol().line
        tipo_retorno = ctx.tipoFunc().getText()  # "nula", "entero" o "flotante"

        if nombre == self.nombre_programa:
            self.error(linea, 0,
                f"funcion '{nombre}' no puede tener el mismo nombre que el programa")
            self.en_func_duplicada = True
            return

        if nombre in self.func_dir:
            self.error(linea, 0, f"funcion '{nombre}' ya esta declarada")
            self.en_func_duplicada = True
            return

        nueva = FuncInfo(tipo_retorno=tipo_retorno, linea=linea)
        self.func_dir[nombre] = nueva
        self.scope_actual = nueva
        self.mem.reset_scope_local()

        for id_node, tipo in _params_de_paramsOpc(ctx.paramsOpc()):
            self._registrar_parametro(id_node, tipo)

    def _registrar_parametro(self, id_node, tipo):
        nombre = id_node.getText()
        linea = id_node.getSymbol().line

        if nombre in self.scope_actual.variables:
            self.error(linea, 0, f"parametro '{nombre}' duplicado en la funcion")
            return

        direccion = self.mem.nueva_local(tipo)
        self.scope_actual.variables[nombre] = VarInfo(tipo=tipo, linea=linea, direccion=direccion)
        self.scope_actual.params.append(ParamInfo(nombre=nombre, tipo=tipo, direccion=direccion))

    # ========================================================
    # PN-3 (Etapa 2): exitFuncs -> cierra el scope local
    # ========================================================
    def exitFuncs(self, ctx):
        if ctx.ID() is None:
            return
        if self.en_func_duplicada:
            self.en_func_duplicada = False
            return
        self.scope_actual = self.func_dir[self.nombre_programa]

    # ========================================================
    # PN-4 (Etapa 2): enterDeclaracion -> registra cada variable
    # ========================================================
    def enterDeclaracion(self, ctx):
        if self.en_func_duplicada:
            return

        tipo = ctx.tipo().getText()
        es_global = (self.scope_actual is self.func_dir[self.nombre_programa])

        for id_node in _ids_de_idLista(ctx.idLista()):
            nombre = id_node.getText()
            linea = id_node.getSymbol().line

            if nombre in self.scope_actual.variables:
                self.error(linea, 0,
                    f"variable '{nombre}' ya esta declarada en este scope")
                continue

            if es_global:
                direccion = self.mem.nueva_global(tipo)
            else:
                direccion = self.mem.nueva_local(tipo)

            self.scope_actual.variables[nombre] = VarInfo(tipo=tipo, linea=linea, direccion=direccion)

    # ========================================================
    # PN3-A (Etapa 3): exitFactor -> operandos a las pilas
    # ========================================================
    def exitFactor(self, ctx):
        """
        factor : PIZQ expresion PDER   (1: nada)
               | llamada                (2: temporal fantasma)
               | signoOpc ID            (3: push var)
               | signoOpc cte           (4: push constante)
        """
        if self.en_func_duplicada:
            return

        # Caso 1: parentesis
        if ctx.PIZQ() is not None:
            return

        # Caso 2: llamada en expresion
        if ctx.llamada() is not None:
            llamada_ctx = ctx.llamada()
            nombre_func = llamada_ctx.ID().getText()
            linea = llamada_ctx.ID().getSymbol().line

            if nombre_func not in self.func_dir or nombre_func == self.nombre_programa:
                self.error(linea, 0, f"funcion '{nombre_func}' no declarada")
                self.gen.push_operando(None, "error")
                return

            f = self.func_dir[nombre_func]
            if f.tipo_retorno == "nula":
                self.error(linea, 0,
                    f"no se puede usar funcion '{nombre_func}' (retorno nula) en una expresion")
                self.gen.push_operando(None, "error")
                return

            # Temporal fantasma (Etapa 4 emitira ERA/PARAM/GOSUB reales)
            dir_temp = self.mem.nuevo_temporal(f.tipo_retorno)
            self.gen.push_operando(dir_temp, f.tipo_retorno)
            return

        # Casos 3 y 4: signoOpc seguido de ID o cte
        signo = ctx.signoOpc()
        tiene_menos = signo is not None and signo.MENOS() is not None

        if ctx.ID() is not None:
            nombre = ctx.ID().getText()
            linea = ctx.ID().getSymbol().line

            v = self._buscar_var(nombre)
            if v is None:
                self.error(linea, 0,
                    f"variable '{nombre}' usada sin declarar en '{self.scope_actual_nombre()}'")
                self.gen.push_operando(None, "error")
                return

            if tiene_menos:
                cero_dir = self.cte.direccion_de_numerica("0", "entero")
                t = self.mem.nuevo_temporal(v.tipo)
                self.gen.emitir_directo(Cuadruplo(op="-", opIzq=cero_dir, opDer=v.direccion, resultado=t))
                self.gen.push_operando(t, v.tipo)
            else:
                self.gen.push_operando(v.direccion, v.tipo)
            return

        if ctx.cte() is not None:
            cte_ctx = ctx.cte()
            if cte_ctx.CTE_ENT() is not None:
                lex = cte_ctx.CTE_ENT().getText()
                tipo = "entero"
            else:
                lex = cte_ctx.CTE_FLOT().getText()
                tipo = "flotante"

            if tiene_menos:
                lex = "-" + lex  # "-5" distinta de "5"

            dir_cte = self.cte.direccion_de_numerica(lex, tipo)
            self.gen.push_operando(dir_cte, tipo)

    # ========================================================
    # PN3-B1/B2 (Etapa 3): enterExp / exitExp  (+ -)
    # ========================================================
    def enterExp(self, ctx):
        if self.en_func_duplicada:
            return
        if ctx.MAS() is not None:
            self.gen.push_operador("+")
        elif ctx.MENOS() is not None:
            self.gen.push_operador("-")

    def exitExp(self, ctx):
        if self.en_func_duplicada:
            return
        if ctx.MAS() is None and ctx.MENOS() is None:
            return
        res = self.gen.pop_y_emitir_binario()
        if res == "error" and not self.gen.ultimo_fue_propagado():
            linea = ctx.start.line
            op_str = "+" if ctx.MAS() is not None else "-"
            self.error(linea, 0, f"tipos incompatibles para operador '{op_str}'")

    # ========================================================
    # PN3-C1/C2 (Etapa 3): enterTermino / exitTermino  (* /)
    # ========================================================
    def enterTermino(self, ctx):
        if self.en_func_duplicada:
            return
        if ctx.POR() is not None:
            self.gen.push_operador("*")
        elif ctx.ENTRE() is not None:
            self.gen.push_operador("/")

    def exitTermino(self, ctx):
        if self.en_func_duplicada:
            return
        if ctx.POR() is None and ctx.ENTRE() is None:
            return
        res = self.gen.pop_y_emitir_binario()
        if res == "error" and not self.gen.ultimo_fue_propagado():
            linea = ctx.start.line
            op_str = "*" if ctx.POR() is not None else "/"
            self.error(linea, 0, f"tipos incompatibles para operador '{op_str}'")

    # ========================================================
    # PN3-D1/D2 (Etapa 3): enterRelOpc / exitExpresion  (< > == !=)
    # ========================================================
    def enterRelOpc(self, ctx):
        if self.en_func_duplicada:
            return
        op_rel = ctx.opRel()
        if op_rel is None:
            return
        if op_rel.MAYOR() is not None:
            self.gen.push_operador(">")
        elif op_rel.MENOR() is not None:
            self.gen.push_operador("<")
        elif op_rel.DISTINTO() is not None:
            self.gen.push_operador("!=")
        elif op_rel.IGUAL2() is not None:
            self.gen.push_operador("==")

    def exitExpresion(self, ctx):
        if self.en_func_duplicada:
            return
        rel_opc = ctx.relOpc()
        if rel_opc is None or rel_opc.opRel() is None:
            return
        res = self.gen.pop_y_emitir_binario()
        if res == "error" and not self.gen.ultimo_fue_propagado():
            linea = ctx.start.line
            self.error(linea, 0, "tipos incompatibles en expresion relacional")

    # ========================================================
    # PN3-E (Etapa 3): exitAsigna  (=)
    # ========================================================
    def exitAsigna(self, ctx):
        if self.en_func_duplicada:
            return
        nombre = ctx.ID().getText()
        linea = ctx.ID().getSymbol().line

        v = self._buscar_var(nombre)
        if v is None:
            self.error(linea, 0,
                f"variable '{nombre}' usada sin declarar en '{self.scope_actual_nombre()}'")
            if not self.gen.pilas_operandos_vacia():
                self.gen.pop_operando()
            return

        res = self.gen.emitir_asignacion(v.direccion, v.tipo)
        if res == "error" and not self.gen.ultimo_fue_propagado():
            self.error(linea, 0,
                f"tipos incompatibles en asignacion a '{nombre}' ({v.tipo})")

    # ========================================================
    # PN3-F (Etapa 3): exitImpElem  (escribe)
    # ========================================================
    def exitImpElem(self, ctx):
        if self.en_func_duplicada:
            return
        # impElem : expresion | LETRERO
        if ctx.LETRERO() is not None:
            lex = ctx.LETRERO().getText()
            dir_letrero = self.cte.direccion_de_letrero(lex)
            self.gen.emitir_print(dir_letrero)
        elif ctx.expresion() is not None:
            if not self.gen.pilas_operandos_vacia():
                dir_expr = self.gen.top_operando()
                self.gen.pop_operando()
                self.gen.emitir_print(dir_expr)