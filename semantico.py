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
from PatitoParser import PatitoParser
from cubo import tipo_resultado


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
        self.recursos = None  # snapshot {(seg,tipo): count} para que la VM reserve el frame


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
    
    def snapshot_recursos(self):
        """Devuelve un dict con claves como ("local", "entero") → 2 ("esta función usó 2 enteros locales"). 
        Las globales no se incluyen porque no son per-frame..
        """
        recursos = {}
        for (seg, tipo) in self._contadores:
            if seg in ("local", "temp"):
                recursos[(seg, tipo)] = self._contadores[(seg, tipo)] - self._BASE[(seg, tipo)]
        return recursos


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
        self.gen = GeneradorCuadruplos(self.mem, self.cte)
        self.pila_llamadas = [] # pila de llamadas a funciones (para anidados)

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
        self.gen.idx_goto_main = self.gen.emitir_goto()
        
    # ========================================================
    # PN-1B (Etapa 5): exitPrograma -> snapshot de recursos de main
    # ========================================================
    def exitPrograma(self, ctx):
        # Main es el ultimo en compilarse (despues de todas las funciones).
        # Capturamos sus recursos para que la VM pueda reservar el frame inicial.
        programa = self.func_dir[self.nombre_programa]
        programa.recursos = self.mem.snapshot_recursos()

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
        nueva.cuad_inicio = len(self.gen.fila)

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
        
        # Snapshot ANTES del switch de scope, self.scope_actual aun apunta a la funcion actual.
        self.scope_actual.recursos = self.mem.snapshot_recursos()
        self.gen.emitir_endfunc()
        self.scope_actual = self.func_dir[self.nombre_programa]
        
        
    
    # ========================================================
    # PN-4E (Etapa 4): enterCuerpo -> rellena el GOTO-main al iniciar 'main'
    # ========================================================
    def enterCuerpo(self, ctx):
        if self.en_func_duplicada:
            return
        # El cuerpo de 'main' es el unico cuerpo hijo directo de 'programa'.
        # Al entrar a el, ya pasamos todas las funciones, asi que aqui empieza main.
        if isinstance(ctx.parentCtx, PatitoParser.ProgramaContext):
            # Etapa 5: limpiamos contadores antes de que main empiece a usarlos.
            # Si no, main "hereda" los valores que dejo la ultima funcion.
            self.mem.reset_scope_local()
            self.gen.backpatch(self.gen.idx_goto_main, len(self.gen.fila))
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
        PN3-A: empuja operandos a la pila desde un factor.

        factor : PIZQ expresion PDER   ← ya emitio + dejo operando en la pila (nada que hacer)
            | llamada                ← enter/exitLlamada ya emitieron ERA/PARAM/GOSUB + temporal
            | signoOpc ID            ← se maneja abajo
            | signoOpc cte           ← se maneja abajo
        """
        if self.en_func_duplicada:
            return

        signo = ctx.signoOpc()
        tiene_menos = signo is not None and signo.MENOS() is not None

        # Variable ID
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
                # -x se emite como (0 - x) usando un cuadruplo directo.
                cero_dir = self.cte.direccion_de_numerica("0", "entero")
                t = self.mem.nuevo_temporal(v.tipo)
                self.gen.emitir_directo(
                    Cuadruplo(op="-", opIzq=cero_dir, opDer=v.direccion, resultado=t))
                self.gen.push_operando(t, v.tipo)
            else:
                self.gen.push_operando(v.direccion, v.tipo)
            return

        # Constante
        if ctx.cte() is not None:
            cte_ctx = ctx.cte()
            if cte_ctx.CTE_ENT() is not None:
                lex = cte_ctx.CTE_ENT().getText()
                tipo = "entero"
            else:
                lex = cte_ctx.CTE_FLOT().getText()
                tipo = "flotante"

            if tiene_menos:
                lex = "-" + lex  # "-5" usa entrada distinta de "5" en la tabla de constantes

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
        # 1. Procesamiento relacional (solo si hay opRel: < > == !=)
        rel_opc = ctx.relOpc()
        if rel_opc is not None and rel_opc.opRel() is not None:
            res = self.gen.pop_y_emitir_binario()
            if res == "error" and not self.gen.ultimo_fue_propagado():
                linea = ctx.start.line
                self.error(linea, 0, "tipos incompatibles en expresion relacional")
        # 2. Despacho segun el contexto del padre (Etapa 4):
        #    - condicion/ciclo  -> esta expresion ES una condicion  -> GOTOF
        #    - (chunk 4 agregara: argLista/argResto -> PARAM)
        parent = ctx.parentCtx
        if isinstance(parent, (PatitoParser.CondicionContext, PatitoParser.CicloContext)):
            self._manejar_condicion(ctx)
        elif isinstance(parent, (PatitoParser.ArgListaContext, PatitoParser.ArgRestoContext)):
            self._manejar_argumento(ctx)

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
                
    def _manejar_condicion(self, ctx):
        """
        PN-4A: la expresion de un 'si'/'mientras' termino de evaluarse. Su
        resultado (tope de pila) debe ser bool. Emite GOTOF y guarda su indice
        en pila_saltos para backpatch.

        INVARIANTE: siempre empuja EXACTAMENTE un indice a pila_saltos, porque
        exitCondicion/exitCiclo hacen pop incondicional. Por eso el GOTOF se
        emite SIEMPRE (aun con error de tipo o pila vacia).
        """
        
        if self.gen.pilas_operandos_vacia():
            # Defensivo: no deberia pasar (siempre hay operando o None para no desbalancear la pila).
            # Aun asi emitimos+empujamos para no romper el invariante.
            self.gen.pila_saltos.append(self.gen.emitir_goto_falso(None))
            return

        tipo = self.gen.top_tipo()
        dir_cond = self.gen.top_operando()
        self.gen.pop_operando()
        
        if tipo != "bool" and tipo != "error":
            self.error(ctx.start.line, 0, "la condicion de si/mientras debe ser tipo bool")
        
        self.gen.pila_saltos.append(self.gen.emitir_goto_falso(dir_cond))
    
    # --- ciclo: MIENTRAS (cond) HAZ cuerpo ---
    def enterCiclo(self, ctx):
        if self.en_func_duplicada:
            return
        # Punto de retorno: aqui empieza la condicion; el GOTO del final regresa aca.
        self.gen.pila_saltos.append(len(self.gen.fila))

    def exitCiclo(self, ctx):
        if self.en_func_duplicada:
            return
        falso = self.gen.pila_saltos.pop()     # GOTOF de la condicion
        retorno = self.gen.pila_saltos.pop()   # inicio de la condicion
        self.gen.emitir_goto_a(retorno)        # regresa a re-evaluar la condicion
        self.gen.backpatch(falso, len(self.gen.fila))  # GOTOF -> salida del ciclo
            
    # --- condicion: SI (cond) cuerpo sinoOpc PCOMA ---
    def enterSinoOpc(self, ctx):
        if self.en_func_duplicada:
            return
        if ctx.SINO() is None:   # rama epsilon: no hay 'sino'
            return
        falso = self.gen.pila_saltos.pop()        # GOTOF del 'si'
        indice_goto = self.gen.emitir_goto()      # GOTO que brinca el cuerpo del 'sino'
        self.gen.pila_saltos.append(indice_goto)
        self.gen.backpatch(falso, len(self.gen.fila))  # GOTOF -> inicio del 'sino'

    def exitCondicion(self, ctx):
        if self.en_func_duplicada:
            return
        # Salto pendiente: el GOTOF (si no hubo 'sino') o el GOTO (si lo hubo).
        indice = self.gen.pila_saltos.pop()
        self.gen.backpatch(indice, len(self.gen.fila))


    # ========================================================
    # ETAPA 4 - LLAMADA A FUNCIONES (ERA / PARAM / GOSUB)
    # ========================================================
    
    def enterLlamada(self, ctx):
        """
        PN-4B: inicio de llamada. Verifica que la funcion exista, emite ERA y
        apila el contexto (para validar argumentos y soportar llamadas anidadas).
        """
        
        if self.en_func_duplicada:
            return
        nombre = ctx.ID().getText()
        linea = ctx.ID().getSymbol().line
        
        # checa si la funcion existe o no, y que no sea el nombre del programa principal
        if nombre not in self.func_dir or nombre == self.nombre_programa:
            self.error(linea, 0, f"funcion '{nombre}' no declarada")
            self.pila_llamadas.append(
                {"valida": False, "func": None, "nombre": nombre, "n": 0, "linea": linea})
            return
        
        f = self.func_dir[nombre]
        self.gen.emitir_era(nombre)
        self.pila_llamadas.append(
            {"valida": True, "func": f, "nombre": nombre, "n": 0, "linea": linea})
        
    
    
    def _manejar_argumento(self, ctx):
        """
        PN-4C: un argumento termino de evaluarse (tope de pila). Lo empareja con
        el parametro k de la funcion en curso, valida su tipo y emite PARAM.
        """
        
        if not self.pila_llamadas or self.gen.pilas_operandos_vacia():
            return
        contexto = self.pila_llamadas[-1]
        dir_arg = self.gen.top_operando()
        tipo_arg = self.gen.top_tipo()
        self.gen.pop_operando() # consume el argumento SIEMPRE
        
        idx = contexto["n"]
        contexto["n"] += 1
        
        if not contexto["valida"]:
            return      # funcion inexistente: ya reportamos
        f = contexto["func"]
        if idx >= len(f.params):
            return      # sobran args; el conteo se valida en exitLlamada
        if tipo_arg == "error":
            return      # error ya reportado mas abajo en el arbol
            
        param = f.params[idx]
        if tipo_resultado("=", param.tipo, tipo_arg) is None:
            self.error(contexto["linea"], 0,
                f"argumento {idx + 1} de '{contexto['nombre']}': "
                f"se esperaba {param.tipo}, se recibio {tipo_arg}")
            return
        self.gen.emitir_param(dir_arg, param.direccion)
    
    def exitLlamada(self, ctx):
        """
        PN-4D: fin de llamada. Valida el numero de argumentos, emite GOSUB y, si
        la llamada se usa como factor, deja el resultado (temporal) en la pila.
        """
        if self.en_func_duplicada:
            return
        contexto = self.pila_llamadas.pop()
        es_factor = isinstance(ctx.parentCtx, PatitoParser.FactorContext)

        if not contexto["valida"]:
            if es_factor:
                self.gen.push_operando(None, "error")
            return

        f = contexto["func"]
        nombre = contexto["nombre"]
        linea = contexto["linea"]

        if contexto["n"] != len(f.params):
            self.error(linea, 0,
                f"funcion '{nombre}' espera {len(f.params)} argumento(s), "
                f"recibio {contexto['n']}")

        self.gen.emitir_gosub(nombre, f.cuad_inicio)

        # Si la llamada esta dentro de una expresion necesita dejar un valor.
        if es_factor:
            if f.tipo_retorno == "nula":
                self.error(linea, 0,
                    f"no se puede usar funcion '{nombre}' (retorno nula) en una expresion")
                self.gen.push_operando(None, "error")
            else:
                # Temporal fantasma: el retorno real se difiere (no toca la gramatica).
                dir_temp = self.mem.nuevo_temporal(f.tipo_retorno)
                self.gen.push_operando(dir_temp, f.tipo_retorno)