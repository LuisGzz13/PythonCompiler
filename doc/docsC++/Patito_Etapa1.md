# Proyecto Patito — Etapa 1

**TC3002B — Desarrollo de aplicaciones avanzadas de Ciencias Computacionales (Gpo 505)**
**Módulo:** Compiladores · Mini Proyecto INDIVIDUAL — Patito
**Estudiante:** Luis Manuel Gonzalez Martinez · A01722501
**Fecha:** Mayo 2026

---

## Mapeo a la rúbrica de Etapa 1

| Entregable de la rúbrica | Sección de este documento |
|---|---|
| Investigar herramientas de generación automática de compiladores | §1 |
| Seleccionar la herramienta más adecuada y justificar | §2 |
| Desarrollar Scanner y Parser usando reglas de Etapa 0 | §3, §4 |
| Diseñar y ejecutar un Test-Plan | §5, §6 |
| Documentar hallazgos, formato de alta de reglas y test cases | Todo el documento |

Este documento extiende el de Etapa 0 (donde se diseñaron las expresiones regulares, la lista de tokens y la gramática libre de contexto) y está pensado para seguir creciendo en las siguientes etapas (semántica, código intermedio, máquina virtual).

---

## 1. Investigación de herramientas de generación de compiladores

Revisé cinco generadores de scanner/parser de uso común en cursos de compiladores y en proyectos reales. Los puntos que comparé son: madurez, calidad de la documentación, soporte para C++ como lenguaje host, formalismo gramatical y curva de aprendizaje.

| Herramienta | Lenguaje host | Formalismo | Documentación | Notas |
|---|---|---|---|---|
| **ANTLR 4** | Java, **C++**, Python, JS, C#, Go, Swift, Dart, PHP | LL(*) (adaptive) | Excelente: libro oficial, `antlr.org`, ejemplos por target | Soporta recursión por la izquierda directa. IDE plugins (VS Code, IntelliJ). Runtime C++ disponible vía Homebrew. |
| **Flex + Bison** | C / C++ | LALR(1) | Buena (manuales clásicos GNU) | Estándar histórico (lex/yacc). Más manual: lexer y parser en archivos separados. Recursión por la izquierda obligatoria; conflictos shift/reduce frecuentes. |
| **PLY** (Python Lex-Yacc) | Python | LALR(1) | Buena pero menos amplia | Solo Python. Sintaxis de tokens basada en docstrings. |
| **JavaCC** | Java | LL(k) | Buena | Solo Java como host. |
| **Yacc/Bison puro** | C | LALR(1) | Clásica | Solo lo del parser; requiere Lex/Flex aparte para el lexer. |

**Hallazgos:**

1. **ANTLR4 es el único de la lista con un runtime C++ moderno y mantenido oficialmente** (`antlr4-cpp-runtime`, distribuido por Homebrew). Flex/Bison generan C/C++ pero su modelo es más bajo nivel.
2. La **documentación de ANTLR4** (libro *The Definitive ANTLR 4 Reference* de Terence Parr y el sitio `antlr.org`) cubre paso a paso desde gramáticas básicas hasta generación de código intermedio.
3. ANTLR4 acepta **recursión por la izquierda directa** (`exp: exp '+' termino | termino;`). Bison también, pero ANTLR la maneja sin la mecánica de tablas LR. Esto importa porque mi gramática de Etapa 0 ya usa recursión por la izquierda en `<Exp>` y `<Termino>` para la asociatividad izquierda de los operadores.
4. Flex/Bison habrían requerido escribir y mantener dos archivos (`.l` y `.y`) más una capa de pegado en C. ANTLR4 unifica todo en un solo `.g4`.

---

## 2. Selección: ANTLR 4 con runtime C++

Por los puntos anteriores, escogí **ANTLR 4 (versión 4.13.2)** con el **runtime de C++**. Razones concretas para este proyecto:

- **Un solo archivo de gramática (`Patito.g4`).** Lexer y parser en el mismo lugar, lo que simplifica mantener el mapeo 1:1 con la CFG y los tokens del documento de Etapa 0.
- **C++ como lenguaje host** abre la puerta a un driver eficiente y al uso de patrones tipo `Visitor`/`Listener` que serán útiles en las siguientes etapas (análisis semántico, generación de cuádruplos, máquina virtual).
- **Recursión por la izquierda directa**, sin tener que reescribir las producciones de expresiones aritméticas a la forma `Exp -> Termino Exp'`.
- **Disponibilidad inmediata en macOS arm64** (`brew install antlr antlr4-cpp-runtime`), sin compilar runtime desde fuente.

