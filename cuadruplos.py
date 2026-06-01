import sys
from dataclasses import dataclass
from cubo import tipo_resultado

@dataclass 
class Cuadruplo:
    """
    Cuadruplo: (operador, arg1, arg2, resultado)
    """
    
    op: str
    opIzq: int = None
    opDer: int = None
    resultado: int = None
    

class TablaConstantes:
    """
    Registra constantes en la tabla de constantes.
    Usa deduplicacion de constantes para evitar repeticiones.
    asignando eon el mismo lexema a la misma direccion.
    """

    def __init__(self):
        self._ents = {}
        self._floats = {}
        self._letreros = {}
        self._next_ent = 13000
        self._next_float = 14000
        self._next_letrero = 15000
    
    def direccion_de_numerica(self, lexema, tipo):
        """Para constantes numericas. Devuelve direccion (existente o nueva)."""
        if tipo == "entero":
            tabla, contador_attr = self._ents, "_next_ent"
            # doble asignacion, y usamos "papelito intercambiable" de contador_attr para no duplicar codigo, y poder cambiar el atributo en tiempo de ejecucion.
        elif tipo == "flotante":
            tabla, contador_attr = self._floats, "_next_float"
        else:
            raise ValueError(f"tipo invalido para constante numerica: {tipo}")

        if lexema in tabla:
            return tabla[lexema] # si la variable ta existe regresa la direccion virtual asignada.
        direccion = getattr(self, contador_attr) # obtenemos el valor actual del contador lo cual depende de nuestro "papelito intercambiable" si es entero o flotante.
        tabla[lexema] = direccion
        setattr(self, contador_attr, direccion + 1) # incrementamos el contador para la proxima constante.
        return direccion

    def direccion_de_letrero(self, lexema):
        """Para letreros (strings). Devuelve direccion (existente o nueva)."""
        if lexema in self._letreros:
            return self._letreros[lexema] # si la variable ta existe regresa la direccion virtual asignada.
        direccion = self._next_letrero # si la variable no existe, obtenemos la direccion virtual siguiente vacia.
        self._letreros[lexema] = direccion # asignamos la direccion virtual a la variable.
        self._next_letrero += 1 # incrementamos el contador para la proxima constante.
        return direccion # regresa la direccion virtual asignada.

    def imprimir(self, out=sys.stdout):
        """Para el flag --cuadruplos."""
        print("=== TABLA DE CONSTANTES ===", file=out)
        for lex, dir_ in sorted(self._ents.items(), key=lambda kv: kv[1]):
            print(f"  {dir_}: {lex} (entero)", file=out)
        for lex, dir_ in sorted(self._floats.items(), key=lambda kv: kv[1]):
            print(f"  {dir_}: {lex} (flotante)", file=out)
        for lex, dir_ in sorted(self._letreros.items(), key=lambda kv: kv[1]):
            print(f"  {dir_}: {lex} (letrero)", file=out)


class GeneradorCuadruplos:
    """
    Encapsula las 3 pilas y la fila de cuadruplos.
    Aplica el cubo semantico en cada operacion binaria.

    Recibe mem (AsignadorMemoria) y cte (TablaConstantes) por constructor:
    asi no necesita importarlos, evitando dependencias cruzadas.
    """
    
    def __init__(self, mem, cte):
        self.mem = mem # asignador de memoria
        self.cte = cte
        self.pila_operandos = [] 
        self.pila_tipos = []
        self.pila_operadores = []
        self.fila = []
        self._ultimo_propagado = False
    # --- Operaciones de pila ---
    def push_operando(self, direccion, tipo):
        self.pila_operandos.append(direccion)
        self.pila_tipos.append(tipo)

    def push_operador(self, op):
        self.pila_operadores.append(op)

    def pop_operando(self):
        """Pop sin emitir nada (caso escribe(expresion))."""
        if self.pila_operandos:
            self.pila_operandos.pop()
            self.pila_tipos.pop()

    def top_operando(self):
        return self.pila_operandos[-1] if self.pila_operandos else None

    def top_tipo(self):
        return self.pila_tipos[-1] if self.pila_tipos else None

    def pilas_operandos_vacia(self):
        return len(self.pila_operandos) == 0

    # --- Generacion ---
    def pop_y_emitir_binario(self):
        """
        Pop del operador + 2 operandos+tipos. Consulta el cubo.
        Asigna temporal, emite cuadruplo, push del temporal.
        Devuelve el tipo del resultado, o "error" si es invalido.

        Si algun operando ya venia como "error" (propagacion), devuelve "error"
        Y marca _ultimo_propagado=True para que el caller NO reporte un mensaje
        duplicado (el error raiz ya se reporto mas abajo en el arbol).
        """
        self._ultimo_propagado = False

        if not self.pila_operadores or len(self.pila_operandos) < 2:
            return "error"

        op = self.pila_operadores.pop()
        d_der = self.pila_operandos.pop()
        t_der = self.pila_tipos.pop()
        d_izq = self.pila_operandos.pop()
        t_izq = self.pila_tipos.pop()

        # Propagacion silenciosa
        if t_izq == "error" or t_der == "error":
            self._ultimo_propagado = True
            self.pila_operandos.append(None)
            self.pila_tipos.append("error")
            return "error"

        t_res = tipo_resultado(op, t_izq, t_der)
        if t_res is None:
            # ERROR genuino del cubo. Empujamos sentinel para no romper el balance.
            self.pila_operandos.append(None)
            self.pila_tipos.append("error")
            return "error"

        d_res = self.mem.nuevo_temporal(t_res)
        self.fila.append(Cuadruplo(op=op, opIzq=d_izq, opDer=d_der, resultado=d_res))
        self.pila_operandos.append(d_res)
        self.pila_tipos.append(t_res)
        return t_res

    def emitir_asignacion(self, direccion_destino, tipo_destino):
        """Pop del RHS, valida cubo (=), emite (=, rhs, _, destino)."""
        self._ultimo_propagado = False
        if not self.pila_operandos:
            return "error"

        d_origen = self.pila_operandos.pop()
        t_origen = self.pila_tipos.pop()

        if t_origen == "error":
            self._ultimo_propagado = True
            return "error"

        t_res = tipo_resultado("=", tipo_destino, t_origen)
        if t_res is None:
            return "error"

        self.fila.append(Cuadruplo(op="=", opIzq=d_origen, opDer=None, resultado=direccion_destino))
        return t_res

    def emitir_print(self, direccion):
        self.fila.append(Cuadruplo(op="PRINT", opIzq=None, opDer=None, resultado=direccion))

    def emitir_directo(self, cuadruplo):
        """Para cuadruplos que no surgen del flujo binario (p.ej. signo unario)."""
        self.fila.append(cuadruplo)

    def backpatch(self, indice, target):
        """
        Muta el campo resultado del cuadruplo en self.fila[indice].
        Sin uso en Sesion 3; listo para Etapa 4 (resolver saltos GOTOF/GOTO).
        """
        self.fila[indice].resultado = target

    def ultimo_fue_propagado(self):
        return self._ultimo_propagado

    def imprimir_fila(self, out=sys.stdout):
        """Para el flag --cuadruplos."""
        print(f"=== FILA DE CUADRUPLOS ({len(self.fila)}) ===", file=out)
        for i, q in enumerate(self.fila):
            def _f(x):
                return "_" if x is None else str(x)
            print(f"  {i}: ({q.op}, {_f(q.opIzq)}, {_f(q.opDer)}, {_f(q.resultado)})", file=out)