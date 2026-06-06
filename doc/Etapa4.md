# Etapa 4 — Generación de código de control de flujo y funciones

**Patito (versión Python).** Esta etapa extiende el generador de cuádruplos de la
Etapa 3 para producir código intermedio de:

1. **Estatutos condicionales** `si` / `sino`
2. **Ciclos** `mientras`
3. **Declaración** e **invocación de funciones** (`ERA`, `PARAM`, `GOSUB`, `ENDFUNC`)

Todo se resuelve con el patrón *listener* de ANTLR (puntos neurálgicos en
`enter*`/`exit*`), las pilas del generador y **backpatching** para los saltos.

> **Alcance de este documento.** Cubre los **puntos neurálgicos**, la **acción de
> cada uno**, los **nuevos operadores de cuádruplo** y la **distribución de
> direcciones virtuales** (puntos 1–4 y la lista de acciones de la rúbrica). El
> **diagrama visual** de los PN (SVG/HTML) es la pieza gráfica aparte; este MD es
> su contraparte textual/de referencia.

---

## 1. Nuevos operadores de cuádruplo

Un cuádruplo es `(op, opIzq, opDer, resultado)`. Etapa 4 agrega 6 operadores. La
**dirección de un cuádruplo es su índice en la fila** (no se guarda en el cuádruplo).

| Operador  | opIzq          | opDer | resultado        | Significado |
|-----------|----------------|-------|------------------|-------------|
| `GOTO`    | _              | _     | destino (índice) | Salto incondicional |
| `GOTOF`   | dir. condición | _     | destino (índice) | Salta si la condición es **falsa** |
| `ERA`     | _              | _     | nombre_func      | Reserva el registro de activación de la función |
| `PARAM`   | dir. argumento | _     | dir. parámetro   | Copia el argumento al parámetro destino |
| `GOSUB`   | nombre_func    | _     | cuad_inicio      | Salta al cuerpo de la función (guarda el retorno) |
| `ENDFUNC` | _              | _     | _                | Fin del cuerpo de la función (libera el frame) |

Helpers añadidos en `GeneradorCuadruplos` (`cuadruplos.py`):
`emitir_goto()`, `emitir_goto_falso(dir)`, `emitir_goto_a(destino)`,
`emitir_era(f)`, `emitir_param(dir_arg, dir_param)`, `emitir_gosub(f, cuad_inicio)`,
`emitir_endfunc()`, y se reactivó `backpatch(indice, target)`.

Estado nuevo:
- `GeneradorCuadruplos.pila_saltos` — índices de saltos **pendientes de backpatch**.
- `GeneradorCuadruplos.idx_goto_main` — índice del `GOTO` inicial hacia `main`.
- `SemanticAnalyzer.pila_llamadas` — contexto de la llamada en curso (para validar
  argumentos y soportar **llamadas anidadas** como `f(g(x))`).

---

## 2. El esqueleto: `GOTO`-main y `ENDFUNC`

Como las funciones se declaran **antes** de `inicio`, sus cuádruplos quedan
primero en la fila. Para que la ejecución arranque en `main`, **todo programa
emite un `GOTO` en el índice 0** que salta sobre los cuerpos de las funciones.

| PN | Punto neurálgico | Acción |
|----|------------------|--------|
| enterPrograma | inicio del programa | Emite `GOTO _ _ ?` en el índice 0; guarda su índice en `idx_goto_main` |
| enterFuncs    | inicio de una función | Graba `cuad_inicio = len(fila)` (destino del `GOSUB`) |
| exitFuncs     | fin de una función | Emite `ENDFUNC` |
| enterCuerpo   | inicio del cuerpo de `main` | **Backpatch** del `GOTO`-main → primer cuádruplo de `main` |

`enterCuerpo` distingue el cuerpo de `main` porque es el **único** cuyo padre es
`ProgramaContext` (los demás cuerpos cuelgan de condición/ciclo/función).

---

## 3. Control de flujo

### 3.1 `si` / `sino` — `condicion : SI (expresion) cuerpo sinoOpc PCOMA`

| PN | Acción |
|----|--------|
| `_manejar_condicion` (desde `exitExpresion`) | La condición ya está evaluada (tope de pila). Valida que sea **bool**, emite `GOTOF` y apila su índice en `pila_saltos` |
| `enterSinoOpc` (si hay `SINO`) | Saca el `GOTOF`, emite `GOTO` (para brincar el cuerpo del `sino`), lo apila, y **backpatch** del `GOTOF` → inicio del `sino` |
| `exitCondicion` | Saca el salto pendiente (el `GOTOF` si no hubo `sino`, o el `GOTO` si lo hubo) y lo **backpatch** → fin de la condición |