### Versiones y herramientas

| Componente | Versión |
|---|---|
| ANTLR4 (jar generador) | 4.13.2 |
| `antlr4-cpp-runtime` (Homebrew) | 4.13.2_1 |
| CMake | 4.3.2 |
| AppleClang | 16.0.0 |
| C++ standard | C++17 |
| OpenJDK (para correr el jar de ANTLR) | 21.0.3 |

---

## 3. Formato de alta de las reglas en ANTLR4 (`Patito.g4`)

Las reglas léxicas y gramaticales de Etapa 0 se dieron de alta en un único archivo `grammar/Patito.g4`. ANTLR4 distingue las dos clases de reglas por la primera letra del nombre:

- **Reglas de parser** (no-terminales) → empiezan con minúscula.
- **Reglas de lexer** (tokens) → empiezan con MAYÚSCULA.

### 3.1 Reglas léxicas (sección `LEXER RULES`)

Las expresiones regulares de Etapa 0 se traducen casi literalmente. Como ANTLR usa `'.'` para el carácter literal punto y `~[...]` para la negación de clase, los pequeños ajustes son:

| Elemento (Etapa 0) | Notación ANTLR4 |
|---|---|
| `[A-Za-z] ( [A-Za-z] \| [0-9] \| _ )*` | `ID : [a-zA-Z] [a-zA-Z0-9_]* ;` |
| `[0-9]+` | `CTE_ENT : [0-9]+ ;` |
| `[0-9]+ \. [0-9]+` | `CTE_FLOT : [0-9]+ '.' [0-9]+ ;` |
| `" [^"\n]* "` | `LETRERO : '"' ~["\r\n]* '"' ;` |
| Palabras reservadas (literales) | `PROGRAMA : 'programa' ;` etc. |

**Punto fino:** en el lexer ANTLR resuelve empates por orden de aparición. Las palabras reservadas se declaran **antes** de `ID` para que `programa`, `inicio`, `vars`, etc., no caigan como identificadores. Y `CTE_FLOT` se declara **antes** de `CTE_ENT` para que `3.14` no se descomponga en `CTE_ENT '.' CTE_ENT`.

```antlr
// extracto representativo
PROGRAMA : 'programa' ;
INICIO   : 'inicio' ;
// ...
ID       : [a-zA-Z] [a-zA-Z0-9_]* ;
CTE_FLOT : [0-9]+ '.' [0-9]+ ;
CTE_ENT  : [0-9]+ ;
LETRERO  : '"' ~["\r\n]* '"' ;
WS       : [ \t\r\n]+ -> skip ;
```

### 3.2 Reglas gramaticales (sección `PARSER RULES`)

Cada producción de la CFG de Etapa 0 se da de alta como una regla de parser. La traducción es 1:1, conservando los nombres de no-terminales (`<Programa>` → `programa`, `<DeclaracionList>` → `declaracionList`, etc.) y las alternativas separadas por `|`. Las producciones-épsilon se representan con una alternativa vacía:

```antlr
varsOpc
    : vars
    |       // alternativa vacia = epsilon
    ;

idResto
    : COMA ID idResto
    |       // epsilon
    ;

exp
    : exp MAS termino
    | exp MENOS termino
    | termino
    ;
```

ANTLR4 soporta directamente la **recursión por la izquierda directa** que aparece en `exp` y `termino`, así que las producciones aritméticas pasan tal cual al `.g4`. Esto preserva la asociatividad izquierda esperada (`10 - 3 - 2 = (10 - 3) - 2 = 5`).

El conflicto identificado en Etapa 0 entre `id` (factor simple) y `<Llamada>` (que también empieza con `id`) en `factor` se resuelve por la predicción adaptativa de ANTLR4 (LL(*)). En el `.g4` listo `llamada` antes de `signoOpc ID` para que el parser lo intente primero cuando ve `ID PIZQ ...`:

```antlr
factor
    : PIZQ expresion PDER
    | llamada
    | signoOpc ID
    | signoOpc cte
    ;
```

ANTLR generó el código del lexer y del parser sin warnings de ambigüedad ni de recursión no soportada.

### 3.3 Trazabilidad con la CFG de Etapa 0

Cada no-terminal de Etapa 0 corresponde uno a uno con una regla del `.g4`:

