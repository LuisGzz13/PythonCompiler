# Proyecto Patito — Etapa 3

**TC3002B — Desarrollo de aplicaciones avanzadas de Ciencias Computacionales (Gpo 505)**
**Módulo:** Compiladores · Mini Proyecto INDIVIDUAL — Patito
**Estudiante:** Luis Manuel Gonzalez Martinez · A01722501
**Fecha:** Junio 2026

---

## Mapeo a la rúbrica de Etapa 3

| Entregable de la rúbrica | Sección de este documento |
|---|---|
| Implementar las PILAS (operadores, operandos, tipos) | §2.3 |
| Implementar la FILA de cuádruplos | §2.4 |
| Algoritmos de traducción a cuádruplos para expresiones aritméticas y relacionales | §3 |
| Algoritmos para estatutos lineales (asignación y `escribe`) | §3.5 y §3.6 |
| Desplegar el contenido final de la Fila para programas de prueba | §5 |
| Documentar las estructuras de Pilas y Filas | §2 |
| Diagramas con puntos neurálgicos señalados + descripción de cada acción | §4 |
| Documentar apoyo de IA | `docs/Apoyo_IA.md` (archivo separado) |

Este documento extiende lo entregado en Etapas 1 y 2. Para la gramática, ver `Patito_Etapa1.md`. Para el cubo semántico, directorio de funciones y tablas de variables, ver `Patito_Etapa2.md`.

**Alcance:** esta etapa cubre **expresiones aritméticas, relacionales, asignación y escribe** — los estatutos lineales del lenguaje. Control de flujo (`si`, `mientras`) y llamadas a función con su mecánica completa (`ERA`/`PARAM`/`GOSUB`/`ENDFUNC`) entran en Etapa 4 porque requieren parchado de saltos (backpatching).

---

## 1. Esquema de Memoria Virtual

Cada operando que aparece en un cuádruplo (variable, parámetro, temporal, constante) se identifica por una **dirección entera** dentro de uno de **12 rangos** predefinidos. Estos rangos se eligieron por (segmento × tipo) y dejan **huecos visuales** entre segmentos para que el primer dígito de la dirección identifique a simple vista el tipo y segmento.

| Segmento | Tipo | Rango | Cuándo se asigna | Reset |
|---|---|---|---|---|
| **GLOBAL** | entero | `1000 – 1999` | vars del programa principal | nunca |
| **GLOBAL** | flotante | `2000 – 2999` | vars del programa principal | nunca |
| **GLOBAL** | bool | `3000 – 3999` | (reservado para Etapa 4+) | nunca |
| *(hueco)* | | `4000 – 4999` | — | — |
| **LOCAL** | entero | `5000 – 5999` | vars locales y parámetros enteros | al entrar a cada función |
| **LOCAL** | flotante | `6000 – 6999` | locales y parámetros flotantes | al entrar a cada función |
| **LOCAL** | bool | `7000 – 7999` | (reservado) | al entrar a cada función |
| *(hueco)* | | `8000 – 8999` | — | — |
| **TEMPORAL** | entero | `9000 – 9999` | resultados intermedios enteros | al entrar a cada función |
| **TEMPORAL** | flotante | `10000 – 10999` | resultados intermedios flotantes | al entrar a cada función |
| **TEMPORAL** | bool | `11000 – 11999` | resultados de operaciones relacionales | al entrar a cada función |
| *(hueco)* | | `12000 – 12999` | — | — |
| **CONSTANTE** | entero | `13000 – 13999` | literales `5`, `42`, ... (deduplicación) | nunca |
| **CONSTANTE** | flotante | `14000 – 14999` | literales `3.14`, `0.0`, ... | nunca |
| **CONSTANTE** | letrero | `15000 – 15999` | literales `"hola"`, ... | nunca |

**Lectura rápida** (primer dígito):
- `1xxx` → global entero · `5xxx` → local entero · `9xxx` → temporal entero · `13xxx` → constante entera
- `2xxx` → global flot · `6xxx` → local flot · `10xxx` → temp flot · `14xxx` → const flot
- `3xxx` → global bool · `7xxx` → local bool · `11xxx` → temp bool · `15xxx` → const letrero

**Por qué locales y temporales se resetean por función:** cada llamada a función en la VM (Etapa 5+) abrirá un activation record propio. Las direcciones locales son **relativas al frame**, así que dos funciones pueden ambas usar `5000`, sin pisarse. Globales y constantes viven en zonas estáticas únicas, por lo que **no** se resetean.