Como las condiciones se anidan, `pila_saltos` se maneja **LIFO**: cada construcción
saca exactamente lo que metió, así los saltos nunca se cruzan.

**Ejemplo** (`si (x > 0) { y = 1; } sino { y = -1; } ;`, con `x@1000`, `y@1001`):

```
2: (>,    1000, 13001, 11001)   # x > 0  -> temporal bool 11001
3: (GOTOF, 11001, _,    9)      # si falso, brinca al inicio del sino (9)
4: (=,    13002, _,    1001)    # y = 1   (cuerpo del si)
5: (GOTO,  _,    _,    10)      # brinca el sino -> despues del sino (10)
6: ... (otra cosa que sigue)
9: (=,    13003, _,    1001)    # y = -1  (cuerpo del sino)
```

### 3.2 `mientras` — `ciclo : MIENTRAS (expresion) HAZ cuerpo PCOMA`

| PN | Acción |
|----|--------|
| `enterCiclo` | Apila `retorno = len(fila)`: aquí empieza la evaluación de la condición (a dónde regresar) |
| `_manejar_condicion` | Emite `GOTOF` y apila su índice |
| `exitCiclo` | Saca el `GOTOF` y el `retorno`; emite `GOTO retorno` (re-evaluar) y **backpatch** del `GOTOF` → salida del ciclo |

**Ejemplo** (`mientras (i < n) haz { suma = suma + i; i = i + 1; } ;`):

```
4:  (<,     1000, 1001, 11000)  # i < n   <- retorno del ciclo
5:  (GOTOF, 11000, _,   11)     # si falso, sale del ciclo (11)
6:  (+,     1002, 1000, 9000)   # suma + i
7:  (=,     9000, _,   1002)    # suma = ...
8:  (+,     1000, 13002, 9001)  # i + 1
9:  (=,     9001, _,   1000)    # i = ...
10: (GOTO,  _,    _,    4)      # regresa a re-evaluar la condicion (4)
```

El `GOTO` de regreso apunta al **inicio de la condición**, no al cuerpo: si la
condición es `i < n + 1`, el `n + 1` también se recalcula en cada vuelta.

---

## 4. Funciones — `llamada : ID (argsOpc)`

| PN | Acción |
|----|--------|
| `enterLlamada` | Verifica que la función exista, emite `ERA func`, apila el contexto en `pila_llamadas` |
| `_manejar_argumento` (desde `exitExpresion`) | Cada argumento ya evaluado se empareja con el parámetro *k*; valida su tipo (cubo de asignación) y emite `PARAM` |
| `exitLlamada` | Valida el **número de argumentos**, emite `GOSUB func cuad_inicio`, saca el contexto. Si la llamada es **factor** (dentro de una expresión) deja el resultado en la pila |

El despacho "esta expresión es un argumento" se detecta en `exitExpresion` por el
tipo del padre (`ArgListaContext` / `ArgRestoContext`). La `pila_llamadas` permite
llamadas anidadas: el `PARAM` de cada argumento va a la función correcta.

**Ejemplo** (`sumar(3, 4);` con `sumar(a:entero, b:entero)`, `a@5000`, `b@5001`,
`cuad_inicio = 1`):

```
10: (ERA,   _,     _, sumar)    # reserva el frame de sumar
11: (PARAM, 13000, _, 5000)     # arg 3 -> parametro a (5000)
12: (PARAM, 13001, _, 5001)     # arg 4 -> parametro b (5001)
13: (GOSUB, sumar, _, 1)        # salta al cuerpo de sumar (cuad_inicio = 1)
```

### Funciones tipadas usadas en expresiones

Una función `entero`/`flotante` puede usarse como factor (`x = obtener() + 1`).
`exitLlamada` deja un **temporal** del tipo de retorno en la pila para que la
expresión continúe. El **retorno real está diferido** (ver §8): no toca la
gramática y no genera deuda técnica — la mecánica de llamada (`ERA/PARAM/GOSUB`)
es idéntica con o sin retorno.

---

## 5. Validaciones estrictas (Etapa 4)