| Etapa 0 | `Patito.g4` |
|---|---|
| `<Programa>` | `programa` |
| `<VarsOpc>`, `<FuncsOpc>` | `varsOpc`, `funcsOpc` |
| `<Vars>`, `<DeclaracionList>`, `<Declaracion>` | `vars`, `declaracionList`, `declaracion` |
| `<IdLista>`, `<IdResto>` | `idLista`, `idResto` |
| `<Tipo>` | `tipo` |
| `<Funcs>`, `<TipoFunc>`, `<ParamsOpc>`, `<ParamLista>`, `<ParamResto>` | `funcs`, `tipoFunc`, `paramsOpc`, `paramLista`, `paramResto` |
| `<Llamada>`, `<ArgsOpc>`, `<ArgLista>`, `<ArgResto>` | `llamada`, `argsOpc`, `argLista`, `argResto` |
| `<Cuerpo>`, `<EstatutoList>`, `<Estatuto>` | `cuerpo`, `estatutoList`, `estatuto` |
| `<Asigna>`, `<Condicion>`, `<SinoOpc>`, `<Ciclo>` | `asigna`, `condicion`, `sinoOpc`, `ciclo` |
| `<Imprime>`, `<ImpLista>`, `<ImpResto>`, `<ImpElem>` | `imprime`, `impLista`, `impResto`, `impElem` |
| `<Expresion>`, `<RelOpc>`, `<OpRel>` | `expresion`, `relOpc`, `opRel` |
| `<Exp>`, `<Termino>`, `<Factor>`, `<SignoOpc>`, `<Cte>` | `exp`, `termino`, `factor`, `signoOpc`, `cte` |

---

## 4. Pipeline de compilación

### 4.1 Estructura del proyecto

```
Patito/
├── grammar/
│   └── Patito.g4              # gramatica unificada (lexer + parser)
├── src/
│   ├── main.cpp               # driver C++
│   └── generated/             # codigo generado por ANTLR (no editar)
│       ├── PatitoLexer.{h,cpp}
│       ├── PatitoParser.{h,cpp}
│       └── ...
├── tests/
│   ├── valid/                 # programas que deben parsear OK
│   ├── invalid/               # programas que deben fallar
│   └── run_tests.sh           # runner del test plan
├── build/                     # binario y artefactos de cmake
├── docs/
│   └── Patito_Etapa1.md       # este documento
└── CMakeLists.txt
```

### 4.2 Generación del scanner y parser

Desde la raíz del proyecto:

```bash
cd grammar
antlr -Dlanguage=Cpp -visitor -no-listener -o ../src/generated Patito.g4
```

Esto produce 12 archivos en `src/generated/` que CMake compila como parte del binario `patito`.

### 4.3 Build con CMake

`CMakeLists.txt` ubica el runtime ANTLR4 vía `find_path` / `find_library` (apunta a `/opt/homebrew/include/antlr4-runtime` y `/opt/homebrew/lib/libantlr4-runtime.dylib` en macOS arm64). Los pasos para compilar son:

```bash
cmake -S . -B build
cmake --build build
```

El binario queda en `build/patito`.

### 4.4 Driver (`src/main.cpp`)

El driver implementa lo siguiente:

1. Lee un archivo `.patito` desde disco.
2. Lo pasa al `PatitoLexer` para producir un `CommonTokenStream`.
3. Pasa el stream al `PatitoParser` empezando por la regla raíz `programa`.
4. Registra un `BaseErrorListener` propio (`ColectorErrores`) para recolectar errores léxicos y sintácticos con línea y columna.
5. Retorna `0` si no hubo errores, `1` si hubo al menos uno.

Banderas:

| Bandera | Efecto |
|---|---|
| (sin bandera) | Solo parsea y reporta `OK` o `FAIL`. |
| `--tokens` | Imprime la lista completa de tokens (línea, columna, tipo, lexema). |
| `--tree` | Imprime el árbol de parseo en formato LISP. |

---

## 5. Test Plan

### 5.1 Diseño y cobertura

El test plan tiene dos categorías:

- **Válidos** (`tests/valid/`): programas que cubren cada producción de la gramática. Deben parsear sin errores (exit code `0`).
- **Inválidos** (`tests/invalid/`): programas con un error sintáctico o léxico bien delimitado. Deben fallar (exit code distinto de `0`).

La cobertura busca que, en conjunto, los casos toquen al menos una vez cada construcción del lenguaje.

### 5.2 Casos válidos (14)

