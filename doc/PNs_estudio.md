# Profundización de los 23 PNs — Cheat sheet personal

Esta es la versión detallada de la sección §13 del docx de entrega. Incluye fichas completas (8 campos por PN) y diagramas ASCII de flujo antes/después. Pensada como referencia rápida para defensa del proyecto Patito.

El docx oficial (versión 'screenshot') tiene los mismos 23 PNs en formato visual compacto (gramática + arrows + bullets). Este MD es el complemento técnico denso.

---

## Grupo A — PNs estructurales

### PN-1 — `enterPrograma(ctx)`  _(semantico.py:219, Etapa 2)_

**Trigger:** Dispara cuando ANTLR entra al nodo raiz 'programa' (programa ID ; vars? funcs* principal cuerpo). Es el primer PN que se ejecuta en cualquier compilacion.

| Campo | Valor |
|---|---|
| Línea | semantico.py:219 |
| Etapa | 2 |
| Lee del estado | ctx.ID() — el nombre del programa |
| Modifica | nombre_programa, func_dir, scope_actual, gen.idx_goto_main |
| Emite cuádruplos | 1 cuadruplo: (GOTO, _, _, None) — destino pendiente (lo backpatchea enterCuerpo) |
| Pila al cerrar | ninguna pila de expresion tocada |
| **Esencia** | Reserva el FuncInfo del programa y emite el GOTO inicial que apuntara al main. |

**Flujo:**

```
ANTES                                 DESPUES
-----                                 -------
func_dir = {}                         func_dir = {"demo": FuncInfo(programa)}
scope_actual = None                   scope_actual = func_dir["demo"]
nombre_programa = None                nombre_programa = "demo"
gen.fila = []                         gen.fila = [(GOTO, _, _, None)]
gen.idx_goto_main = None              gen.idx_goto_main = 0

El cuadruplo 0 (GOTO con destino None) queda pendiente; se
rellena en enterCuerpo cuando ANTLR entra al cuerpo de main.
```

### PN-1B — `exitPrograma(ctx)`  _(semantico.py:230, Etapa 5)_

**Trigger:** Dispara cuando ANTLR sale del nodo raiz 'programa'. Es el ultimo PN que se ejecuta antes de que el compilador entregue la fila a la VM.

| Campo | Valor |
|---|---|
| Línea | semantico.py:230 |
| Etapa | 5 |
| Lee del estado | self.func_dir[self.nombre_programa], self.mem._contadores |
| Modifica | func_dir[programa].recursos |
| Emite cuádruplos | ninguno |
| Pila al cerrar | ninguna pila tocada |
| **Esencia** | Snapshot final: captura cuantos slots usa main para que la VM reserve el frame inicial. |

**Flujo:**

```
ANTES                                 DESPUES
-----                                 -------
programa.recursos = None              programa.recursos = {
                                        ('local',    'entero'):   0,
                                        ('local',    'flotante'): 0,
                                        ('local',    'bool'):     0,
                                        ('temp',     'entero'):   3,
                                        ('temp',     'flotante'): 0,
                                        ('temp',     'bool'):     1,
                                      }

NOTA: este snapshot es para MAIN. Para funciones, el snapshot
ocurre en exitFuncs antes del switch de scope.
```

### PN-2 — `enterFuncs(ctx)`  _(semantico.py:239, Etapa 2)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'funcs' (cada funcion declarada antes de 'principal'). Si hay 3 funciones, se llama 3 veces.

| Campo | Valor |
|---|---|
| Línea | semantico.py:239 |
| Etapa | 2 |
| Lee del estado | ctx.ID(), ctx.tipoFunc(), ctx.paramsOpc() |
| Modifica | func_dir[nombre], scope_actual, mem._contadores (reset), scope.variables, scope.params; o errores |
| Emite cuádruplos | ninguno (asigna direcciones de params pero no emite cuadruplos) |
| Pila al cerrar | ninguna pila de expresion tocada |
| **Esencia** | Abre el scope de la funcion: registra signatura, resetea contadores, registra parametros con direcciones locales. |

**Flujo:**

```
ANTES                                  DESPUES
-----                                  -------
func_dir = {"demo": ...}              func_dir = {"demo":..., "sumar": FuncInfo(entero)}
scope_actual = func_dir["demo"]       scope_actual = func_dir["sumar"]
mem._contadores = (con valores         mem._contadores = (reseteado a _BASE para
  de la fase anterior)                  los segmentos local y temp)
sumar.cuad_inicio = None              sumar.cuad_inicio = len(gen.fila) = 1

Por cada param (a, b) declarado:
  scope.variables["a"] = VarInfo(entero, dir=5000)
  scope.params.append(ParamInfo("a", entero, 5000))
  (similar para b en dir 5001)

VALIDACIONES:
  - Nombre = nombre del programa  -> error 'no puede tener el mismo nombre'
  - Funcion ya declarada         -> error 'ya esta declarada'
  Ambos casos prenden en_func_duplicada y abortan el resto.
```