**Deduplicación de constantes:** si el literal `5` aparece varias veces, ambas referencias usan la misma dirección. Esto reduce el uso del rango y simplifica la VM.

---

## 2. Estructuras nuevas

### 2.1 `Cuadruplo` (`src/semantic/Cuadruplo.h`)

La unidad mínima de código intermedio:

```cpp
struct Cuadruplo {
    Operador op;    // qué operación
    int opIzq;      // dirección del operando izq, o -1 si N/A
    int opDer;      // dirección del operando der, o -1 si N/A
    int resultado;  // dirección del destino
};
```

| Forma | `op` | `opIzq` | `opDer` | `resultado` |
|---|---|---|---|---|
| Binario aritmético / relacional | `+ - * / > < != ==` | dirección | dirección | dirección del temporal |
| Asignación | `=` | dirección origen | `-1` | dirección destino |
| Imprimir | `PRINT` | `-1` | `-1` | dirección a imprimir |

### 2.2 `AsignadorMemoria` (`src/semantic/AsignadorMemoria.{h,cpp}`)

Maneja los **9 contadores** de los rangos no-constantes (globales, locales, temporales). API:

```cpp
class AsignadorMemoria {
public:
    void resetScopeLocal();                // llamada en enterFuncs
    int nuevaGlobal(Tipo tipo);
    int nuevaLocal(Tipo tipo);             // también usado para parámetros
    int nuevoTemporal(Tipo tipo);
};
```

Si el rango se desborda, devuelve `-1` (el analizador reporta error).

### 2.3 PILAS — `GeneradorCuadruplos` (`src/semantic/GeneradorCuadruplos.{h,cpp}`)

Encapsula las **3 pilas** que pide la rúbrica:

| Pila | Tipo C++ | Contenido | Operación principal |
|---|---|---|---|
| `pilaOperandos` | `std::stack<int>` | direcciones de operandos pendientes | push (al ver id/cte), pop (al generar cuádruplo) |
| `pilaTipos` | `std::stack<Tipo>` | tipos de los operandos en `pilaOperandos` | paralela a pilaOperandos |
| `pilaOperadores` | `std::stack<Operador>` | operadores pendientes (precedencia) | push al ver operador, pop al generar |

**Nota honesta sobre el algoritmo:** en un parser flat (sin árbol) la `pilaOperadores` sirve para resolver precedencia comparando operadores que llegan consecutivamente. Aquí, gracias al listener de ANTLR4 sobre un árbol cuya estructura (`exp → exp + termino`, `termino → termino * factor`) **ya codifica** la precedencia, la pila no necesita comparar — basta con empujar el operador en `enter<Regla>` y popearlo en `exit<Regla>`. Mantenemos la pila porque (a) la rúbrica la pide explícitamente y (b) hace el algoritmo idéntico al clásico de Aho/Ullman cuando se documenta.

### 2.4 FILA — `_fila` en `GeneradorCuadruplos`

```cpp
std::vector<Cuadruplo> _fila;
```

**Por qué `vector` y no `queue`:** Etapa 4 va a necesitar parchear cuádruplos ya emitidos (cuando se sabe el destino de un `GOTO` después de generar el cuerpo del `si`). Un `std::queue` no permite acceso por índice, mientras que `std::vector` sí.

### 2.5 `TablaConstantes` (`src/semantic/TablaConstantes.{h,cpp}`)

Tres maps internos (uno por tipo de constante), cada uno mapea `lexema → dirección`:

```cpp
class TablaConstantes {
public:
    int direccionDe(const std::string& lex, Tipo tipo);  // entero o flotante
    int direccionDeLetrero(const std::string& lex);      // letrero (cadena)
    void imprimir(std::ostream& os) const;
};
```

Si el lexema ya estaba en el map, devuelve la misma dirección (deduplicación). Si no, asigna del rango correspondiente.

### 2.6 Modificaciones a estructuras de Etapa 2

| Estructura | Cambio | Por qué |
|---|---|---|
| `VariableInfo` | agregado campo `int direccion` | la dirección virtual asignada por `AsignadorMemoria` |
| `ParametroInfo` | agregado campo `int direccion` | igual |
| `Operador` enum | agregado valor `PRINT` | para los cuádruplos de `escribe` |
| `VariableTable::agregar` | agregado parámetro `int direccion = -1` | el analizador asigna y registra atómicamente |

