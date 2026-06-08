# Etapa 5 — Memoria de Ejecución y Máquina Virtual

**Patito (versión Python).** Esta etapa cierra el proyecto: implementa la
**Máquina Virtual** que ejecuta los cuádruplos producidos por las etapas 1–4,
diseña su **mapa de memoria de ejecución**, y demuestra el funcionamiento con
una suite de **test cases**.

> **Alcance de este documento.** Cubre las **estructuras de memoria** y sus
> **métodos de acceso**, los **12 opcodes** que la VM ejecuta, **cómo las
> direcciones virtuales indexan la memoria**, las **limitaciones documentadas**,
> y los **test cases**. El **diagrama visual** vive en
> `doc/Etapa5_diagramas.html`.

---

## 1. Pipeline completo

| Etapa | Produce | Quien lo consume |
|------|---------|------------------|
| 1 — Léxico/sintaxis | Árbol sintáctico (ANTLR) | Etapa 2 |
| 2 — Semántica | `func_dir`, scope, validaciones | Etapa 3 |
| 3 — Expresiones lineales | `gen.fila` (cuádruplos), `cte` (constantes) | Etapas 4–5 |
| 4 — Control de flujo + funciones | `gen.fila` con `GOTO/GOTOF/ERA/PARAM/GOSUB/ENDFUNC`, `FuncInfo.cuad_inicio` | Etapa 5 |
| **5 — Ejecución** | **stdout (salida del programa)** | **el usuario final** |

Etapa 4 cerró la generación; Etapa 5 cierra el compilador con un único cambio
mínimo (snapshot de recursos) y construye la VM encima.

---

## 2. Cerrar el compilador: snapshot de recursos

La VM necesita saber **cuántos slots de cada (segmento × tipo)** reservar al
abrir un frame nuevo. El compilador tiene esa información — está en
`AsignadorMemoria._contadores` — pero se **resetea** en cada `enterFuncs`. Hay
que capturarla justo antes de cerrar el scope.

**Cambios mínimos en `semantico.py`:**

| Punto neurálgico | Acción |
|---|---|
| `AsignadorMemoria.snapshot_recursos()` | Devuelve `{(seg,tipo) -> contador - base}` para locales y temps |
| `FuncInfo.recursos` | Atributo nuevo donde se guarda el snapshot |
| `exitFuncs` | Snapshot antes del switch de scope (la función que se cierra) |
| `exitPrograma` (PN nuevo) | Snapshot al cerrar `programa` (recursos de `main`) |
| `enterCuerpo` (extensión) | `reset_scope_local()` al entrar a `main` para que sus contadores no hereden basura de la última función |

Con esto, cada `FuncInfo` queda con un dict como:

```python
recursos = {
    ('local', 'entero'):    2,    # 'a' y 'b'
    ('local', 'flotante'):  0,
    ('local', 'bool'):      0,
    ('temp',  'entero'):    1,    # 'a + 1'
    ('temp',  'flotante'):  0,
    ('temp',  'bool'):      0,
}
```

`ERA` no cambia: sigue siendo `(ERA, _, _, nombre_func)`. La VM, al verlo,
**lee `func_dir[nombre].recursos`** y arma el frame.

---

## 3. Mapa de memoria de ejecución

La VM mantiene **cuatro estructuras** de memoria:

| Estructura | Tipo Python | Vida | Quién la escribe |
|---|---|---|---|
| **`memoria_global`** | `dict` | Toda la ejecución | `escribir()` para direcciones 1000–3999 |
| **`memoria_constantes`** | `dict` (inmutable) | Toda la ejecución | Cargada de `cte` al inicio, **no se modifica** |
| **`pila_frames`** | `list[Frame]` | Crece con `GOSUB`, decrece con `ENDFUNC`. **Main es `pila_frames[0]`** | `_nuevo_frame()` |
| **`pila_prep`** | `list[Frame]` | Crece con `ERA`, decrece con `GOSUB`. Pila para soportar `f(g(x))` | `_nuevo_frame()` |

Un **`Frame`** es:

```python
class Frame:
    nombre:     str        # nombre de la funcion (debug)
    locales:    dict       # {direccion -> valor} para 5000s/6000s/7000s
    temps:      dict       # {direccion -> valor} para 9000s/10000s/11000s
    ip_retorno: int        # IP al que volver cuando esta funcion termine
```