### PN-3 — `exitFuncs(ctx)`  _(semantico.py:282, Etapa 2)_

**Trigger:** Dispara cuando ANTLR sale de un nodo 'funcs'. Cierra el cuerpo de la funcion y prepara la transicion a la siguiente (o a main).

| Campo | Valor |
|---|---|
| Línea | semantico.py:282 |
| Etapa | 2 |
| Lee del estado | self.scope_actual, self.mem._contadores |
| Modifica | scope_actual.recursos, scope_actual (al programa) |
| Emite cuádruplos | 1 cuadruplo: (ENDFUNC, _, _, _) |
| Pila al cerrar | ninguna pila tocada |
| **Esencia** | Cierra el scope: snapshot recursos ANTES del switch, emite ENDFUNC, regresa scope al programa. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
scope_actual = func_dir["sumar"]        scope_actual = func_dir["demo"]
sumar.recursos = None                   sumar.recursos = {
                                          ('local','entero'):   2,    # a, b
                                          ('temp', 'entero'):   1,    # a + b
                                          ...
                                        }
gen.fila = [..., 7]                     gen.fila = [..., 7, (ENDFUNC, _, _, _)]

ORDEN CRITICO:
  1. snapshot recursos                ← scope_actual aun apunta a la funcion
  2. emite ENDFUNC
  3. switch scope al programa         ← snapshot HUBIERA capturado al
                                       programa equivocado si se invierte
```

### PN-4E — `enterCuerpo(ctx)`  _(semantico.py:299, Etapa 4)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'cuerpo'. Se llama muchas veces (uno por funcion, uno por main, uno por cuerpo de si/mientras). Solo actua si el padre es ProgramaContext (i.e. es el cuerpo de main).

| Campo | Valor |
|---|---|
| Línea | semantico.py:299 |
| Etapa | 4 |
| Lee del estado | ctx.parentCtx |
| Modifica | mem._contadores (reset), gen.fila[gen.idx_goto_main].resultado (backpatch) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | ninguna pila tocada |
| **Esencia** | Solo para main: limpia contadores y resuelve el GOTO inicial. Para otros cuerpos, NO HACE NADA. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
(suponer 8 cuadruplos generados por      mem._contadores = (reseteado: temp y local
 funciones anteriores)                    arrancan en sus _BASE de nuevo)
gen.fila[0] = (GOTO, _, _, None)        gen.fila[0] = (GOTO, _, _, 8)
mem._contadores[('temp','entero')] =     
  9003 (heredado de la ultima funcion)   

PORQUE EL RESET: si main hereda contadores, sus temporales
arrancan en dirs altos. La VM los buscaria en main.temps en
indices >= 9003 — funciona, pero rompe la asuncion de que
cada frame parte sus contadores en _BASE. Mejor resetear.

PORQUE EL BACKPATCH: el GOTO emitido en enterPrograma apuntaba
a None. Ahora sabemos que el primer cuadruplo de main es el
len(fila) actual; backpatch lo deja apuntando alli.
```

### PN-4 — `enterDeclaracion(ctx)`  _(semantico.py:312, Etapa 2)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'declaracion' (var X, Y, Z : tipo ;). Puede haber multiples nombres por declaracion.

| Campo | Valor |
|---|---|
| Línea | semantico.py:312 |
| Etapa | 2 |
| Lee del estado | ctx.tipo(), ctx.idLista() (aplanado), self.scope_actual |
| Modifica | scope.variables (por cada ID), mem._contadores (incrementa) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | ninguna pila tocada |
| **Esencia** | Por cada ID en la idLista, valida no-duplicado, asigna direccion virtual y registra en scope.variables. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
scope.variables = {}                    scope.variables = {
                                          "i": VarInfo(entero, linea=2, dir=1000),
                                          "s": VarInfo(entero, linea=2, dir=1001),
                                        }
mem._contadores[("global","entero")]    mem._contadores[("global","entero")]
  = 1000                                  = 1002

DECISION GLOBAL VS LOCAL:
  es_global = (scope_actual is func_dir[nombre_programa])
  Si SI -> nueva_global(tipo)  -> dir en 1000-3999
  Si NO -> nueva_local(tipo)   -> dir en 5000-7999

ERROR: si el nombre ya esta en scope.variables, se reporta
       'variable X ya esta declarada' y se sigue con el siguiente ID.
