# Proyecto Patito — Etapa 2

**TC3002B — Desarrollo de aplicaciones avanzadas de Ciencias Computacionales (Gpo 505)**
**Módulo:** Compiladores · Mini Proyecto INDIVIDUAL — Patito
**Estudiante:** Luis Manuel Gonzalez Martinez · A01722501
**Fecha:** Mayo 2026

---

## Mapeo a la rúbrica de Etapa 2

| Entregable de la rúbrica | Sección de este documento |
|---|---|
| Diseñar la Tabla de Consideraciones Semánticas (Cubo Semántico) | §1 |
| Implementar las estructuras del Directorio de Funciones y las Tablas de Variables | §2 |
| Establecer los puntos neurálgicos para crear y llenar el directorio + tablas, con validaciones | §3 |
| Documentar las estructuras elegidas, por qué, y las principales operaciones | Todo el documento |

Este documento extiende lo entregado en Etapa 1 (scanner + parser con ANTLR 4 C++ runtime). Para todo lo referente a la gramática y el análisis léxico/sintáctico, ver `docs/Patito_Etapa1.md`.

---

## 1. Cubo Semántico

El cubo es una **función de tres entradas** `(tipo_izq, operador, tipo_der) → tipo_resultado`. Cuando la combinación no es válida, el resultado es `ERROR`. En esta etapa el cubo solo se **diseña e implementa**; su **aplicación** sobre expresiones reales llegará en Etapa 3 al generar cuádruplos.

### 1.1 Tipos manejados

| Tipo | Origen | Uso |
|---|---|---|
| `entero` | Tipo del lenguaje | operandos enteros, tipo de retorno |
| `flotante` | Tipo del lenguaje | operandos de punto flotante, tipo de retorno |
| `nula` | Tipo del lenguaje | solo como tipo de retorno de función |
| `bool` | Interno | resultado de operadores relacionales |
| `error` | Interno | sentinela para combinaciones inválidas |

### 1.2 Tabla del cubo

**Operadores aritméticos** (`+`, `-`, `*`, `/`): el `flotante` "gana" cuando aparece en alguno de los operandos.

| izq \ der | entero | flotante |
|---|---|---|
| **entero** | entero | flotante |
| **flotante** | flotante | flotante |

**Operadores relacionales** (`>`, `<`, `!=`, `==`): cualquier combinación numérica produce `bool`.

| izq \ der | entero | flotante |
|---|---|---|
| **entero** | bool | bool |
| **flotante** | bool | bool |

**Asignación** (`=`): el lado izquierdo es el destino.

| izq \ der | entero | flotante |
|---|---|---|
| **entero** | entero | **ERROR** (pérdida de precisión) |
| **flotante** | flotante (ensanchamiento) | flotante |

Cualquier operación con `nula`, `bool` o `error` como operando produce `error`.

### 1.3 Implementación

El cubo vive en `src/semantic/SemanticCube.{h,cpp}`. La interfaz es una sola función estática:

```cpp
class SemanticCube {
public:
    static Tipo resultado(Tipo izq, Operador op, Tipo der);
};
```

Internamente uso un `switch` sobre el operador con casos agrupados por familia (aritmético, relacional, asignación) en vez de una tabla 3D literal. Es más legible y compila a algo equivalente, pero documenta la intención del diseño.

```cpp
Tipo SemanticCube::resultado(Tipo izq, Operador op, Tipo der) {
    if (!esNumerico(izq) || !esNumerico(der)) return Tipo::ERROR;
    const bool algunoFlot = (izq == Tipo::FLOTANTE) || (der == Tipo::FLOTANTE);
    switch (op) {
        case Operador::MAS: case Operador::MENOS:
        case Operador::POR: case Operador::ENTRE:
            return algunoFlot ? Tipo::FLOTANTE : Tipo::ENTERO;
        case Operador::MAYOR: case Operador::MENOR:
        case Operador::DISTINTO: case Operador::IGUAL2:
            return Tipo::BOOL;
        case Operador::ASIGNA:
            if (izq == Tipo::ENTERO && der == Tipo::FLOTANTE) return Tipo::ERROR;
            return izq;
    }
    return Tipo::ERROR;
}
```

---

## 2. Estructuras de datos

### 2.1 Resumen y justificación