> **Por qué `pila_frames[0]` es `main`**: si tratáramos `main` como caso
> especial ("aquí no hay frame, sólo memoria global y temps de top-level"), el
> routing de `leer`/`escribir` se llenaría de `if`s. Empujando un frame de
> `main` al inicio, el routing queda **uniforme** desde la dirección 5000–11999:
> siempre van al `pila_frames[-1]`.

### Tabla completa del mapa de memoria de la VM

| Estructura | Rango virtual | Tipo | Persistencia | Mutable |
|---|---|---|---|---|
| `memoria_constantes` | 13000–13999 | entero (`int`) | toda la ejecución | ❌ |
| `memoria_constantes` | 14000–14999 | flotante (`float`) | toda la ejecución | ❌ |
| `memoria_constantes` | 15000–15999 | letrero (`str`) | toda la ejecución | ❌ |
| `memoria_global` | 1000–1999 | entero | toda la ejecución | ✅ |
| `memoria_global` | 2000–2999 | flotante | toda la ejecución | ✅ |
| `memoria_global` | 3000–3999 | bool | toda la ejecución | ✅ |
| `frame_actual.locales` | 5000–5999 | entero | un frame | ✅ |
| `frame_actual.locales` | 6000–6999 | flotante | un frame | ✅ |
| `frame_actual.locales` | 7000–7999 | bool | un frame | ✅ |
| `frame_actual.temps` | 9000–9999 | entero | un frame | ✅ |
| `frame_actual.temps` | 10000–10999 | flotante | un frame | ✅ |
| `frame_actual.temps` | 11000–11999 | bool | un frame | ✅ |

---

## 4. Las direcciones virtuales como índice

El compilador (Etapa 3) asignó direcciones virtuales por **(segmento × tipo)**
en tramos de 1000. La VM aprovecha esa estructura: cada **rango** te dice
**dónde vive el dato**.

### `_segmento_y_tipo(direccion)`

```python
def _segmento_y_tipo(direccion):
    """Decodifica una direccion virtual en (segmento, tipo). None si invalida.

    Recorre _RANGOS (derivados de las bases del compilador) y devuelve la
    primera (seg, tipo) cuyo rango la contiene.
    """
```

`_RANGOS` se **deriva** de `AsignadorMemoria._BASE` y `TablaConstantes._BASE`
del compilador — **única fuente de verdad** para no duplicar números:

```python
_RANGOS = []
for (seg, tipo), base in AsignadorMemoria._BASE.items():
    _RANGOS.append((base, base + 1000, seg, tipo))
for tipo, base in TablaConstantes._BASE.items():
    _RANGOS.append((base, base + 1000, "cte", tipo))
```

Si el compilador cambia un rango, la VM lo refleja automáticamente.

### `leer(direccion)`

```python
def leer(self, direccion):
    seg, tipo = _segmento_y_tipo(direccion)
    if seg == "cte":     return self.memoria_constantes[direccion]
    if seg == "global":  return self.memoria_global.get(direccion, _DEFAULTS[tipo])
    # local o temp: del FRAME ACTUAL
    f = self._frame_actual()
    store = f.locales if seg == "local" else f.temps
    return store.get(direccion, _DEFAULTS[tipo])
```

> **El default por tipo (`0`, `0.0`, `0` para bool)** evita crashes por *phantom
> temporals* (función tipada usada como factor; el retorno real está diferido,
> ver §8). Una variable nunca escrita devuelve el default — no `KeyError`.
> Bool usa `0` (no Python `False`) porque Patito representa booleanos como
> enteros 0/1 — coherente con C/C++ y con el resto del lenguaje, donde solo
> existen tipos `entero` y `flotante` declarables (ver §8).

### `escribir(direccion, valor)`

Mismo routing por segmento, escribe en `memoria_global` o en el `frame_actual`.
**Lanza error si intentas escribir a una constante.**

### `escribir_en_prep(direccion, valor)` — el método especial de `PARAM`

```python
def escribir_en_prep(self, direccion, valor):
    """Escribe en el TOP de pila_prep (callee aun no activo), NO en el frame actual."""
    self.pila_prep[-1].locales[direccion] = valor
```