```

## Grupo B — Expresiones lineales

### PN3-A — `exitFactor(ctx)`  _(semantico.py:338, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale de un nodo 'factor' (lo atomico de una expresion: ID, cte, (expr), o llamada). Cada hoja de la expresion termina aqui.

| Campo | Valor |
|---|---|
| Línea | semantico.py:338 |
| Etapa | 3 |
| Lee del estado | ctx.signoOpc(), ctx.ID(), ctx.cte() |
| Modifica | pila_operandos, pila_tipos (ambas push), gen.fila (solo si signo unario) |
| Emite cuádruplos | 0 o 1 cuadruplo: si hay menos unario sobre ID, emite (-, 0, dir_id, temp) |
| Pila al cerrar | pila_operandos += [dir_factor]; pila_tipos += [tipo_factor] |
| **Esencia** | Empuja la direccion y tipo del operando a las pilas. Maneja constantes (con dedup) y signo unario. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [...]                  pila_operandos = [..., dir_factor]
pila_tipos     = [...]                  pila_tipos     = [..., tipo_factor]

CASOS:
  factor = ID 'x':
    busca v = _buscar_var('x'); si None -> error + push (None,error)
    sin signo -:  push (v.direccion, v.tipo)
    con signo -:  emite (-, dir_0, v.dir, T); push (T, v.tipo)

  factor = CTE_ENT '5':
    cte.direccion_de_numerica('5','entero') = 13000 (dedup)
    push (13000, 'entero')

  factor = CTE_FLOT '3.14':
    cte.direccion_de_numerica('3.14','flotante') = 14000
    push (14000, 'flotante')

  factor = (expresion):  ya empujo el resultado (nada que hacer)
  factor = llamada:      enter/exitLlamada ya empujaron el temporal
```

### PN3-B1 — `enterExp(ctx)`  _(semantico.py:397, Etapa 3)_

**Trigger:** Dispara cuando ANTLR entra a una subregla 'exp' (parte de la expresion que tiene + o -). Si el exp no tiene ningun + ni -, este PN no hace nada (return temprano).

| Campo | Valor |
|---|---|
| Línea | semantico.py:397 |
| Etapa | 3 |
| Lee del estado | ctx.MAS(), ctx.MENOS() |
| Modifica | pila_operadores (push) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | pila_operadores += [op] |
| **Esencia** | Apila el operador + o - para que exitExp lo combine con sus dos operandos. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operadores = [...]                 pila_operadores = [..., '+' o '-']

Patron emparejado con exitExp:
  enter empuja el operador (lado izq del PN ya en pila_operandos)
  ...el lado der se procesa (puede ser otro exp o un termino)...
  exit pop el operador + 2 operandos -> emite -> push temp
```

### PN3-B2 — `exitExp(ctx)`  _(semantico.py:405, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale de una subregla 'exp'. Si el exp no tenia + ni - (return temprano), no opera; los dos operandos siguen en pila para el nivel padre.

| Campo | Valor |
|---|---|
| Línea | semantico.py:405 |
| Etapa | 3 |
| Lee del estado | ctx.MAS(), ctx.MENOS(), pila_operandos[-2:], pila_tipos[-2:], pila_operadores[-1] |
| Modifica | pila_operandos (-2, +1), pila_tipos (-2, +1), pila_operadores (-1), gen.fila (+1) |
| Emite cuádruplos | 1 cuadruplo: (+, dA, dB, T) o (-, dA, dB, T) con T = nuevo_temporal del tipo resultado |
| Pila al cerrar | pila_operandos = [..., T_res]; pila_tipos = [..., tipo_res]; pila_operadores = [..., sin el +/-] |
| **Esencia** | Pop 2 operandos + 1 operador, consulta cubo semantico, emite cuadruplo binario, push del temporal resultado. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., A, B]            pila_operandos = [..., T]
pila_tipos     = [..., tA, tB]          pila_tipos     = [..., tR]
pila_operadores = [..., '+']            pila_operadores = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (+, A, B, T)]

PROCESO INTERNO (pop_y_emitir_binario):
  1. pop op = '+', d_der = B, t_der = tB, d_izq = A, t_izq = tA
  2. si t_izq o t_der es 'error' -> propaga (push None,'error')
  3. cubo(op, tA, tB) = tR (o None si no compatible -> error tipos)
  4. T = mem.nuevo_temporal(tR)
  5. emite (op, A, B, T)
  6. push (T, tR)
```

### PN3-C1 — `enterTermino(ctx)`  _(semantico.py:419, Etapa 3)_

**Trigger:** Igual que enterExp pero para 'termino' (la parte de la expresion que tiene * o /). Si el termino no tiene * ni /, no opera.

| Campo | Valor |
|---|---|
| Línea | semantico.py:419 |
| Etapa | 3 |
| Lee del estado | ctx.POR(), ctx.ENTRE() |
| Modifica | pila_operadores (push) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | pila_operadores += ['*' o '/'] |
| **Esencia** | Apila el operador * o / para que exitTermino lo combine. La separacion exp/termino implementa precedencia. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operadores = [...]                 pila_operadores = [..., '*' o '/']

POR QUE EXISTEN exp Y termino POR SEPARADO:
  La gramatica separa:  expresion -> exp ((<|>|==|!=) exp)?
                        exp       -> termino ((+ | -) termino)*
                        termino   -> factor ((* | /) factor)*

  Asi *,/ enlazan mas que +,-, y +,- enlazan mas que <,>,==,!=.
  Es la implementacion gramatical clasica de precedencia.