| Estructura | Tipo C++ | Por qué |
|---|---|---|
| `VariableInfo` | `struct` simple | Solo guarda 3 campos (nombre, tipo, línea de declaración). No necesita encapsulación todavía. |
| `VariableTable` | wrapper sobre `std::unordered_map<string, VariableInfo>` | Las búsquedas por nombre son O(1) promedio, que es la operación dominante (cada uso de identificador hará lookup en Etapa 3). El orden de inserción no es relevante. |
| `ParametroInfo` | `struct` simple | Igual que `VariableInfo` pero sin línea (porque el orden importa, no la posición). |
| `FunctionInfo` | `struct` con `vector<ParametroInfo>` y `VariableTable` | Los parámetros van en `vector` porque el **orden** sí es crítico (las llamadas pasan argumentos posicionales). Las vars locales en `VariableTable` por la misma razón que las globales. |
| `FunctionDirectory` | wrapper sobre `std::unordered_map<string, FunctionInfo>` | Mismo razonamiento que `VariableTable`: lookup O(1) por nombre cuando se llama una función. |

### 2.2 Modelo de scopes

**Decisión clave:** el scope global del programa se representa como una **entrada más en el `FunctionDirectory`** (con el nombre del programa y tipo de retorno `nula`). Las variables globales viven en la `VariableTable` de esa entrada.

```
FunctionDirectory
├── "<nombrePrograma>"  ← scope global (tipoRetorno=nula, sin params)
│       └── VariableTable: vars globales
├── "funcion1"
│       ├── parámetros: [(x, entero), (y, flotante)]
│       └── VariableTable: parámetros + vars locales
├── "funcion2"
│       └── ...
└── ...
```

**Beneficios:** una sola estructura uniforme para todos los scopes, una sola operación (`obtener(nombre)`) para acceder a cualquiera, y al registrar una función con el mismo nombre del programa, el detector de duplicados lo atrapa "gratis".

### 2.3 Operaciones principales

**`VariableTable`:**

| Operación | Firma | Uso |
|---|---|---|
| Insertar | `bool agregar(nombre, tipo, linea)` | Devuelve `false` si ya existía (duplicado). |
| Existir | `bool existe(nombre)` | Para validaciones futuras (uso de variable). |
| Obtener | `const VariableInfo* obtener(nombre)` | Recupera tipo y línea de declaración. |
| Tamaño | `size_t tamano()` | Para el dump del directorio. |
| Iterar | `begin() / end()` | Recorrer la tabla en el dump. |

**`FunctionDirectory`:**

| Operación | Firma | Uso |
|---|---|---|
| Registrar | `FunctionInfo* agregar(nombre, tipoRetorno, linea)` | Devuelve puntero a la entrada nueva, o `nullptr` si el nombre ya estaba en uso. |
| Existir | `bool existe(nombre)` | Para validaciones en llamadas. |
| Obtener (mutable) | `FunctionInfo* obtener(nombre)` | Cuando hay que modificar (p. ej. agregar variables al entrar a la función). |
| Obtener (const) | `const FunctionInfo* obtener(nombre)` | Solo lectura. |
| Imprimir | `void imprimir(ostream&)` | Dump legible para la bandera `--dir`. |
| Iterar | `begin() / end()` | Recorrer todas las entradas. |

---

## 3. Puntos neurálgicos y validaciones

### 3.1 Arquitectura: listener de ANTLR

Las acciones semánticas se conectan al parse tree mediante el **patrón listener** de ANTLR4. Se hereda de `PatitoBaseListener` (clase generada) y se sobreescriben los métodos `enter<Regla>` / `exit<Regla>` correspondientes a los puntos donde se decide registrar algo. La clase es `patito::SemanticAnalyzer` en `src/semantic/SemanticAnalyzer.{h,cpp}`.

**Por qué listener:** el concepto clásico de "punto neurálgico" (acción semántica disparada al reconocer una regla) tiene una traducción 1:1 con un callback `enter<Regla>`. La gramática `.g4` se mantiene limpia (sin código C++ embebido) y el código semántico vive aislado en su propio archivo, lo cual también facilita extender hacia Etapa 3.

### 3.2 Puntos neurálgicos implementados