`PARAM` no puede usar `escribir()` porque el "frame actual" en ese momento es
**el caller**. Si `caller.5000` y `callee.5000` chocan, el escribir genérico
sobreescribiría la variable del caller. Por eso PARAM tiene su propio método.

---

## 5. Las tres reglas que sostienen el modelo

| # | Regla | Consecuencia |
|---|-------|--------------|
| **1** | `main` es `pila_frames[0]` | Routing uniforme: no hay caso especial para top-level |
| **2** | `PARAM` lee del caller (frame actual), escribe en el callee (top de `pila_prep`) | Locales del caller no se corrompen, aunque compartan número de dirección con un parámetro |
| **3** | `pila_prep` es PILA, no slot | Soporta llamadas anidadas tipo `f(g(x))`. ERA empuja, GOSUB hace pop+activa |

Test que **cazaría** una violación de cada regla:
- Regla 1: `test_aritmetica_precedencia` (usa temps de main, sin función).
- Regla 2: `test_llamada_no_corrompe_memoria_del_caller`.
- Regla 3: `test_llamada_anidada_f_de_g`.

---

## 6. Los 12 opcodes y su semántica

| Opcode | opIzq | opDer | resultado | Acción en la VM |
|---|---|---|---|---|
| `+` `-` `*` | dir_a | dir_b | dir_res | `escribir(res, leer(a) op leer(b))` |
| `/` | dir_a | dir_b | dir_res | `int/int → //`; `float → /`. Error si `b == 0` |
| `<` `>` `==` `!=` | dir_a | dir_b | dir_res (bool, 0 o 1) | `escribir(res, int(leer(a) op leer(b)))`. Se envuelve en `int(...)` para que Patito almacene 0/1 en lugar de `True`/`False` |
| `=` | dir_origen | _ | dir_destino | `escribir(destino, leer(origen))` |
| `PRINT` | _ | _ | dir | `print(leer(dir))` |
| `GOTO` | _ | _ | destino | `IP = destino` |
| `GOTOF` | dir_cond | _ | destino | `if not leer(cond): IP = destino` |
| `ERA` | _ | _ | nombre_func | `pila_prep.append(_nuevo_frame(nombre_func))` |
| `PARAM` | dir_arg | _ | dir_param | `escribir_en_prep(dir_param, leer(dir_arg))` |
| `GOSUB` | nombre | _ | cuad_inicio | Pop prep, set `ip_retorno`, push como frame actual, `IP = cuad_inicio` |
| `ENDFUNC` | _ | _ | _ | Pop frame actual, `IP = frame.ip_retorno` |

### Convención del IP

Una sola regla:
- **Opcodes que saltan** (`GOTO/GOTOF/GOSUB/ENDFUNC`): setean `IP` y hacen `continue`.
- **Todos los demás**: caen al `IP += 1` del final del `while`.

Así ningún opcode necesita pensar "¿avanzo IP o no?".

---

## 7. Manejo de errores en runtime

Cuatro situaciones lanzan `RuntimeError` (capturado por `patito.py --ejecutar`
y reportado a stderr con exit code 1):

| Error | Cuándo | Mensaje |
|---|---|---|
| División por cero | `q.op == "/"` y `leer(opDer) == 0` | `VM: division por cero (IP=k)` |
| Stack overflow | `len(pila_frames) > 1000` después de un `GOSUB` | `VM: stack overflow (>1000 frames) al llamar 'f' (recursion infinita?)` |
| Dirección inválida | `_segmento_y_tipo(dir) is None` | `VM: direccion invalida al leer/escribir: D` |
| Opcode desconocido | Default del dispatch | `VM: opcode desconocido 'X' (IP=k)` |

Estos errores son **bugs detectables** en runtime. Errores de tipo, # de
argumentos, etc. son responsabilidad del compilador (etapas 2–4) y no llegan
a la VM.

---

## 8. Limitaciones documentadas

> **Nota histórica:** la limitación 8.1 (retorno de funciones diferido) **ya fue
> implementada** en una extensión posterior — ver §11 "Implementación de `retorna`"
> al final del documento. Se conserva la descripción histórica como referencia.