```

### PN3-C2 — `exitTermino(ctx)`  _(semantico.py:427, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale de un termino. Si no hay * ni /, no opera. Internamente es identico a exitExp solo cambia el operador.

| Campo | Valor |
|---|---|
| Línea | semantico.py:427 |
| Etapa | 3 |
| Lee del estado | ctx.POR(), ctx.ENTRE(), pilas |
| Modifica | pila_operandos, pila_tipos, pila_operadores, gen.fila |
| Emite cuádruplos | 1 cuadruplo: (*, dA, dB, T) o (/, dA, dB, T) |
| Pila al cerrar | pila_operandos = [..., T_res]; pila_tipos = [..., tipo_res] |
| **Esencia** | Identico a exitExp pero para * y /. La separacion en dos PNs (vs uno general) reduce ramas if dentro del PN. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., A, B]            pila_operandos = [..., T]
pila_tipos     = [..., tA, tB]          pila_tipos     = [..., tR]
pila_operadores = [..., '*']            pila_operadores = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (*, A, B, T)]

CUBO PARA / :
  entero / entero -> entero  (la VM usa // de Python)
  entero / flotante -> flotante  (la VM usa /)
  flotante / X -> flotante
  En runtime: si B == 0, RuntimeError('VM: division por cero')
```

### PN3-D1 — `enterRelOpc(ctx)`  _(semantico.py:441, Etapa 3)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'relOpc' (la parte opcional 'opRel expresion' del nivel de expresion). Solo opera si el opRel esta presente.

| Campo | Valor |
|---|---|
| Línea | semantico.py:441 |
| Etapa | 3 |
| Lee del estado | ctx.opRel() y sus tokens MAYOR, MENOR, DISTINTO, IGUAL2 |
| Modifica | pila_operadores (push) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | pila_operadores += ['<', '>', '!=', '=='] |
| **Esencia** | Apila el operador relacional para que exitExpresion lo combine. Identifica cual de los 4 operadores (no es solo MENOR). |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operadores = [...]                 pila_operadores = [..., '<' | '>' | '==' | '!=']

Patito tiene 4 operadores relacionales (no 6 como C):
  < (MENOR)   > (MAYOR)   == (IGUAL2)   != (DISTINTO)

NO tiene  <= ni >= (decision del lenguaje).
```

### PN3-D2 — `exitExpresion(ctx)`  _(semantico.py:456, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale del nodo top de la expresion (no exp, no termino, no factor — el nodo raiz). Es el PN mas multifacetico: emite relacional + despacha al contexto padre.

| Campo | Valor |
|---|---|
| Línea | semantico.py:456 |
| Etapa | 3 |
| Lee del estado | ctx.relOpc(), pilas, ctx.parentCtx |
| Modifica | pilas (si emit relacional); luego invoca _manejar_condicion o _manejar_argumento segun el padre |
| Emite cuádruplos | 0 o 1 cuadruplo relacional (<, >, ==, !=); puede emitir mas via los helpers a los que despacha |
| Pila al cerrar | pila_operandos / pila_tipos posiblemente con el temp bool del relacional |
| **Esencia** | Cierra la expresion: si hay relOpc emite cuadruplo bool; luego SI el padre es condicion/argumento, llama al helper correspondiente. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., A, B]            pila_operandos = [..., T]   (si hay relOpc)
pila_tipos     = [..., tA, tB]          pila_tipos     = [..., 'bool']
pila_operadores = [..., '<']            pila_operadores = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (<, A, B, T)]

LUEGO, EL DESPACHO POR CONTEXTO PADRE:
  parent = ctx.parentCtx
  if parent es CondicionContext o CicloContext:
      -> _manejar_condicion (emite GOTOF, push a pila_saltos)
  elif parent es ArgListaContext o ArgRestoContext:
      -> _manejar_argumento (empareja con param k, emite PARAM)
  else: queda en pila para que exitAsigna o exitImpElem lo consuma
```

### PN3-E — `exitAsigna(ctx)`  _(semantico.py:478, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale de un nodo 'asigna' (ID = expresion ;). El RHS ya fue evaluado y dejado en pila.

| Campo | Valor |
|---|---|
| Línea | semantico.py:478 |
| Etapa | 3 |
| Lee del estado | ctx.ID(), self._buscar_var(nombre), pila_operandos[-1], pila_tipos[-1] |
| Modifica | pila_operandos (pop), pila_tipos (pop) |
| Emite cuádruplos | 1 cuadruplo: (=, dir_rhs, _, dir_destino) |
| Pila al cerrar | pila_operandos = [...]; pila_tipos = [...] (ambas decrecen en 1) |
| **Esencia** | Consume el RHS de la pila, valida tipo con cubo, emite (=) hacia la direccion del LHS. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., dir_rhs]         pila_operandos = [...]
pila_tipos     = [..., tipo_rhs]        pila_tipos     = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (=, dir_rhs, _, v.direccion)]

