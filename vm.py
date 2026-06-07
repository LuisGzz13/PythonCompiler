"""
Maquina Virtual de Patito (Etapa 5).

Lee la fila de cuadruplos y la tabla de constantes producidas por el compilador
(analizador semantico) y ejecuta el codigo intermedio.

Diseño clave (las 3 reglas que sostienen todo lo demas):
  1. Main es el bottom de pila_frames -> routing uniforme, sin casos especiales.
  2. PARAM lee del caller (frame actual) y escribe en el callee (top de pila_prep).
     No usar 'escribir()' para PARAM o pisas memoria del caller.
  3. pila_prep es PILA, no slot. ERA empuja, GOSUB hace pop+activa.
     Soporta llamadas anidadas tipo f(g(x)).
"""


from semantico import AsignadorMemoria
from cuadruplos import TablaConstantes



# Defaults por tipo. Cualquier slot que se lea sin haberse escrito antes
# devuelve esto en lugar de crashear. Importante para el "phantom temporal"
# de las funciones tipadas sin retorno real (Etapa 4, limitacion documentada).
_DEFAULTS = {
    "entero":   0,
    "flotante": 0.0,
    "bool":     0, # bool en patito es 0 y 1
}

_RANGOS = []
for (seg, tipo), base in AsignadorMemoria._BASE.items():
    _RANGOS.append((base, base + 1000, seg, tipo))
for tipo, base in TablaConstantes._BASE.items():
    _RANGOS.append((base, base + 1000, "cte", tipo))

def _segmento_y_tipo(direccion):
    """Decodifica una direccion virtual en (segmento, tipo). None si invalida.

    Las direcciones VIENEN del compilador con el formato (segmento x tipo) que
    se decidio en Etapa 3. La VM las usa COMO INDICE: el rango te dice donde
    vive el dato (memoria global, memoria de constantes, o frame actual).

    Recorre _RANGOS (derivados de las bases del compilador). Como solo hay 12
    rangos, la busqueda lineal es trivial; quedaria igual con un if/elif.
    """
    if direccion is None:
        return None
    for start, end, seg, tipo in _RANGOS:
        if start <= direccion < end:
            return (seg, tipo)
    return None


class Frame:
    """Un frame de ejecucion: memoria local + temporal de UNA funcion activa.

    nombre:      el nombre de la funcion (debug y trazas)
    locales:     dict {direccion -> valor} para 5000s/6000s/7000s
    temps:       dict {direccion -> valor} para 9000s/10000s/11000s
    ip_retorno:  IP al que volver cuando esta funcion termine (lo escribe GOSUB)
    """
    def __init__(self, nombre):
        self.nombre = nombre
        self.locales = {}
        self.temps = {}
        self.ip_retorno = None