- **~~Retorno de funciones (`retorna`) diferido.~~ IMPLEMENTADO** Etapa 4 lo dejó
  diferido sin tocar la gramática. En su momento `entero f() {...}` se compilaba
  e invocaba, pero el "valor de retorno" era siempre `0` (default del *phantom
  temporal*). Se cerró agregando el token `RETORNA` al lexer, la regla
  `retorno : RETORNA expresion PCOMA` al parser, el PN `exitRetorno` que copia
  a un slot de retorno global, y la copia inversa en `exitLlamada` post-GOSUB
  para llevar el valor al phantom temporal del caller. Diseño "return slot por
  función": 0 opcodes nuevos en la VM. Detalle completo en §11.

- **Recursión.** La VM soporta **recursión directa** (`f` se llama a sí misma)
  con su pila de frames. La **recursión mutua** (`a` llama a `b` que llama a
  `a`) **no funciona** por la limitación de "referencias hacia adelante":
  cuando el compilador camina el cuerpo de `a`, `b` no está en `func_dir`
  todavía.

- **Variables no inicializadas.** Devuelven el *default* por tipo
  (`0`/`0.0`/`0`) en vez de lanzar error. Decisión deliberada para que el
  phantom temporal degrade limpiamente.

- **Sin tipo bool declarable.** La gramática solo permite tipos
  `entero` y `flotante` en `vars`. El tipo bool existe **solo internamente**
  como resultado de operadores relacionales (`<`, `>`, `==`, `!=`) y vive en
  los rangos 11000s (temporales). Cuando `escribe` imprime un bool, sale como
  `0` o `1` (coherente con la tradición académica y con C/C++ pre-C99).

---

## 9. Archivos agregados/modificados

| Archivo | Cambios |
|---|---|
| `vm.py` | **NUEVO**: `Frame`, `_DEFAULTS`, `_RANGOS`, `_segmento_y_tipo`, `MaquinaVirtual` |
| `semantico.py` | `snapshot_recursos`, `FuncInfo.recursos`, `exitPrograma`, snapshot en `exitFuncs`, `reset_scope_local` al entrar a `main` |
| `cuadruplos.py` | `TablaConstantes._BASE` (atributo de clase: única fuente para 13000/14000/15000); fix de `emitir_goto_falso` (ahora pone `opIzq=dir_cond`) |
| `patito.py` | Flag `--ejecutar` que importa y corre `MaquinaVirtual`. Flag `--dir` (utilidad de depuración) que imprime `func_dir` formateado vía `analizador.imprimir_directorio()` |
| `tests/test_vm.py` | **NUEVO**: 19 tests de ejecución con `capsys` + 2 tests de CLI |
| `tests/test_codegen.py` | Test que blinda `GOTOF.opIzq = dir_cond` + test que blinda `escribe(bool)` imprime 0/1 |
| `tests/valid/15_ejecutar_demo.patito` | **NUEVO**: programa demo para tests de CLI |
| `doc/Etapa5.md` | **NUEVO**: este documento |
| `doc/Etapa5_diagramas.html` | **NUEVO**: diagramas visuales |

---

## 10. Cómo correr y test cases

### Compilar + ejecutar un programa

```bash
python3 patito.py --ejecutar archivo.patito
```

### Ver los cuádruplos antes de ejecutar (útil para depurar)

```bash
python3 patito.py --cuadruplos --ejecutar archivo.patito
```

### Solo compilar (sin ejecutar)

```bash
python3 patito.py archivo.patito
echo $?    # 0 si compila, != 0 si hay errores
```

### Suite de tests

```bash
python3 -m pytest -q
```

**108 tests** total, distribuidos en tres archivos:
- `tests/test_compiler.py` (**59 tests**): cada `.patito` se ejecuta como
  subproceso y se verifica `exit code` + `stderr`. Cubre sintaxis (E1: 15 válidos + 10 inválidos),
  semántica (E2: 4 + 8), cuádruplos (E3: 12 + 6), y validaciones de Etapa 4
  (E4: 4 nuevos inválidos).
- `tests/test_codegen.py` (**28 tests**): asserts estructurales sobre la fila
  de cuádruplos. Cubre precedencia, dedup, control de flujo (saltos),
  llamadas (ERA/PARAM/GOSUB), y blindajes (`GOTOF.opIzq`, `escribe(bool)` = 0/1).
- `tests/test_vm.py` (**21 tests**): 19 con `capsys` (output de programas)
  + 2 con `subprocess` (flag `--ejecutar` end-to-end).

### Test cases destacados (Etapa 5)