VALIDACIONES:
  1. _buscar_var(nombre):
       not encontrado -> error 'variable X usada sin declarar'
                          + pop del rhs (limpia pila) + return
  2. cubo('=', v.tipo, tipo_rhs):
       None -> error 'tipos incompatibles en asignacion'
  3. propagacion: si tipo_rhs == 'error', no se reporta dup (ya se reporto antes)
```

### PN3-F — `exitImpElem(ctx)`  _(semantico.py:500, Etapa 3)_

**Trigger:** Dispara cuando ANTLR sale de un 'impElem' (un elemento individual dentro de escribe(...). Puede ser LETRERO o una expresion).

| Campo | Valor |
|---|---|
| Línea | semantico.py:500 |
| Etapa | 3 |
| Lee del estado | ctx.LETRERO() o ctx.expresion(); si expresion: top de pila |
| Modifica | pila_operandos (pop si expresion), pila_tipos (pop si expresion) |
| Emite cuádruplos | 1 cuadruplo: (PRINT, _, _, dir) |
| Pila al cerrar | decrece en 1 si era expresion (LETRERO no afecta pilas) |
| **Esencia** | Emite un PRINT por cada elemento del escribe(...). Para LETRERO empuja a tabla de letreros; para expresion consume top. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., d_expr]          pila_operandos = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (PRINT, _, _, d_expr)]

CASO LETRERO:
  lex = '\"hola\"' (con comillas)
  dir = cte.direccion_de_letrero(lex)  -> p.ej. 15000 (dedup)
  emite (PRINT, _, _, 15000)

CASO EXPRESION:
  if pilas_operandos_vacia: no hace nada (defensivo)
  d_expr = top_operando, pop_operando
  emite (PRINT, _, _, d_expr)

escribe(a, b, "hola") emite 3 PRINTs separados, en orden.
```

## Grupo C — Control de flujo

### PN-4A — `_manejar_condicion(ctx)`  _(semantico.py:514, Etapa 4)_

**Trigger:** NO es un listener ANTLR — es un helper INVOCADO por exitExpresion cuando detecta que el padre de la expresion es CondicionContext o CicloContext. La 'condicion' ya termino de evaluarse.

| Campo | Valor |
|---|---|
| Línea | semantico.py:514 |
| Etapa | 4 |
| Lee del estado | pila_operandos[-1], pila_tipos[-1] |
| Modifica | pila_operandos (pop), pila_tipos (pop), pila_saltos (push), gen.fila (+1) |
| Emite cuádruplos | 1 cuadruplo: (GOTOF, dir_cond, _, None) — destino pendiente |
| Pila al cerrar | pila_operandos / pila_tipos decrecen en 1; pila_saltos crece en 1 |
| **Esencia** | Toma el bool del top, emite GOTOF con destino pendiente, recuerda el indice del GOTOF en pila_saltos para backpatch. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., d_cond]          pila_operandos = [...]
pila_tipos     = [..., 'bool']          pila_tipos     = [...]
pila_saltos    = [...]                  pila_saltos    = [..., idx_gotof]
gen.fila = [..., I]                     gen.fila = [..., I, (GOTOF, d_cond, _, None)]
                                        idx_gotof = I (recien emitido)

INVARIANTE CRITICO:
  SIEMPRE empuja exactamente 1 indice a pila_saltos, porque
  exitCondicion/exitCiclo hacen pop INCONDICIONAL. Si la condicion
  tuvo error (tipo no-bool), AUN ASI emitimos GOTOF y push, para
  no desbalancear la pila — si no, exitCiclo popearia basura.

  El error 'la condicion debe ser tipo bool' se reporta, pero NO
  se aborta el flujo de control PN.
```

### PN-4F — `enterCiclo(ctx)`  _(semantico.py:541, Etapa 4)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'ciclo' (MIENTRAS (expr) HAZ cuerpo). Marca el 'punto de regreso' del ciclo ANTES de que la condicion se evalue.

| Campo | Valor |
|---|---|
| Línea | semantico.py:541 |
| Etapa | 4 |
| Lee del estado | len(gen.fila) — el proximo indice de cuadruplo |
| Modifica | pila_saltos (push) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | pila_saltos = [..., I_inicio] |
| **Esencia** | Recuerdo donde empieza la condicion para volver aqui al final del cuerpo. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_saltos = [...]                     pila_saltos = [..., I_inicio]
gen.fila = [.., 0, 1, .., I-1]          gen.fila = [.., 0, 1, .., I-1]  (no emit)
                                        I_inicio = len(fila) = I

Despues entra la condicion -> exitExpresion -> _manejar_condicion
  push idx_gotof a pila_saltos
Asi pila_saltos = [..., I_inicio, idx_gotof]
Cuando termina el cuerpo, exitCiclo pop ambos.
```

### PN-4G — `exitCiclo(ctx)`  _(semantico.py:547, Etapa 4)_