---

## 3. Algoritmo de generación

### 3.1 Idea general

Recorremos el árbol de parseo en pre-orden (enters) y post-orden (exits) con un `ParseTreeWalker` de ANTLR4. En los **puntos neurálgicos** correspondientes, manipulamos las pilas y la fila.

**Invariante clave:** al terminar de procesar cualquier `expresion` del árbol, su dirección de resultado queda como **top** de `pilaOperandos` (y su tipo como top de `pilaTipos`). La regla que la consume (la asignación, la próxima operación binaria, el `escribe`...) hace pop.

### 3.2 Operandos atómicos

Cuando exit de un `factor` que es `id` o `cte`:
- **Variable (`id`)**: buscar en la tabla del scope actual (y luego en global), tomar su dirección y tipo, push.
- **Constante (`cte`)**: registrar en `TablaConstantes` (si ya existía, recupera dirección; si no, asigna nueva), push dirección y tipo.

Cuando exit de un `factor` que es `( expresion )`: nada (la expresión interna ya empujó su resultado).

Cuando exit de un `factor` que es `llamada`: reservar un temporal del tipo de retorno y empujarlo como "fantasma" (Etapa 4 emitirá los cuádruplos reales de llamada).

### 3.3 Signo unario

Para `-id`: emitir un cuádruplo `(-, 0, dir_id, t)` donde `0` es la constante 0 y `t` es un temporal del tipo del id. Push `t`.

Para `-cte`: tratar `-5` como una constante distinta de `5` (lexema `"-5"` registrado en `TablaConstantes`). Push su dirección.

Para `+`: nada (push el operando tal cual).

### 3.4 Expresiones binarias (aritméticas y relacionales)

Aplica al patrón **`exp → exp <op> termino`**, **`termino → termino <op> factor`**, y **`expresion → exp <opRel> exp`**.

**Al entrar** a la regla con operador:
1. Push el operador a `pilaOperadores`.

**Al salir** de la regla con operador (después de haber recorrido los hijos, que ya empujaron sus operandos):
1. Pop el operador.
2. Pop el operando derecho y su tipo.
3. Pop el operando izquierdo y su tipo.
4. Consultar el **Cubo Semántico**: `tRes = SemanticCube::resultado(tIzq, op, tDer)`.
5. Si `tRes == ERROR`: reportar y abortar este cuádruplo (no se emite).
6. Si OK: asignar un temporal del tipo `tRes` y emitir `(op, dIzq, dDer, tNuevo)`. Push `tNuevo` y `tRes` para que la operación enclosing los use.

### 3.5 Asignación

Al salir de `asigna : id = expresion ;`:
1. Resolver la dirección y tipo del `id` destino (buscarlo en el scope).
2. Pop el operando del RHS (top de `pilaOperandos`).
3. Consultar cubo con `(tipoDestino, =, tipoRHS)`. Si ERROR, reportar.
4. Emitir `(=, dirRHS, -1, dirDestino)`.

### 3.6 Escribe

Para cada elemento de la lista (`escribe(elem1, elem2, ...)`):
- Si es un **letrero** (literal de cadena): registrarlo en `TablaConstantes` con `direccionDeLetrero`, emitir `(PRINT, -1, -1, dirLetrero)`.
- Si es una **expresion**: la expresión ya dejó su resultado en el top de `pilaOperandos`. Pop, emitir `(PRINT, -1, -1, dirResultado)`.

---

## 4. Puntos neurálgicos — diagramas

A continuación cada regla relevante con marcas `[PN]` en los puntos exactos donde el listener dispara acciones semánticas.

### 4.1 `<PROGRAMA>` (Etapa 2, modificado en Etapa 3)

```
   programa --- id --- ; --- VARS_OPC --- FUNCS_OPC --- inicio --- CUERPO --- fin
                ▲
                │
       [PN2-1] enterPrograma
         · registra el programa como scope GLOBAL en directorio
         · scopeActual = programa
         · Etapa 3: AsignadorMemoria arranca con globales en 1000/2000
```

### 4.2 `<VARS>` (declaraciones)

```
   vars --- ┌────────────────────────────────────────┐ ───
            │                                        │
            ▼                                        │
            id ─┬─ , ─ id ─┐ ─── : ─ TIPO ─── ; ─────┤
                │           │                        │
                └───────────┘                        │
            └────────────────────────────────────────┘
                                                     ▲
                                                     │
                                            [PN2-4] enterDeclaracion
                                              · extrae lista de ids + tipo
                                              · valida duplicados en scope actual
                                              · Etapa 3: asigna direccion
                                                (global o local segun scope)
                                                via AsignadorMemoria
```