| # | Archivo | Qué prueba |
|---|---|---|
| 01 | `01_minimo.patito` | Programa más pequeño legal: `programa id; inicio { } fin`. Sin vars, sin funcs, cuerpo vacío. |
| 02 | `02_vars_simple.patito` | Bloque `vars` con una sola declaración. |
| 03 | `03_vars_lista.patito` | Lista de identificadores separados por coma (`a, b, c : entero;`). Verifica `idLista`/`idResto`. |
| 04 | `04_vars_mixto.patito` | Varias declaraciones consecutivas con `entero` y `flotante`. |
| 05 | `05_asigna.patito` | Asignaciones a `entero` y `flotante`, con literales y referencias. |
| 06 | `06_expr_aritm.patito` | Precedencia (`*` vs `+`), asociatividad izquierda, paréntesis, signo unario. |
| 07 | `07_expr_rel.patito` | Operadores relacionales `<`, `>`, `==`, `!=` dentro de condiciones. |
| 08 | `08_condicion.patito` | `si` con y sin `sino`, condicionales anidadas. |
| 09 | `09_ciclo.patito` | `mientras (...) haz { ... }` con cuerpo no trivial. |
| 10 | `10_imprime.patito` | `escribe` con expresiones, letreros y listas mixtas separadas por coma. |
| 11 | `11_funcion_nula.patito` | Función con tipo `nula`, sin parámetros, llamada como estatuto. |
| 12 | `12_funcion_params.patito` | Función con varios parámetros tipados, vars locales, llamadas con argumentos. |
| 13 | `13_llamada.patito` | Llamadas en los dos contextos del lenguaje: como estatuto (`uno();`) y como factor dentro de expresión (`a = obtener() + 1;`). Verifica el camino `factor → llamada` del parser. |
| 14 | `14_completo.patito` | Programa que combina vars globales, función, ciclo, condición, escribe y aritmética flotante. |

### 5.3 Casos inválidos (10)

| # | Archivo | Error esperado |
|---|---|---|
| 01 | `01_falta_pcoma.patito` | Falta `;` al final de una declaración de variables. |
| 02 | `02_keyword_como_id.patito` | Uso de `entero` como identificador (debe ganar la palabra reservada). |
| 03 | `03_paren_desbalanceado.patito` | Paréntesis sin cerrar dentro de una expresión. |
| 04 | `04_llave_desbalanceada.patito` | `{` del cuerpo principal sin `}` correspondiente. |
| 05 | `05_tipo_invalido.patito` | Tipo `cadena` inexistente en la gramática. |
| 06 | `06_letrero_sin_cierre.patito` | Comilla doble sin cerrar (error léxico). |
| 07 | `07_op_invalido.patito` | Operador `**` (no existe en la gramática). |
| 08 | `08_factor_vacio.patito` | Operando faltante después de `+`. |
| 09 | `09_funcion_mala.patito` | Función sin paréntesis de parámetros. |
| 10 | `10_si_sin_pcoma.patito` | Falta `;` al cierre de un `si`. |

### 5.4 Runner automatizado

`tests/run_tests.sh` recorre los dos directorios, ejecuta cada programa con `./build/patito` y compara el exit code contra el esperado (0 para `valid/`, 1 para `invalid/`). Imprime PASS/FAIL por archivo y un resumen final.

```bash
./tests/run_tests.sh
```

### 5.5 Resultados

Última corrida:

```
========================================
 VALIDOS  (deben parsear OK, exit=0)
========================================
  PASS  01_minimo.patito              (esperado=0, obtenido=0)
  PASS  02_vars_simple.patito         (esperado=0, obtenido=0)
  PASS  03_vars_lista.patito          (esperado=0, obtenido=0)
  PASS  04_vars_mixto.patito          (esperado=0, obtenido=0)
  PASS  05_asigna.patito              (esperado=0, obtenido=0)
  PASS  06_expr_aritm.patito          (esperado=0, obtenido=0)
  PASS  07_expr_rel.patito            (esperado=0, obtenido=0)
  PASS  08_condicion.patito           (esperado=0, obtenido=0)
  PASS  09_ciclo.patito               (esperado=0, obtenido=0)
  PASS  10_imprime.patito             (esperado=0, obtenido=0)
  PASS  11_funcion_nula.patito        (esperado=0, obtenido=0)
  PASS  12_funcion_params.patito      (esperado=0, obtenido=0)
  PASS  13_llamada.patito             (esperado=0, obtenido=0)
  PASS  14_completo.patito            (esperado=0, obtenido=0)

========================================
 INVALIDOS  (deben fallar, exit=1)
========================================
  PASS  01_falta_pcoma.patito         (esperado=1, obtenido=1)
  PASS  02_keyword_como_id.patito     (esperado=1, obtenido=1)
  PASS  03_paren_desbalanceado.patito (esperado=1, obtenido=1)
  PASS  04_llave_desbalanceada.patito (esperado=1, obtenido=1)
  PASS  05_tipo_invalido.patito       (esperado=1, obtenido=1)
  PASS  06_letrero_sin_cierre.patito  (esperado=1, obtenido=1)
  PASS  07_op_invalido.patito         (esperado=1, obtenido=1)
  PASS  08_factor_vacio.patito        (esperado=1, obtenido=1)
  PASS  09_funcion_mala.patito        (esperado=1, obtenido=1)
  PASS  10_si_sin_pcoma.patito        (esperado=1, obtenido=1)

========================================
 RESUMEN: 24 / 24 pasaron
========================================
```