**Trigger:** Dispara cuando ANTLR sale del ciclo (cuerpo del mientras ya emitio sus cuadruplos). Cierra el ciclo emitiendo el GOTO de regreso y backpatcheando el GOTOF de la condicion.

| Campo | Valor |
|---|---|
| Línea | semantico.py:547 |
| Etapa | 4 |
| Lee del estado | pila_saltos[-1], pila_saltos[-2] |
| Modifica | pila_saltos (pop x2), gen.fila (+1), gen.fila[idx_gotof].resultado (backpatch) |
| Emite cuádruplos | 1 cuadruplo: (GOTO, _, _, I_inicio) |
| Pila al cerrar | pila_saltos decrece en 2 (queda vacia para este ciclo) |
| **Esencia** | Pop GOTOF + I_inicio; emite GOTO al inicio (vuelve a evaluar la cond); backpatch GOTOF para que apunte despues del GOTO. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_saltos = [.., I_cond, I_gotof]     pila_saltos = [...]
gen.fila = [.., I_cond:(<,..), ...,    gen.fila = [.., I_cond:(<,..), ...,
            I_body, ..., I_endbody]                 I_body, ..., I_endbody,
                                                    (GOTO, _, _, I_cond)]
                                       gen.fila[I_gotof].resultado = len(fila)
                                       (apunta al siguiente del GOTO)

ORDEN:
  1. falso   = pila_saltos.pop()   # idx del GOTOF
  2. retorno = pila_saltos.pop()   # I_inicio
  3. emite_goto_a(retorno)         # GOTO de regreso al len(fila)
  4. backpatch(falso, len(fila))   # GOTOF -> tras el GOTO
```

### PN-4H — `enterSinoOpc(ctx)`  _(semantico.py:556, Etapa 4)_

**Trigger:** Dispara cuando ANTLR entra al nodo opcional 'sinoOpc' del 'si'. Si la rama es epsilon (no hay 'sino'), no hace nada. Si SI hay 'sino', necesita brincar el cuerpo del sino para que el cuerpo del 'si' no caiga en cascada.

| Campo | Valor |
|---|---|
| Línea | semantico.py:556 |
| Etapa | 4 |
| Lee del estado | ctx.SINO(), pila_saltos[-1] |
| Modifica | pila_saltos (pop, push), gen.fila (+1), gen.fila[idx_gotof].resultado (backpatch) |
| Emite cuádruplos | 1 cuadruplo (si hay sino): (GOTO, _, _, None) — destino pendiente |
| Pila al cerrar | pila_saltos: pop el GOTOF, push el nuevo GOTO; misma altura |
| **Esencia** | Si hay sino: el cuerpo del si termino — emite GOTO para brincar el sino, backpatch del GOTOF al sino, push del GOTO para que exitCondicion lo cierre. |

**Flujo:**

```
ANTES (cuerpo del 'si' termino)          DESPUES
-----                                   -------
pila_saltos = [..., I_gotof_si]         pila_saltos = [..., I_goto_brinca_sino]
gen.fila = [.., I_gotof_si:(GOTOF,..),  gen.fila = [.., I_gotof_si:(GOTOF, c, _,
            ...cuerpo_si...,                                len(fila)+1),
            I_end_cuerpo_si]                       ...cuerpo_si..., (GOTO, _, _, None)]

ORDEN:
  1. falso = pila_saltos.pop()      # GOTOF del 'si'
  2. idx_goto = emitir_goto()       # GOTO que brinca el cuerpo del sino
  3. pila_saltos.push(idx_goto)     # exitCondicion lo cerrara
  4. backpatch(falso, len(fila))    # GOTOF -> inicio del sino

RAMA EPSILON: si no hay SINO, return temprano. pila_saltos queda
             con el GOTOF original; exitCondicion lo backpatcheara.
```

### PN-4I — `exitCondicion(ctx)`  _(semantico.py:566, Etapa 4)_

**Trigger:** Dispara cuando ANTLR sale de un nodo 'condicion' (SI (expr) cuerpo sinoOpc ;). Cierra el salto pendiente que dejaron _manejar_condicion (si sin sino) o enterSinoOpc (si con sino).

| Campo | Valor |
|---|---|
| Línea | semantico.py:566 |
| Etapa | 4 |
| Lee del estado | pila_saltos[-1] |
| Modifica | pila_saltos (pop), gen.fila[indice].resultado (backpatch) |
| Emite cuádruplos | ninguno |
| Pila al cerrar | pila_saltos decrece en 1 (queda como estaba antes del si) |
| **Esencia** | Pop del unico salto pendiente y backpatch al final del si — sea el GOTOF (sin sino) o el GOTO (con sino). |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_saltos = [..., I_pendiente]        pila_saltos = [...]
gen.fila[I_pendiente].resultado = None  gen.fila[I_pendiente].resultado = len(fila)

EL SALTO ES POLIMORFICO:
  Si NO hubo sino: I_pendiente es el GOTOF de _manejar_condicion.
                   Apunta despues del cuerpo del 'si' (fin de si).
  Si SI hubo sino: I_pendiente es el GOTO de enterSinoOpc.
                   Apunta despues del cuerpo del 'sino' (fin del condicion).
  En ambos casos, len(fila) actual es exactamente ese 'despues'.
```