| Validación | Dónde | Mensaje |
|------------|-------|---------|
| Condición debe ser `bool` | `_manejar_condicion` | `la condicion de 'si'/'mientras' debe ser de tipo bool` |
| Nº de argumentos = Nº de parámetros | `exitLlamada` | `funcion 'f' espera N argumento(s), recibio M` |
| Tipo de cada argumento compatible | `_manejar_argumento` | `argumento k de 'f': se esperaba T, se recibio U` |
| Función no declarada | `enterLlamada` | `funcion 'f' no declarada` |
| `nula` usada en expresión | `exitLlamada` | `no se puede usar funcion 'f' (retorno nula) en una expresion` |

El tipo de argumento usa la **regla de asignación del cubo semántico**: permite
ensanchamiento `entero → flotante`, rechaza estrechamiento `flotante → entero`.
Los errores ya propagados (operandos `"error"`) **no** se reportan de nuevo, para
evitar cascadas.

---

## 6. Distribución de direcciones virtuales

Sin cambios respecto a Etapa 3 (`AsignadorMemoria` y `TablaConstantes`); se
incluye como referencia porque la rúbrica lo pide.

| Segmento | entero | flotante | bool |
|----------|--------|----------|------|
| **Global**   | 1000–1999 | 2000–2999 | 3000–3999 |
| **Local**    | 5000–5999 | 6000–6999 | 7000–7999 |
| **Temporal** | 9000–9999 | 10000–10999 | 11000–11999 |

| Constantes | rango |
|------------|-------|
| entero   | 13000–13999 |
| flotante | 14000–14999 |
| letrero  | 15000–15999 |

- **Globales**: zona estática única, nunca se resetean.
- **Locales y temporales**: se **resetean al entrar a cada función**
  (`reset_scope_local`), por eso dos funciones distintas reusan `5000`, `6000`, etc.
  Es correcto: cada `ERA` abre un frame nuevo y el `PARAM`/`GOSUB` opera sobre él.
- Los huecos (4000, 8000, 12000) son reservas intencionales.

---

## 7. Archivos modificados

| Archivo | Cambios |
|---------|---------|
| `cuadruplos.py` | `pila_saltos`, `idx_goto_main`; helpers `emitir_goto/goto_falso/goto_a/era/param/gosub/endfunc`; se reactivó `backpatch` |
| `semantico.py`  | `import PatitoParser`, `pila_llamadas`; PNs nuevos (control de flujo y funciones); ampliación de `enterPrograma`, `enterFuncs`, `exitFuncs`, `exitExpresion`, `exitFactor`; nuevo `enterCuerpo` |
| `cubo.py`       | sin cambios (la regla de asignación se reusa para validar argumentos) |
| `patito.py`     | sin cambios (`--cuadruplos` ya imprime la fila genéricamente) |

`exitExpresion` quedó como **despachador de 3 vías** según el padre del nodo:
condición (`→ GOTOF`), argumento (`→ PARAM`), o normal (deja el operando en la pila).

---

## 8. Limitaciones documentadas (a propósito)

- **Retorno de funciones (`retorna`) diferido.** La gramática no tiene la sentencia
  `retorna`; no se tocó. Las funciones tipadas son invocables y dejan un temporal,
  pero su valor de retorno real se implementará después. Es **ortogonal** a la
  mecánica de llamada: agregarlo después no requiere rehacer `ERA/PARAM/GOSUB`.
- **Referencias hacia adelante.** Una función solo puede llamar a funciones
  declaradas **antes** que ella (o desde `main`). Llamar a una función declarada
  después se reporta como `funcion 'f' no declarada` (no es un crash).

---

## 9. Pruebas

83 pruebas en verde (`pytest`). Cobertura nueva de Etapa 4:

- **Contenido** (`tests/test_codegen.py`): destinos de `GOTOF`/`GOTO` afirmados
  **estructuralmente** (`== índice` del cuádruplo destino), `ERA/PARAM/GOSUB` en
  orden, `PARAM` a la dirección del parámetro, `GOSUB` a `cuad_inicio`, temporal de
  función tipada, llamada anidada, y las validaciones estrictas.
- **Exit codes** (`tests/cuadruplos_invalid/`): `07_args_de_mas`, `08_args_de_menos`,
  `09_arg_tipo_malo`, `10_condicion_no_bool`.
- Los programas válidos de control de flujo y funciones (`tests/valid/08`–`14`) ya
  generan cuádruplos y siguen saliendo con exit 0.
