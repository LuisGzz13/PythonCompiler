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

> **El default por tipo (`0`, `0.0`, `False`)** evita crashes por *phantom
> temporals* (función tipada usada como factor; el retorno real está diferido,
> ver §8). Una variable nunca escrita devuelve el default — no `KeyError`.

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
| `<` `>` `==` `!=` | dir_a | dir_b | dir_res (bool) | Mismo patrón |
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

- **Retorno de funciones (`retorna`) diferido.** Etapa 4 lo dejó así sin tocar
  la gramática. `entero f() {...}` se compila y se invoca, pero el "valor de
  retorno" es siempre `0` (default del *phantom temporal*). Para retornos
  reales se necesitaría agregar el token `retorna` al lexer, una regla
  `retorno : RETORNA expresion PCOMA` al parser, un PN `exitRetorno` que
  copie a un slot de retorno, y unas 5 líneas más en `exitLlamada` y la VM
  para leerlo.

- **Recursión.** La VM soporta **recursión directa** (`f` se llama a sí misma)
  con su pila de frames. La **recursión mutua** (`a` llama a `b` que llama a
  `a`) **no funciona** por la limitación de "referencias hacia adelante":
  cuando el compilador camina el cuerpo de `a`, `b` no está en `func_dir`
  todavía.

- **Variables no inicializadas.** Devuelven el *default* por tipo
  (`0`/`0.0`/`False`) en vez de lanzar error. Decisión deliberada para que el
  phantom temporal degrade limpiamente.

---

## 9. Archivos agregados/modificados

| Archivo | Cambios |
|---|---|
| `vm.py` | **NUEVO**: `Frame`, `_DEFAULTS`, `_RANGOS`, `_segmento_y_tipo`, `MaquinaVirtual` |
| `semantico.py` | `snapshot_recursos`, `FuncInfo.recursos`, `exitPrograma`, snapshot en `exitFuncs`, `reset_scope_local` al entrar a `main` |
| `cuadruplos.py` | `TablaConstantes._BASE` (atributo de clase: única fuente para 13000/14000/15000); fix de `emitir_goto_falso` (ahora pone `opIzq=dir_cond`) |
| `patito.py` | Flag `--ejecutar` que importa y corre `MaquinaVirtual` |
| `tests/test_vm.py` | **NUEVO**: 20 tests de ejecución con `capsys` + 2 tests de CLI |
| `tests/test_codegen.py` | Test que blinda `GOTOF.opIzq = dir_cond` |
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

**107 tests** total:
- 24 de sintaxis (E1)
- 12 de semántica (E2)
- 18 de generación de cuádruplos contenido + 6 inválidos (E3)
- 10 de control de flujo y funciones contenido + 4 inválidos (E4)
- 20 de ejecución de la VM + 2 de CLI (E5)
- Más programas integradores en `tests/valid/`

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