### 4.3 `<FUNCS>`

```
   TIPO_FUNC --- id --- ( --- PARAMS --- ) --- { --- VARS_OPC --- CUERPO --- } --- ;
                  ▲                                                              ▲
                  │                                                              │
        [PN2-2] enterFuncs                                       [PN2-3] exitFuncs
          · registra funcion en directorio                        · scopeActual = global
          · valida duplicados                                     · enFuncDuplicada = false
          · scopeActual = nueva funcion
          · Etapa 3: mem.resetScopeLocal()
          · procesa parametros con direccion local
```

### 4.4 `<ASIGNA>`

```
   id --- = --- EXPRESION --- ;
                                ▲
                                │
                          [PN3-E] exitAsigna
                            · resuelve direccion+tipo del id destino
                            · pop operando RHS de pilaOperandos
                            · valida cubo: (tDestino, =, tRHS)
                            · emite cuadruplo (=, dirRHS, -1, dirDestino)
```

### 4.5 `<EXPRESION>` (con opcional relacional)

```
   EXP --- REL_OPC --- EXP
            │                              ▲
            │                              │
   [PN3-D1] enterRelOpc            [PN3-D2] exitExpresion (si relOpc no es epsilon)
     (si opRel no es epsilon)        · pop operador + 2 operandos
       · push operador relacional    · valida cubo (resultado = BOOL)
         (>, <, ==, !=)              · emite cuadruplo, push temp BOOL
```

### 4.6 `<EXP>` (suma y resta)

```
   ┌────────────────────────────────┐
   │                                │
   ▼                                │
   TERMINO ──┬── '+' ──┬── TERMINO ─┘
             │         │
             └── '-' ──┘
                  ▲
                  │
          [PN3-B1] enterExp (si MAS o MENOS)
            · push operador a pilaOperadores

                       ────► exit del nodo
                                │
                           [PN3-B2] exitExp (si MAS o MENOS)
                             · pop operador
                             · pop 2 operandos+tipos
                             · valida cubo (resultado entero o flotante)
                             · asigna nuevo temporal
                             · emite (op, izq, der, temp)
                             · push temp+tipo
```

### 4.7 `<TERMINO>` (multiplicación y división)

Estructura idéntica a `<EXP>` pero con `*` y `/` en lugar de `+` y `-`:

```
   FACTOR ──┬── '*' ──┬── FACTOR
            │         │
            └── '/' ──┘
                 ▲
                 │
         [PN3-C1] enterTermino: push operador
         [PN3-C2] exitTermino:  pop, validar cubo, emitir
```

### 4.8 `<FACTOR>`

```
   ┌── '(' --- EXPRESION --- ')' ──────────┐
   │                                       │
   ├── LLAMADA ────────────────────────────┤
   │                                       │
   ├── SIGNO_OPC ─┬─ id ──────────────────┤
   │              │                       │
   │              └─ CTE ──────────────────┤
   └───────────────────────────────────────┘
                                            ▲
                                            │
                                  [PN3-A] exitFactor
                                    · caso 1 (parens): nada
                                    · caso 2 (llamada): reserva temp del retorno
                                    · caso 3 (id):
                                         - busca var
                                         - si '-' delante: emite (-, 0, var, t)
                                         - push direccion+tipo
                                    · caso 4 (cte):
                                         - registra en TablaConstantes
                                           (si '-' delante, lexema = "-X")
                                         - push direccion+tipo
```

### 4.9 `<IMPRIME>`

```
   escribe --- ( --- IMP_LISTA --- ) --- ;
                          │
                          ▼
                  ELEM ──┬── , ──┬── ELEM
                         │       │
                         └───────┘

   donde ELEM = EXPRESION | LETRERO
                                ▲
                                │
                       [PN3-F] exitImpElem
                         · si LETRERO: registra en TablaConstantes (rango 15000s),
                                        emite (PRINT, -, -, dir_letrero)
                         · si EXPRESION: pop top de pilaOperandos,
                                          emite (PRINT, -, -, dir_resultado)
```

---

## 5. Test Plan

### 5.1 Cobertura

El test plan crece de 36 (Etapas 1+2) a **51 casos**:

| Suite | Casos | Esperado |
|---|---|---|
| `tests/valid/` (sintaxis) | 14 | exit 0 |
| `tests/invalid/` (sintaxis) | 10 | exit 1 |
| `tests/semantic_valid/` (semántica) | 4 | exit 0 |
| `tests/semantic_invalid/` (semántica) | 8 | exit 1 |
| `tests/cuadruplos_valid/` (cuádruplos) | 12 | exit 0 |
| `tests/cuadruplos_invalid/` (cuádruplos) | 3 | exit 1 |
| **Total** | **51** | |

### 5.2 Casos válidos de cuádruplos (12)

| # | Archivo | Qué prueba |
|---|---|---|
| 1 | `01_asigna_literal.patito` | `x = 5;` — un solo cuádruplo `=` con constante 5 |
| 2 | `02_asigna_var.patito` | `x = a;` — `=` entre dos vars sin operación intermedia |
| 3 | `03_suma_simple.patito` | `x = a + b;` — un `+` + un `=` |
| 4 | `04_precedencia.patito` | `x = a + b * c;` — `*` se evalúa antes que `+` |
| 5 | `05_parens.patito` | `x = (a + b) * c;` — paréntesis cambian la precedencia |
| 6 | `06_asociatividad_izq.patito` | `x = 10 - 3 - 2;` — debe dar `(10-3)-2 = 5` |
| 7 | `07_signo_unario.patito` | `x = -a + 1;` — `0 - a` antes de sumar |
| 8 | `08_flotantes.patito` | `p = 3.14 * 2.0;` y `r = p + 0.5;` — temporales flotantes |
| 9 | `09_mixto.patito` | `p = a + b;` (a entero, p flotante) — promoción + ensanchamiento en `=` |
| 10 | `10_relacional.patito` | `escribe(a < b); escribe(a == b);` — expresión relacional dentro de escribe |
| 11 | `11_escribe_letrero.patito` | `escribe("hola"); escribe("mundo"); escribe("hola");` — verifica deduplicación |
| 12 | `12_escribe_lista.patito` | `escribe("x vale ", x, " y a+b es ", a + b);` — múltiples elementos mixtos |

### 5.3 Casos inválidos de cuádruplos (3)

| # | Archivo | Error esperado |
|---|---|---|
| 1 | `01_var_no_declarada.patito` | `x = y;` donde `y` no se declaró |
| 2 | `02_asigna_flot_a_ent.patito` | `x = 3.14;` donde `x` es entero (cubo dice ERROR para `entero = flotante`) |
| 3 | `03_func_no_declarada.patito` | `x = noExiste() + 1;` — llamada a función no registrada |

### 5.4 Resultados

```
========================================
 RESUMEN: 51 / 51 pasaron
========================================
```

---

## 6. Salidas de muestra

### 6.1 Precedencia: `x = a + b * c`

```
=== TABLA DE CONSTANTES (0) ===

=== FILA DE CUADRUPLOS (3) ===
  0: (*, 1001, 1002, 9000)
  1: (+, 1000, 9000, 9001)
  2: (=, 9001, _, 1003)
```

Lectura: `b` (1001) `*` `c` (1002) → `t0` (9000). Luego `a` (1000) `+` `t0` → `t1` (9001). Finalmente `x` (1003) recibe `t1`.

### 6.2 Signo unario: `x = -a + 1`

```
=== TABLA DE CONSTANTES (2) ===
  enteros   (13000-13999):
    13000 <- 0
    13001 <- 1

=== FILA DE CUADRUPLOS (3) ===
  0: (-, 13000, 1000, 9000)
  1: (+, 9000, 13001, 9001)
  2: (=, 9001, _, 1001)
```

El `-a` se traduce a `0 - a` (constante 0 en `13000`). Luego `+ 1` (constante 1 en `13001`). Asignación final.

### 6.3 Escribe con lista: `escribe("x vale ", x, " y a+b es ", a + b)`

```
=== TABLA DE CONSTANTES (3) ===
  enteros   (13000-13999):
    13000 <- 5
  letreros  (15000-15999):
    15000 <- "x vale "
    15001 <- " y a+b es "

=== FILA DE CUADRUPLOS (6) ===
  0: (=, 13000, _, 1000)
  1: (PRINT, _, _, 15000)
  2: (PRINT, _, _, 1000)
  3: (PRINT, _, _, 15001)
  4: (+, 1001, 1002, 9000)
  5: (PRINT, _, _, 9000)
```