class MaquinaVirtual:
    def __init__(self, analizador):
        """Construye el estado inicial a partir del SemanticAnalyzer compilado.

        analizador.gen.fila   -> lista de Cuadruplo a ejecutar
        analizador.cte        -> tabla de constantes (lexema -> direccion)
        analizador.func_dir   -> dict {nombre_func -> FuncInfo} con cuad_inicio y recursos
        """
        self.fila = analizador.gen.fila
        self.func_dir = analizador.func_dir
        self.nombre_programa = analizador.nombre_programa

        # Memoria global: persiste durante TODA la ejecucion.
        self.memoria_global = {}

        # Memoria de constantes: direccion -> valor (ya convertido a int/float/str).
        # El compilador guardo lexema->direccion; aqui invertimos y convertimos.
        self.memoria_constantes = self._cargar_constantes(analizador.cte)

        # Pila de frames de ejecucion. Main es el bottom (frame[0]).
        # Empujamos el frame de main YA inicializado: routing uniforme desde aqui.
        main = self._nuevo_frame(self.nombre_programa)
        self.pila_frames = [main]


        # Pila de prep frames: frames creados por ERA, activados por GOSUB.
        # PILA (no slot) para soportar llamadas anidadas como f(g(x)).
        self.pila_prep = []

        # Instruction Pointer: indice del proximo cuadruplo a ejecutar.
        self.IP = 0

    @staticmethod
    def _cargar_constantes(cte):
        """Invierte las tablas del compilador (lexema -> direccion) a la forma
        que necesita la VM (direccion -> valor real) con type-conversion:

          - enteros:   int(lex)    "5" -> 5,   "-3" -> -3
          - flotantes: float(lex)  "3.14" -> 3.14
          - letreros:  lex sin las comillas que el lexer dejo pegadas
                       '"hola"' -> 'hola'
        """
        m = {}
        for lex, dir_ in cte._ents.items():
            m[dir_] = int(lex)
        for lex, dir_ in cte._floats.items():
            m[dir_] = float(lex)
        for lex, dir_ in cte._letreros.items():
            m[dir_] = lex[1:-1]   # quita el " inicial y final
        return m
    
    def _nuevo_frame(self, nombre_func):
        """Crea un Frame con sus locales/temps PRE-INICIALIZADOS al default por tipo.

        Por que pre-inicializar (no lazy):
        - El 'phantom temporal' de las funciones tipadas (Etapa 4) nunca es
            escrito en runtime (los retornos estan diferidos). Si lo dejas
            ausente, leer() crashea. Con default 0, degrada limpiamente.
        - Variables locales sin asignacion previa tambien degradan a default.
        """
        f = Frame(nombre_func)
        info = self.func_dir[nombre_func]
        if info.recursos is None:
            # Caso defensivo: no deberia pasar despues del snapshot del Chunk 1.
            return f
        for (seg, tipo), cuantos in info.recursos.items():
            destino = f.locales if seg == "local" else f.temps
            base = AsignadorMemoria._BASE[(seg, tipo)]   # <-- directo del compilador
            for i in range(cuantos):
                destino[base + i] = _DEFAULTS[tipo]
        return f

    def _frame_actual(self):
        """Top de la pila de frames de ejecucion."""
        return self.pila_frames[-1]

    def leer(self, direccion):
        """Lee el valor en una direccion virtual. Routing por segmento.

        - global / cte: memoria correspondiente
        - local / temp: del FRAME ACTUAL (top de pila_frames)
        """
        seg_tipo = _segmento_y_tipo(direccion)
        if seg_tipo is None:
            raise RuntimeError(f"VM: direccion invalida al leer: {direccion}")
        seg, tipo = seg_tipo
        if seg == "cte":
            return self.memoria_constantes[direccion]
        if seg == "global":
            return self.memoria_global.get(direccion, _DEFAULTS[tipo])
        f = self._frame_actual()
        store = f.locales if seg == "local" else f.temps
        return store.get(direccion, _DEFAULTS[tipo])

    def escribir(self, direccion, valor):
        """Escribe un valor en una direccion virtual. Routing por segmento.

        NO USAR PARA PARAM. PARAM debe escribir en el prep frame (callee),
        no en el frame actual (caller). Para eso usa escribir_en_prep().
        """
        seg_tipo = _segmento_y_tipo(direccion)
        if seg_tipo is None:
            raise RuntimeError(f"VM: direccion invalida al escribir: {direccion}")
        seg, tipo = seg_tipo
        if seg == "cte":
            raise RuntimeError(f"VM: intento de escribir a una constante: {direccion}")
        if seg == "global":
            self.memoria_global[direccion] = valor
            return
        f = self._frame_actual()
        store = f.locales if seg == "local" else f.temps
        store[direccion] = valor

    def escribir_en_prep(self, direccion, valor):
        """Especial para PARAM: escribe en el TOP de pila_prep (el callee aun
        no activo), no en el frame actual (el caller).

        Por que importa: si caller y callee comparten un numero de direccion
        (p.ej. h tiene 'a' en 5000, f tiene un param tambien en 5000), pasar
        por el escribir() generico pisaria la 'a' de h. Aqui escribes EXPLICITO
        al prep que despues activara GOSUB.
        """
        if not self.pila_prep:
            raise RuntimeError("VM: PARAM sin ERA previo (pila_prep vacia)")
        seg_tipo = _segmento_y_tipo(direccion)
        if seg_tipo is None:
            raise RuntimeError(f"VM: direccion invalida en PARAM: {direccion}")
        seg, _tipo = seg_tipo
        if seg != "local":
            raise RuntimeError(f"VM: PARAM destino no es local: {direccion}")
        self.pila_prep[-1].locales[direccion] = valor
        
        
    def ejecutar(self):
        """Loop principal de despacho. Se implementa en el Chunk 3."""
        """Loop principal de despacho.

        Lee el cuadruplo en self.IP, lo despacha por opcode, y avanza.

        Convencion del IP:
          - opcodes que SALTAN (GOTO/GOTOF/GOSUB/ENDFUNC): setean self.IP y
            hacen 'continue' para no caer en el IP += 1 del final.
          - el resto cae a self.IP += 1 al final del while.

        Limite anti-runaway: 1000 frames simultaneos (~recursion infinita).
        """
        LIMITE_FRAMES = 1000

        while self.IP < len(self.fila):
            q = self.fila[self.IP]
            op = q.op

            # --- Aritmeticos ---
            if op == "+":
                self.escribir(q.resultado, self.leer(q.opIzq) + self.leer(q.opDer))
            elif op == "-":
                self.escribir(q.resultado, self.leer(q.opIzq) - self.leer(q.opDer))
            elif op == "*":
                self.escribir(q.resultado, self.leer(q.opIzq) * self.leer(q.opDer))
            elif op == "/":
                izq = self.leer(q.opIzq)
                der = self.leer(q.opDer)
                if der == 0:
                    raise RuntimeError(f"VM: division por cero (IP={self.IP})")
                # int/int -> // (truncated), si alguno es float -> /.
                # Coherente con el cubo: int/int da int; cualquier float da float.
                if isinstance(izq, int) and isinstance(der, int) \
                   and not isinstance(izq, bool) and not isinstance(der, bool):
                    self.escribir(q.resultado, izq // der)
                else:
                    self.escribir(q.resultado, izq / der)

            # --- Relacionales ---
            elif op == "<":
                self.escribir(q.resultado, int(self.leer(q.opIzq) <  self.leer(q.opDer)))
            elif op == ">":
                self.escribir(q.resultado, int(self.leer(q.opIzq) >  self.leer(q.opDer)))
            elif op == "==":
                self.escribir(q.resultado, int(self.leer(q.opIzq) == self.leer(q.opDer)))
            elif op == "!=":
                self.escribir(q.resultado, int(self.leer(q.opIzq) != self.leer(q.opDer)))

            # --- Asignacion ---
            elif op == "=":
                # Cubo permite ent->flot (ensanchamiento). Copiamos el valor tal
                # cual; los rangos virtuales ya garantizan tipos compatibles.
                self.escribir(q.resultado, self.leer(q.opIzq))

            # --- Salida ---
            elif op == "PRINT":
                # q.resultado es la direccion del valor o letrero a imprimir.
                # leer() resuelve constante/global/local/temp segun el rango.
                print(self.leer(q.resultado))

            # --- Saltos ---
            elif op == "GOTO":
                self.IP = q.resultado
                continue
            elif op == "GOTOF":
                if not self.leer(q.opIzq):
                    self.IP = q.resultado
                    continue

            # --- Funciones ---
            elif op == "ERA":
                # Reserva un frame para el callee (no lo activa todavia).
                # Va a la PILA de prep para soportar f(g(x)).
                self.pila_prep.append(self._nuevo_frame(q.resultado))
            elif op == "PARAM":
                # Lee del frame ACTUAL (caller), escribe en el TOP de pila_prep
                # (callee aun no activo). NO usar self.escribir() aqui!
                self.escribir_en_prep(q.resultado, self.leer(q.opIzq))
            elif op == "GOSUB":
                # Activa el prep frame y salta al cuad_inicio de la funcion.
                prep = self.pila_prep.pop()
                prep.ip_retorno = self.IP + 1   # a donde regresar al ENDFUNC
                self.pila_frames.append(prep)
                if len(self.pila_frames) > LIMITE_FRAMES:
                    raise RuntimeError(
                        f"VM: stack overflow (>{LIMITE_FRAMES} frames) "
                        f"al llamar '{q.opIzq}' (recursion infinita?)"
                    )
                self.IP = q.resultado
                continue
            elif op == "ENDFUNC":
                # Cierra el frame actual y restaura el IP de retorno.
                frame = self.pila_frames.pop()
                self.IP = frame.ip_retorno
                continue

            else:
                raise RuntimeError(f"VM: opcode desconocido '{op}' (IP={self.IP})")

            # Caso por defecto: avanza al siguiente cuadruplo.
            # Los opcodes de salto ya hicieron 'continue' arriba.
            self.IP += 1