| # | Punto neurálgico (regla) | Acción semántica | Validaciones disparadas |
|---|---|---|---|
| 1 | `enterPrograma` | Extrae nombre del programa, lo registra como entrada GLOBAL del directorio (tipo retorno `nula`), establece `scopeActual` apuntando a esa entrada. | — (siempre la primera, no puede haber colisión) |
| 2 | `enterFuncs` | Extrae nombre y tipo de retorno, los registra en el directorio. Si la inserción tiene éxito, cambia `scopeActual` al nuevo. Recorre la lista de parámetros (`paramLista` + cadena de `paramResto`) y agrega cada uno como variable local. | • Función doblemente declarada. • Función con mismo nombre que el programa. • Parámetro duplicado dentro de la misma función. |
| 3 | `exitFuncs` | Cierra el scope local. Resetea `scopeActual` al scope global del programa y limpia la bandera de "función duplicada". | — |
| 4 | `enterDeclaracion` | Extrae el tipo (`tipo` hijo) y recorre toda la cadena `idLista` → `idResto` para obtener cada identificador. Agrega cada uno a la `VariableTable` del scope actual. | • Variable doblemente declarada en el mismo scope (cubre tanto el caso `vars: x:entero; x:flot;` como `vars: a,b,a:entero;`). |

**Manejo de subárbol contaminado:** cuando `enterFuncs` detecta una función duplicada, el walker de ANTLR sigue recorriendo el cuerpo de la función ofensora (no podemos saltarlo desde un listener). Para evitar que sus declaraciones internas se atribuyan al scope global, se activa una bandera `enFuncDuplicada` que `enterDeclaracion` consulta para ignorar el subárbol. `exitFuncs` la limpia al salir.

### 3.3 Resumen de validaciones

| Validación | Cuándo dispara | Mensaje |
|---|---|---|
| Variable doblemente declarada | dos declaraciones del mismo nombre en el mismo scope | `variable 'X' doblemente declarada en 'scope'` |
| Función doblemente declarada | dos `<Funcs>` con el mismo nombre | `funcion 'X' ya fue declarada antes` |
| Función con nombre del programa | un `<Funcs>` cuyo nombre coincide con el del programa | `el nombre de funcion 'X' coincide con el nombre del programa` |
| Parámetro duplicado | dos parámetros con el mismo nombre en una función | `parametro 'X' duplicado en funcion 'F'` |

Los errores se **acumulan**: el analizador no aborta al primero. Esto permite reportar todos los problemas en una sola corrida (igual que el comportamiento del análisis sintáctico en Etapa 1).

### 3.4 Wire en el driver

En `src/main.cpp`, tras `parser.programa()`, y solo si no hubo errores sintácticos, se ejecuta el listener:

```cpp
patito::SemanticAnalyzer analizador(archivo);
if (totalSintaxis == 0) {
    tree::ParseTreeWalker::DEFAULT.walk(&analizador, arbol);
    erroresSemantica = analizador.errores();
}
```

`ParseTreeWalker` es la utilidad de ANTLR que recorre el árbol llamando los callbacks correspondientes. El recorrido va en pre-order para `enter*` y post-order para `exit*`, lo cual permite que `enterFuncs` se dispare antes que cualquier `enterDeclaracion` de la misma función.

---

## 4. Estructura del proyecto (actualizada)

```
Patito/
├── grammar/
│   └── Patito.g4
├── src/
│   ├── main.cpp                     # driver (Etapa 1 + 2)
│   ├── generated/                   # codigo ANTLR (lexer/parser/listener)
│   └── semantic/                    # NUEVO en Etapa 2
│       ├── SemanticTypes.h          # enums Tipo y Operador
│       ├── SemanticCube.{h,cpp}     # cubo semantico
│       ├── SymbolTable.{h,cpp}      # VariableTable, FunctionDirectory
│       └── SemanticAnalyzer.{h,cpp} # listener con los 4 puntos neuralgicos
├── tests/
│   ├── valid/                       # 14 tests sintacticos validos
│   ├── invalid/                     # 10 tests sintacticos invalidos
│   ├── semantic_valid/              # NUEVO: 4 tests semanticos validos
│   ├── semantic_invalid/            # NUEVO: 7 tests semanticos invalidos
│   └── run_tests.sh                 # runner extendido (35 casos en total)
├── build/
├── docs/
│   ├── Patito_Etapa1.md
│   └── Patito_Etapa2.md             # este documento
└── CMakeLists.txt                   # actualizado para incluir src/semantic/*.cpp
```

---

## 5. Test Plan

### 5.1 Cobertura

El test plan crece de 24 (Etapa 1) a **36 casos**:

| Suite | Casos | Esperado |
|---|---|---|
| `tests/valid/` (sintaxis) | 14 | exit 0 |
| `tests/invalid/` (sintaxis) | 10 | exit 1 |
| `tests/semantic_valid/` (semántica) | 4 | exit 0 |
| `tests/semantic_invalid/` (semántica) | 8 | exit 1 |
| **Total** | **36** | |

### 5.2 Tests semánticos válidos (4)