---

## 6. Salidas de muestra

### 6.1 Lista de tokens (extracto de `05_asigna.patito`)

```
=== TOKENS ===
  linea 1:0   PROGRAMA  'programa'
  linea 1:9   ID        'asigna'
  linea 1:15  PCOMA     ';'
  linea 2:0   VARS      'vars'
  linea 3:4   ID        'a'
  linea 3:5   COMA      ','
  linea 3:7   ID        'b'
  linea 3:9   DPUNTOS   ':'
  linea 3:11  ENTERO    'entero'
  linea 3:17  PCOMA     ';'
  ...
  linea 10:8  CTE_FLOT  '3.14'
  linea 10:12 PCOMA     ';'
  linea 11:0  LLAVEDER  '}'
  linea 12:0  FIN       'fin'
```

### 6.2 Árbol de parseo (extracto)

```
(programa programa asigna ;
    (varsOpc
        (vars vars
            (declaracionList
                (declaracion
                    (idLista a (idResto , b idResto)) :
                    (tipo entero) ;)
                (declaracionList
                    (declaracion
                        (idLista p idResto) :
                        (tipo flotante) ;)))))
    funcsOpc inicio
    (cuerpo {
        (estatutoList
            (estatuto
                (asigna a =
                    (expresion ...))))) ...)
```

### 6.3 Mensajes de error de muestra

**`03_paren_desbalanceado.patito`** (paréntesis sin cerrar):
```
[tests/invalid/03_paren_desbalanceado.patito] linea 6:18  missing ')' at ';'
FAIL tests/invalid/03_paren_desbalanceado.patito  (1 error)
```

**`06_letrero_sin_cierre.patito`** (error léxico):
```
[tests/invalid/06_letrero_sin_cierre.patito] linea 4:12  token recognition error at: '"hola sin cerrar);\n'
[tests/invalid/06_letrero_sin_cierre.patito] linea 5:0   mismatched input '}' expecting {'+', '-', '(', ID, CTE_FLOT, CTE_ENT, LETRERO}
FAIL tests/invalid/06_letrero_sin_cierre.patito  (2 errores)
```

**`08_factor_vacio.patito`** (operando faltante):
```
[tests/invalid/08_factor_vacio.patito] linea 6:12  mismatched input ';' expecting {'+', '-', '(', ID, CTE_FLOT, CTE_ENT}
FAIL tests/invalid/08_factor_vacio.patito  (1 error)
```

Los mensajes incluyen línea, columna, qué se encontró y qué se esperaba, lo cual es suficiente para que un usuario localice el error sin tener que leer el `.g4`.

---

## 7. Cómo reproducir todo desde cero

```bash
# 1. Dependencias (macOS)
brew install antlr antlr4-cpp-runtime cmake

# 2. Generar lexer/parser desde la gramatica
cd grammar
antlr -Dlanguage=Cpp -visitor -no-listener -o ../src/generated Patito.g4
cd ..

# 3. Compilar
cmake -S . -B build
cmake --build build

# 4. Probar
./build/patito tests/valid/14_completo.patito
./build/patito --tokens tests/valid/05_asigna.patito
./build/patito --tree   tests/valid/05_asigna.patito

# 5. Correr el test plan completo
./tests/run_tests.sh
```

---

## 8. Próximas etapas (para extender este documento)

| Etapa | Contenido |
|---|---|
| **2** | Análisis semántico: tabla de variables, tabla de funciones, validación de tipos y uso. |
| **3** | Cubo semántico, generación de cuádruplos para asignaciones y expresiones. |
| **4** | Cuádruplos para condiciones, ciclos, llamadas a función y manejo de memoria virtual. |
| **5** | Máquina virtual que interpreta los cuádruplos. |
| **Final** | Integración: programa Patito → ejecución end-to-end. |

Cada etapa agregará una nueva sección en este documento con su propio mapeo a la rúbrica, decisiones de diseño y test plan.