## Grupo D — Llamadas a funciones

### PN-4B — `enterLlamada(ctx)`  _(semantico.py:578, Etapa 4)_

**Trigger:** Dispara cuando ANTLR entra a un nodo 'llamada' (ID(args)). Valida la signatura, emite ERA y empuja contexto para emparejar argumentos con parametros.

| Campo | Valor |
|---|---|
| Línea | semantico.py:578 |
| Etapa | 4 |
| Lee del estado | ctx.ID(), self.func_dir |
| Modifica | pila_llamadas (push contexto), gen.fila (+1 si valida) |
| Emite cuádruplos | 1 cuadruplo (si valida): (ERA, _, _, nombre) |
| Pila al cerrar | pila_llamadas += [{'valida':bool, 'func':FuncInfo, 'nombre':str, 'n':0, 'linea':int}] |
| **Esencia** | Verifica funcion existe; emite ERA (reservar frame); apila contexto (para soportar llamadas anidadas). |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_llamadas = [...]                   pila_llamadas = [..., contexto]
gen.fila = [..., 7]                     gen.fila = [..., 7, (ERA, _, _, 'sumar')]

CONTEXTO empujado:
  {
    "valida":  True / False,            # paso validaciones?
    "func":    FuncInfo o None,         # la funcion en cuestion
    "nombre":  'sumar',                 # para mensajes de error
    "n":       0,                       # # de argumentos ya vistos
    "linea":   12,                      # para localizar errores
  }

VALIDACIONES:
  - nombre not in func_dir       -> error 'funcion X no declarada'
  - nombre == nombre_programa    -> error idem (no se puede llamar al programa)
  En ambos casos se push contexto invalido para mantener balance
  con exitLlamada (que SIEMPRE pop).
```

### PN-4C — `_manejar_argumento(ctx)`  _(semantico.py:603, Etapa 4)_

**Trigger:** NO es listener — es helper INVOCADO por exitExpresion cuando el padre es ArgListaContext o ArgRestoContext. Un argumento de la llamada acaba de evaluarse.

| Campo | Valor |
|---|---|
| Línea | semantico.py:603 |
| Etapa | 4 |
| Lee del estado | pila_llamadas[-1], pila_operandos[-1], pila_tipos[-1] |
| Modifica | pila_operandos (pop), pila_tipos (pop), contexto.n += 1, gen.fila (+1) |
| Emite cuádruplos | 1 cuadruplo (si tipo OK): (PARAM, dir_arg, _, dir_param) |
| Pila al cerrar | pila_operandos / pila_tipos decrecen en 1; contexto.n se incrementa |
| **Esencia** | Toma el arg del top de pila, lo empareja con el param k de la funcion, valida tipo con cubo, emite PARAM. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., d_arg]           pila_operandos = [...]
pila_tipos     = [..., t_arg]           pila_tipos     = [...]
contexto.n = k                          contexto.n = k+1
gen.fila = [..., 7]                     gen.fila = [..., 7, (PARAM, d_arg, _, p.dir)]

EMPAREJAMIENTO:
  idx = contexto.n        # cuantos arg ya vimos
  contexto.n += 1         # SIEMPRE incrementa (para conteo final)
  if contexto invalido o idx >= len(params): return (no emite)
  param = f.params[idx]
  cubo('=', param.tipo, t_arg):
    None -> error 'argumento k de F: esperaba X, recibio Y'
    OK   -> emite (PARAM, d_arg, _, param.direccion)

NOTA: PARAM lee de la variable LOCAL del caller (que ya esta en
      memoria_global o en frame_actual del caller), pero ESCRIBE
      en el frame del callee (pila_prep[-1], no frame actual).
```

### PN-4D — `exitLlamada(ctx)`  _(semantico.py:635, Etapa 4)_

**Trigger:** Dispara cuando ANTLR sale del nodo 'llamada'. Todos los argumentos ya pasaron por _manejar_argumento. Valida el conteo final y emite GOSUB.

| Campo | Valor |
|---|---|
| Línea | semantico.py:635 |
| Etapa | 4 |
| Lee del estado | pila_llamadas.pop(), ctx.parentCtx |
| Modifica | pila_llamadas (pop), gen.fila (+1 si valida), pila_operandos/pila_tipos (push phantom si es factor) |
| Emite cuádruplos | 1 cuadruplo: (GOSUB, nombre, _, cuad_inicio) |
| Pila al cerrar | pila_llamadas decrece en 1; pila_operandos += [phantom] si la llamada esta dentro de una expresion |
| **Esencia** | Pop contexto; valida # argumentos == # params; emite GOSUB; si es factor (dentro de expresion), empuja temporal phantom. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_llamadas = [..., contexto(n=2)]   pila_llamadas = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7, (GOSUB, 'sumar', _,
                                                                  sumar.cuad_inicio)]