Un `PRINT` por elemento. Las expresiones (`a + b`) se evalúan a un temporal antes de imprimir.

### 6.4 Error: variable no declarada

```
[tests/cuadruplos_invalid/01_var_no_declarada.patito] linea 6:8  semantica: variable 'y' usada sin declarar en 'varNoDecl'
[tests/cuadruplos_invalid/01_var_no_declarada.patito] linea 6:4  semantica: tipos incompatibles en asignacion a 'x' (entero)
FAIL tests/cuadruplos_invalid/01_var_no_declarada.patito  (2 errores)
```

El primer error es el principal (uso sin declarar). El segundo es **derivado**: como el RHS quedó con `Tipo::ERROR` en la pila, el cubo rechaza la asignación. Esto se podría suprimir en una versión más pulida, pero por ahora la doble notificación es útil para depurar.

---

## 7. Estructura del proyecto (actualizada)

```
Patito/
├── grammar/Patito.g4
├── src/
│   ├── main.cpp                            (modificado: bandera --cuadruplos)
│   ├── generated/                          (sin cambios)
│   └── semantic/
│       ├── SemanticTypes.h                 (modificado: Operador::PRINT)
│       ├── SemanticCube.{h,cpp}            (modificado: caso PRINT)
│       ├── SymbolTable.{h,cpp}             (modificado: campo direccion + dump)
│       ├── SemanticAnalyzer.{h,cpp}        (modificado: 9 nuevos overrides)
│       ├── Cuadruplo.h                     (NUEVO)
│       ├── AsignadorMemoria.{h,cpp}        (NUEVO)
│       ├── TablaConstantes.{h,cpp}         (NUEVO)
│       └── GeneradorCuadruplos.{h,cpp}     (NUEVO)
├── tests/
│   ├── valid/                              (Etapa 1)
│   ├── invalid/                            (Etapa 1)
│   ├── semantic_valid/                     (Etapa 2)
│   ├── semantic_invalid/                   (Etapa 2)
│   ├── cuadruplos_valid/                   (NUEVO, 12 casos)
│   ├── cuadruplos_invalid/                 (NUEVO, 3 casos)
│   └── run_tests.sh                        (modificado: 2 suites más)
├── docs/
│   ├── Patito_Etapa1.md / .docx
│   ├── Patito_Etapa1_Walkthrough.html
│   ├── Patito_Etapa2.md
│   ├── Patito_Etapa2_Walkthrough.html
│   ├── Patito_Etapa3.md                    (este documento)
│   ├── Patito_Etapa3_Walkthrough.html      (walkthrough del código nuevo)
│   ├── Patito_Etapa3_PuntosNeuralgicos.html (auditoría visual con SVG)
│   └── Apoyo_IA.md                         (NUEVO: bitácora de uso de IA)
└── CMakeLists.txt                          (sin cambios; el GLOB recoge los nuevos .cpp)
```

---

## 8. Cómo reproducir

```bash
# 1. Asegurar dependencias (ya instaladas en Etapas previas)
brew install antlr antlr4-cpp-runtime cmake

# 2. Generar lexer/parser (si no se hizo en Etapa 2)
cd grammar
antlr -Dlanguage=Cpp -visitor -listener -o ../src/generated Patito.g4
cd ..

# 3. Reconfigurar CMake (importante: el GLOB recoge nuevos .cpp solo al configurar)
cmake -S . -B build

# 4. Compilar
cmake --build build

# 5. Smoke test
./build/patito --cuadruplos tests/cuadruplos_valid/04_precedencia.patito

# 6. Suite completa
./tests/run_tests.sh        # debe mostrar 51 / 51 pasaron
```

---

## 9. Próximas etapas

| Etapa | Contenido |
|---|---|
| **4** | Control de flujo (`si`, `mientras`) con backpatching. Llamadas a función completas con `ERA`, `PARAM`, `GOSUB`, `ENDFUNC`, `RETURN`. Validación de aridad y tipos de argumentos. |
| **5** | Máquina virtual que interpreta los cuádruplos, con manejo de memoria virtual real (vectores indexados por los rangos de direcciones de esta etapa). |
| **Final** | Integración end-to-end y pruebas de programas Patito completos. |

Las direcciones diseñadas en esta etapa (rangos por segmento × tipo) son la base directa para la VM: bastará con allocar arreglos para globales y para el activation record de cada función.