| # | Archivo | Qué prueba |
|---|---|---|
| 1 | `01_basico.patito` | Programa con dos vars globales de tipos distintos. |
| 2 | `02_funciones.patito` | Dos funciones, una con parámetros y vars locales, otra sin nada. |
| 3 | `03_mismo_nombre_distinto_scope.patito` | Variable `x` declarada en el global, en parámetros de `primera`, y como local de `segunda`. Verifica que scopes independientes NO se cruzan. |
| 4 | `04_lista_vars.patito` | `a, b, c : entero;` y `p, q : flotante;` en el mismo bloque. Verifica que la lista con coma no produce falsos duplicados. |

### 5.3 Tests semánticos inválidos (8)

| # | Archivo | Error esperado |
|---|---|---|
| 1 | `01_var_duplicada_global.patito` | Dos vars globales con el mismo nombre, distinto tipo. |
| 2 | `02_var_duplicada_local.patito` | Dos vars locales con el mismo nombre dentro de una función. |
| 3 | `03_var_duplicada_en_lista.patito` | `a, b, a : entero;` (mismo identificador dos veces en una sola declaración). |
| 4 | `04_funcion_duplicada.patito` | Dos funciones con el mismo nombre y firma distinta. |
| 5 | `05_funcion_igual_programa.patito` | Una función nombrada igual que el programa. |
| 6 | `06_param_duplicado.patito` | `nula func(x : entero, y : flotante, x : entero)`. |
| 7 | `07_param_y_local_duplicados.patito` | Parámetro `x` y luego `vars x : flotante;` dentro de la misma función. |
| 8 | `08_func_dup_con_vars.patito` | Función duplicada que además tiene vars locales — verifica que las vars de la copia no contaminen el scope global (manejo del subárbol "sucio"). |

### 5.4 Resultados

```
========================================
 RESUMEN: 36 / 36 pasaron
========================================
```

---

## 6. Salidas de muestra

### 6.1 Directorio de funciones (bandera `--dir`)

Sobre `tests/semantic_valid/02_funciones.patito`:

```
=== DIRECTORIO DE FUNCIONES (3) ===
  funcion 'funciones'  retorno=nula  linea=1
    variables locales (1):
      n : entero  (linea 3)
  funcion 'calcular'  retorno=nula  linea=5
    parametros: x:entero y:flotante
    variables locales (3):
      x : entero  (linea 5)
      y : flotante  (linea 5)
      z : flotante  (linea 7)
  funcion 'otra'  retorno=nula  linea=13

OK   tests/semantic_valid/02_funciones.patito
```

Observa cómo `calcular` tiene 3 vars locales: las dos que vienen de parámetros (`x`, `y`) **más** la var declarada en el `vars` interno (`z`). El programa `funciones` aparece como su propio scope con la var global `n`. El orden de impresión está fijado por la línea de declaración (ordenado en `FunctionDirectory::imprimir`) para que la salida sea determinista entre corridas, independiente del orden interno del `unordered_map`.

### 6.2 Errores semánticos

**Variable doblemente declarada en global:**
```
[tests/semantic_invalid/01_var_duplicada_global.patito] linea 4:4  semantica: variable 'x' doblemente declarada en 'varDupGlobal'
FAIL tests/semantic_invalid/01_var_duplicada_global.patito  (1 error)
```

**Función duplicada:**
```
[tests/semantic_invalid/04_funcion_duplicada.patito] linea 8:5  semantica: funcion 'procesar' ya fue declarada antes
FAIL tests/semantic_invalid/04_funcion_duplicada.patito  (1 error)
```

**Parámetro duplicado:**
```
[tests/semantic_invalid/06_param_duplicado.patito] linea 3:36  semantica: parametro 'x' duplicado en funcion 'func'
FAIL tests/semantic_invalid/06_param_duplicado.patito  (1 error)
```

Cada mensaje sigue el formato `[archivo] linea L:C  semantica: <descripción>` para distinguirse claramente de los errores sintácticos de Etapa 1.

---

## 7. Cómo reproducir desde cero

```bash
# 1. Si vienes de Etapa 1, regenera el lexer/parser con listener habilitado
cd grammar
antlr -Dlanguage=Cpp -visitor -listener -o ../src/generated Patito.g4
cd ..

# 2. Reconfigura CMake (incluye los nuevos src/semantic/*.cpp via glob)
cmake -S . -B build

# 3. Compila
cmake --build build

# 4. Probar un caso concreto
./build/patito --dir tests/semantic_valid/02_funciones.patito

# 5. Correr todo el test plan
./tests/run_tests.sh
```

---