Si la llamada esta dentro de una expresion (factor = llamada):
  pila_operandos = [..., d_phantom]
  pila_tipos     = [..., 'entero' (tipo retorno de la funcion)]
  d_phantom = mem.nuevo_temporal('entero')
  (el valor real nunca se escribe en runtime — limitacion 8.1)

VALIDACIONES:
  contexto.n != len(params) -> error 'F espera N args, recibio K'
  factor de funcion 'nula' -> error 'no se puede usar en expresion'

RESUMEN DE EMISIONES DE UNA LLAMADA sumar(3, 4):
  enterLlamada:           (ERA, _, _, 'sumar')
  exitExpresion+helper #1 (PARAM, 13000, _, 5000)  # 3 -> a
  exitExpresion+helper #2 (PARAM, 13001, _, 5001)  # 4 -> b
  exitLlamada:            (GOSUB, 'sumar', _, sumar.cuad_inicio)
  exitLlamada (si factor): (=, sumar.dir_retorno, _, phantom) # NUEVO: post-GOSUB copy
```

> **Nota: PN-4D modificado por feature `retorna`.** Cuando la llamada es factor,
> exitLlamada ahora **también emite** `(=, f.dir_retorno, _, phantom)` justo
> después del GOSUB para copiar el valor de retorno del slot global al phantom
> temporal del caller. El phantom ya no es "fantasma" — efectivamente lleva el
> valor real. Ver PN-Retorno abajo.

---

## Grupo E — Retorno de funciones (1)

### PN-Retorno — `exitRetorno`  _(semantico.py:691, Etapa post-5)_

**Trigger:** ANTLR sale de la regla `retorno : RETORNA expresion PCOMA`. El resultado de la expresion esta en el top de pila_operandos.

| Campo | Valor |
|---|---|
| Línea | semantico.py:691 |
| Etapa | post-5 (extensión que cierra la limitación 8.1) |
| Lee del estado | scope_actual.tipo_retorno, scope_actual.dir_retorno, top de pila_operandos |
| Modifica | pila_operandos (pop), pila_tipos (pop), gen.fila (+2 cuádruplos) |
| Emite cuádruplos | 2 cuádruplos: `(=, dir_expr, _, dir_retorno)` + `(ENDFUNC, _, _, _)` |
| Pila al cerrar | pila_operandos/pila_tipos decrecen en 1 |
| **Esencia** | Copia el valor de la expresión al slot global de retorno y termina la función inmediatamente. |

**Flujo:**

```
ANTES                                   DESPUES
-----                                   -------
pila_operandos = [..., d_expr]          pila_operandos = [...]
pila_tipos     = [..., tipo_expr]       pila_tipos     = [...]
gen.fila = [..., 7]                     gen.fila = [..., 7,
                                                   (=, d_expr, _, dir_retorno),
                                                   (ENDFUNC, _, _, _)]

VALIDACIONES (orden de check):
  1) scope_actual.tipo_retorno == "programa"
       -> error "no se puede usar 'retorna' en el programa principal"
       -> pop defensivo del operando, return temprano
  2) scope_actual.tipo_retorno == "nula"
       -> error "no se puede usar 'retorna' en funcion 'nula' ('NOMBRE')"
       -> pop defensivo, return
  3) cubo("=", tipo_destino, tipo_expr) == None
       -> error "tipo de 'retorna' incompatible con tipo de retorno de la funcion"
  4) propagacion silenciosa si tipo_expr == "error"

DISEÑO ELEGIDO (Design E): "return slot por función".
  - Cada funcion tipada recibe dir_retorno = un slot global unico
    (segmento 17000s para entero, 18000s para flotante).
  - El slot vive en memoria_global (sobrevive frames).
  - retorna E: emite (=, E, _, dir_retorno) + ENDFUNC.
  - Caller post-GOSUB: emite (=, dir_retorno, _, phantom) — la copia inversa.
  - NO HAY OPCODES NUEVOS en la VM. Solo se reusa el =.

POR QUE FUNCIONA CON RECURSION:
  Aunque cada llamada sobrescribe el mismo slot, la VM lee
  inmediatamente despues del GOSUB hacia un phantom único por call site.
  No hay race porque la VM es single-threaded.

POR QUE EL ENDFUNC EXTRA:
  exitFuncs YA emite un ENDFUNC al final del cuerpo. Si retorna
  emite otro ENDFUNC, hay dos ENDFUNCs back-to-back en algunos paths.
  Está OK — el primero popea el frame y la VM nunca alcanza el segundo.
  Para retorna dentro de si/sino, el ENDFUNC del retorna es lo que da
  el early-exit (sin él, ejecucion seguiria al cuerpo despues del si).
```