| Test | Demuestra |
|---|---|
| `test_aritmetica_precedencia` | `2 + 3 * 4 = 14` — ejecución de aritmética con precedencia correcta |
| `test_mientras_suma_1_a_5` | `1+2+3+4+5 = 15` — ciclo completo con condición, cuerpo y backpatch |
| `test_si_anidado_dentro_de_mientras` | Saltos LIFO mezclados — sale `["baja","baja","alta","alta"]` |
| `test_llamada_no_corrompe_memoria_del_caller` | **Regla 2**: PARAM no pisa al caller (`h` mantiene su `a=7` tras llamar a `f`) |
| `test_llamada_anidada_f_de_g` | **Regla 3**: `pila_prep` es pila — `f(g(7))` ejecuta ambas en orden |
| `test_dos_funciones_distintas_no_se_pisan_locales` | Frame stack aísla locales (`a` y `b` ambas usan dir 5000 sin chocar) |
| `test_recursion_directa_con_caso_base` | Pila de frames crece y decrece correctamente |
| `test_recursion_infinita_se_detiene_con_stack_overflow` | Límite anti-runaway (1000 frames) detecta recursión sin caso base |
| `test_division_por_cero_*` | Error de runtime con mensaje claro y exit 1 |
| `test_cli_ejecutar_demo_corre_correctamente` | El flag `--ejecutar` produce el output esperado end-to-end |

---

## 11. Implementación de `retorna` (extensión post-Etapa 5)

Esta sección documenta el cierre de la limitación 8.1. El feature se implementó
en 6 secciones pequeñas, con tests entre cada una. El diseño elegido evita
cualquier opcode nuevo en la VM: reutiliza el cuádruplo `=` existente.

### 11.1 Diseño "return slot por función" (Design E)

Cada función tipada (entero/flotante) recibe **una dirección global única** al
ser registrada en `enterFuncs`. Esa dirección vive en un **nuevo segmento de
memoria virtual** llamado `retorno`:

| Segmento | Rango | Tipo |
|---|---|---|
| `("retorno", "entero")` | 17000–17999 | retorno entero |
| `("retorno", "flotante")` | 18000–18999 | retorno flotante |

(No hay `bool` retorno porque la gramática no permite funciones bool — `tipoFunc : NULA | tipo` y `tipo : ENTERO | FLOTANTE`.)

El segmento `retorno` se rutea a `memoria_global` en la VM. Los slots
**sobreviven** a cualquier frame pop — son globales en todo sentido.

### 11.2 Flujo end-to-end (ejemplo: `r = doble(5)`)

```
Compilador emite:                      VM ejecuta:
─────────────────────────────────────  ─────────────────────────────────────
(ERA, _, _, doble)                     push frame de doble a pila_prep
(PARAM, 13000, _, 5000)                escribir_en_prep: 5 → doble.x (5000)
(GOSUB, doble, _, cuad_inicio_doble)   pop prep, push como frame actual, IP=cuerpo
... cuerpo de doble ejecuta ...
  (*, 5000, 13000, 9000)                 9000 = 5 * 2 = 10 (en frame de doble)
  (=, 9000, _, 17000)  ← retorna         17000 = 10 (slot global de doble) ← NUEVO
  (ENDFUNC, _, _, _)   ← del retorna     pop frame, IP regresa a caller
(=, 17000, _, 9001)  ← post-GOSUB copy 9001 = leer(17000) = 10 (phantom en main) ← NUEVO
(=, 9001, _, 1000)   ← r = phantom     1000 = 10 (r en global)
```

Las **dos líneas nuevas** son las marcadas con NUEVO:
- El callee escribe su valor al slot global.
- El caller copia el slot al phantom temporal **inmediatamente después del GOSUB**.

### 11.3 PN nuevo: `exitRetorno`

Dispara cuando ANTLR sale de la regla `retorno : RETORNA expresion PCOMA`.
Comportamiento (semantico.py):

1. Si `scope_actual.tipo_retorno` es `"programa"` o `"nula"` → reporta error semántico, popea operando defensivamente, return.
2. Llama `gen.emitir_asignacion(dir_retorno, tipo_retorno)`. Eso reusa la lógica
   de `exitAsigna`: pop del RHS, valida cubo (`=`), emite `(=, dir_expr, _, dir_retorno)`.
3. Si el cubo falla (tipos incompatibles), reporta error.
4. Emite `(ENDFUNC, _, _, _)` para terminar la función inmediatamente.

### 11.4 Cambios en `exitLlamada`

Cuando una llamada se usa como factor (dentro de una expresión), se agregaron
2 líneas que emiten la copia post-GOSUB:

```python
dir_temp = self.mem.nuevo_temporal(f.tipo_retorno)
self.gen.emitir_directo(
    Cuadruplo(op="=", opIzq=f.dir_retorno, opDer=None, resultado=dir_temp))
self.gen.push_operando(dir_temp, f.tipo_retorno)
```

### 11.5 Cambios en la VM

Solamente 2 líneas modificadas en `vm.py`: ambos `leer()` y `escribir()`
ahora rutean el segmento `"retorno"` a `memoria_global`:

```python
if seg in ("global", "retorno"):
    return self.memoria_global.get(direccion, _DEFAULTS[tipo])
```

**No hay opcodes nuevos**. No cambia `GOSUB`, `ENDFUNC`, ni `PARAM`.

### 11.6 Por qué la recursión funciona

Aunque cada llamada recursiva **sobrescribe el mismo slot global**, la VM
**lee inmediatamente al regresar del GOSUB** hacia un phantom único por
call site. Trace conceptual de `factorial(5)`:

```
factorial(5) → factorial(4) → factorial(3) → factorial(2) → factorial(1) → factorial(0)
                                                                              retorna 1; slot=1
                                                       leer slot, phantom=1; retorna 1*1=1; slot=1
                                  leer slot, phantom=1; retorna 2*1=2; slot=2
            leer slot, phantom=2; retorna 3*2=6; slot=6
leer slot, phantom=6; retorna 4*6=24; slot=24
main: leer slot, phantom=120; r = phantom; escribe(r) → "120"
```

No hay race porque la VM es single-threaded.

### 11.7 Test cases nuevos

Cierra con **18 tests nuevos** (3 archivos `.patito` + 8 en `test_vm.py` + 7 en `test_codegen.py`):

| Test | Demuestra |
|---|---|
| `test_retorna_funcion_simple_entero` | `doble(7) = 14` — caso básico |
| `test_retorna_funcion_simple_flotante` | `division(15.0, 4.0) = 3.75` — slot flotante |
| `test_retorna_recursion_factorial` | `factorial(5) = 120` — recursión simple |
| `test_retorna_fibonacci` | `fib(10) = 55` — recursión doble (~177 llamadas) |
| `test_retorna_llamada_anidada` | `doble(triple(5)) = 30` — pila_prep + 2 slots distintos |
| `test_retorna_misma_funcion_dos_veces` | `doble(2) + doble(3) = 10` — phantoms únicos por call site |
| `test_retorna_early_exit_en_si` | retorna dentro de si termina la función |
| `test_retorna_entero_a_flotante_ensancha` | cubo permite ensanchamiento |
| `test_retorna_emite_asignacion_a_slot_y_endfunc` | cuádruplos generados correctos |
| `test_retorna_slots_separados_entero_y_flotante` | contadores 17000/18000 separados |
| `test_llamada_factor_emite_copy_post_gosub` | la copia inversa se emite |
| `test_retorna_en_nula_es_error_semantico` | validación: no retorna en nula |
| `test_retorna_en_main_es_error_semantico` | validación: no retorna en programa |
| `test_retorna_tipo_incompatible_es_error_semantico` | cubo previene estrechamiento |

### 11.8 Diff total

| Archivo | Cambios |
|---|---|
| `grammar/Patito.g4` | +1 token (`RETORNA`), +1 regla (`retorno`), +1 alternativa en `estatuto` |
| `generated/*` | regenerado por ANTLR |
| `semantico.py` | +12 líneas (memoria) + ~28 líneas (PN `exitRetorno`) + 3 líneas (`exitLlamada`) |
| `vm.py` | 2 líneas modificadas (routing del segmento `retorno`) |
| `tests/valid/` | +3 archivos (`20`, `21`, `22`) |
| `tests/semantic_invalid/` | +3 archivos (`13`, `14`, `15`) |
| `tests/test_vm.py` | +8 tests |
| `tests/test_codegen.py` | +7 tests |
| `doc/Etapa5.md` | esta sección §11 |
| **Tests totales** | **117 → 135 (sin regresiones)** |
