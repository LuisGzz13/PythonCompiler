# Bitácora de Apoyo de IA — Proyecto Patito

**Estudiante:** Luis Manuel Gonzalez Martinez · A01722501
**TC3002B Compiladores · Gpo 505**

Este documento registra el uso de herramientas de IA generativa a lo largo del desarrollo del proyecto Patito. Se mantiene una entrada por sesión significativa, indicando tarea, herramienta, prompts clave, salida obtenida y las ediciones manuales aplicadas. La intención es transparencia académica: muestra qué partes del trabajo recibieron asistencia y cuáles fueron revisadas/editadas por el estudiante antes de entregar.

---

## Herramienta principal usada

**Claude Code** (Anthropic) — modelo Sonnet 4.6 / Opus 4.7 según disponibilidad. Asistente con acceso a lectura/escritura de archivos en el workspace local. Se le suministró:
- Los diagramas del lenguaje Patito (PDF de la rúbrica) como contexto.
- Los entregables previos en cada nueva sesión para mantener continuidad.

Otras herramientas usadas:
- **Homebrew** (`brew`) para instalar ANTLR, CMake, pandoc.
- **VS Code** + **clangd** para edición y resolución de includes.
- **Pandoc** para convertir Markdown a DOCX.

---

## Etapa 0 — Diseño de regex, tokens y CFG

| Fecha | Tarea | Herramienta | Prompts clave | Salida obtenida | Edición manual |
|---|---|---|---|---|---|
| 2026-04-26 | Diseño inicial de expresiones regulares y CFG a partir de los diagramas | Claude Code | "Diseña las expresiones regulares para tokens del lenguaje Patito a partir de estos diagramas" + PDF de la rúbrica | Tablas iniciales de regex y lista de tokens; primer borrador de la CFG | Revisión y ajuste de la prosa para sonar natural (1ra persona, frases cortas); decisión de quitar la 4-tupla formal `G = (V_N, V_T, P, S)` por ser ajena al material del curso |
| 2026-04-27 | Verificación de listas con coma en declaraciones | Claude Code | "Valida contra los diagramas si `<VARS>`, `<FUNCS>`, `<LLAMADA>` e `<IMPRIME>` permiten múltiples elementos separados por coma" | Confirmación de que las 4 producciones de listas (`<IdLista>/<IdResto>`, etc.) están en el diseño original | Ninguna |
| 2026-04-27 | Generación del docx de entrega | Script Node.js (`build_doc.js`) con librería `docx-js` | "Genera un .docx desde el Markdown con formato simple blanco y negro" | `Patito_Etapa0.docx` | Ajustes manuales de bordes en tablas y estilos |

---

## Etapa 1 — Scanner y Parser con ANTLR4 + C++

| Fecha | Tarea | Herramienta | Prompts clave | Salida obtenida | Edición manual |
|---|---|---|---|---|---|
| 2026-05-05 | Instalación del toolchain (ANTLR, runtime C++, CMake) | Claude Code + `brew` | "Instala ANTLR4 con runtime C++ en macOS arm64" | Comandos `brew install antlr antlr4-cpp-runtime cmake`; verificación de versiones | Aprobación manual de cada `brew install` |
| 2026-05-05 | Implementación de `Patito.g4` | Claude Code | "Traduce 1:1 la CFG de Etapa 0 a una gramática ANTLR4 combinada (lexer + parser)" | Archivo `grammar/Patito.g4` con 235 líneas | Ninguna; compiló al primer intento sin warnings |
| 2026-05-05 | Driver C++ (`main.cpp`) + `CMakeLists.txt` | Claude Code | "Escribe un driver que lea un archivo .patito, corra lexer/parser, reporte errores con linea/columna" | `src/main.cpp` con `ColectorErrores` propio y banderas `--tokens`, `--tree` | Fix de un error de tipo (ANTLR 4.13 cambió `getSymbolicName` a `string_view`); requirió construir `std::string` explícitamente |
| 2026-05-05 | Diseño del Test Plan (14 válidos + 10 inválidos) | Claude Code | "Diseña casos de prueba que cubran cada producción de la gramática" + lista de qué verificar | 24 archivos `.patito` + `run_tests.sh` runner | Revisión de cada caso para confirmar que efectivamente prueba lo descrito; agregado del caso 13 corregido (función como factor en expresión) tras feedback del advisor |
| 2026-05-05 | Documentación de Etapa 1 | Claude Code | "Escribe un .md que cubra todos los puntos de la rúbrica de Etapa 1" | `docs/Patito_Etapa1.md` (18 KB) | Revisión de la prosa, ajustes de las descripciones de tests |
| 2026-05-05 | Walkthrough HTML línea por línea | Claude Code | "Genera un HTML scrollable que explique cada línea de código nuevo, con su contexto" | `docs/Patito_Etapa1_Walkthrough.html` (73 KB) | Ninguna; usado como referencia para estudiar |
| 2026-05-05 | Conversión a DOCX | `pandoc` (instalado con brew) | `pandoc docs/Patito_Etapa1.md -o docs/Patito_Etapa1.docx --from gfm --to docx` | `Patito_Etapa1.docx` | Ninguna |

---

## Etapa 2 — Análisis Semántico (Directorio + Tablas + Cubo)

| Fecha | Tarea | Herramienta | Prompts clave | Salida obtenida | Edición manual |
|---|---|---|---|---|---|
| 2026-05-17 | Diseño del cubo semántico | Claude Code | "Diseña el cubo semántico para Patito (tipos entero, flotante; operadores aritméticos, relacionales, asignación)" | Tablas de reglas + implementación en `SemanticCube.{h,cpp}` | Decisión informada: meter `BOOL` y `ERROR` en el mismo enum `Tipo` (artefactos internos, no tipos del lenguaje) — aclarado en doc |
| 2026-05-17 | Estructuras de scope (Directorio + Tablas) | Claude Code | "Implementa Directorio de Funciones y Tabla de Variables; modela el scope global como entrada especial" | `SymbolTable.{h,cpp}` con `VariableInfo`, `VariableTable`, `FunctionInfo`, `FunctionDirectory` | Discusión con la IA sobre por qué 5 structs (debate: las 2 pedidas vs las 3 records auxiliares) — se documentó la justificación |
| 2026-05-17 | Analizador semántico con listener | Claude Code | "Implementa SemanticAnalyzer heredando de PatitoBaseListener; sobreescribe los 4 puntos neurálgicos para llenar el directorio" | `SemanticAnalyzer.{h,cpp}` con `enterPrograma`, `enterFuncs`, `exitFuncs`, `enterDeclaracion` | Tras feedback del advisor: agregado de bandera `enFuncDuplicada` para no contaminar scope global con declaraciones de funciones duplicadas |
| 2026-05-17 | Tests semánticos | Claude Code | "Diseña 4 válidos + 8 inválidos cubriendo todas las validaciones de duplicados" | 12 archivos en `semantic_valid/` y `semantic_invalid/` + extensión del runner | Agregado del caso 08 (funcion duplicada con vars) tras detectar el bug de cascada |
| 2026-05-17 | Documentación de Etapa 2 | Claude Code | "Escribe Patito_Etapa2.md siguiendo el mismo formato de Etapa 1, con secciones de cubo, estructuras, puntos neurálgicos, tests" | `docs/Patito_Etapa2.md` (17 KB) | Ajustes para clarificar que `BOOL` y `ERROR` no son tipos del lenguaje |
| 2026-05-17 | Walkthrough HTML de Etapa 2 | Claude Code | "Genera HTML walkthrough siguiendo el patrón de Etapa 1, cubriendo solo código nuevo/modificado" | `docs/Patito_Etapa2_Walkthrough.html` (94 KB) | Ninguna |
| 2026-05-17 | Mejora de orden determinístico en `--dir` | Claude Code (feedback del advisor) | "El output del unordered_map no es determinista; agrega ordenamiento por línea de declaración en `imprimir`" | Modificación de `SymbolTable.cpp::imprimir` | Ninguna |

---

## Etapa 3 — Generación de Cuádruplos

| Fecha | Tarea | Herramienta | Prompts clave | Salida obtenida | Edición manual |
|---|---|---|---|---|---|
| 2026-06-XX | Análisis de gap entre Etapa 2 y requisitos de Etapa 3 | Claude Code | "Analiza si lo que tengo es suficiente para Etapa 3 (PILAS, FILA, cuádruplos para expresiones y estatutos lineales)" | Lista de gaps: falta memoria virtual, tabla de constantes, generador, varios overrides nuevos | Decisión sobre alcance: solo asigna + escribe (recomendado), no si/mientras |
| 2026-06-XX | Diseño del esquema de memoria virtual | Claude Code (en plan mode) | "Diseña rangos por (segmento × tipo) que sean fáciles de leer al debuggear" | Tabla con 12 rangos, huecos visuales en 4000s/8000s/12000s | Aprobación manual del plan antes de implementar |
| 2026-06-XX | `AsignadorMemoria`, `TablaConstantes` | Claude Code | "Implementa las clases con las API definidas en el plan" | `AsignadorMemoria.{h,cpp}` y `TablaConstantes.{h,cpp}` | Refactor: separar `direccionDe` para numéricos y `direccionDeLetrero` (en lugar de overload con tipo dummy) |
| 2026-06-XX | `GeneradorCuadruplos` con 3 pilas | Claude Code | "Implementa el generador siguiendo el algoritmo clásico de Aho con las 3 pilas pedidas por la rúbrica" | `GeneradorCuadruplos.{h,cpp}` con `pushOperando/Operador`, `popYEmitirBinario`, `emitirAsignacion/Print/Directo` | Agregado de `emitirDirecto` para reemplazar un `const_cast` feo |
| 2026-06-XX | Extensión del `SemanticAnalyzer` (9 nuevos puntos neurálgicos) | Claude Code | "Agrega los puntos neurálgicos para generación de cuádruplos: exitFactor, enter/exitExp, enter/exitTermino, enterRelOpc, exitExpresion, exitAsigna, exitImpElem" | `SemanticAnalyzer.{h,cpp}` extendido | Manejo del signo unario (caso `-id` genera `0-id`, caso `-cte` prepende `-` al lexema); manejo de llamada como factor (reserva temporal phantom para Etapa 4) |
| 2026-06-XX | Tests de cuádruplos (12 válidos + 3 inválidos) | Claude Code | "Diseña tests que verifiquen precedencia, asociatividad, paréntesis, signo unario, deduplicación de constantes, errores de tipos" | 15 archivos + extensión de `run_tests.sh` | Ninguna |
| 2026-06-XX | Documentación de Etapa 3 con diagramas ASCII | Claude Code | "Escribe Patito_Etapa3.md con diagramas tipo railroad en ASCII, marcando puntos neurálgicos con [PN-X]" | `docs/Patito_Etapa3.md` con 9 diagramas de reglas | Ninguna |
| 2026-06-XX | Walkthrough HTML de Etapa 3 | Claude Code | (pendiente) | (pendiente) | (pendiente) |
| 2026-06-XX | HTML de auditoría de puntos neurálgicos con SVG | Claude Code | (pendiente) | (pendiente) | (pendiente) |

---

## Patrones de uso

A lo largo del proyecto se siguieron estas prácticas para asegurar que el aporte propio fuera sustantivo:

1. **Plan mode antes de implementar**: en Etapa 3, todo se planeó (incluyendo rangos de memoria exactos) y se aprobó antes de generar código.
2. **Revisión de cada decisión de diseño**: cuando la IA propuso `BOOL`/`ERROR` en el enum `Tipo`, se cuestionó y se documentó la justificación (no se aceptó silenciosamente).
3. **Cuestionamiento de estructuras**: se debatió por qué 5 structs en lugar de 2 (la respuesta llevó a una documentación más clara).
4. **Validación con casos límite**: cada feature se probó con casos que el plan no contemplaba (variable doblemente declarada en lista, función con mismo nombre del programa, función duplicada con vars internas).
5. **Ediciones del estudiante** en momentos clave: rechazos de propuestas (p. ej. el `ExitPlanMode` inicial que omitía un walkthrough esperado), ajustes de prosa, decisiones de naming.

---

## Apéndice: Sesiones largas notables

- **2026-05-05 (Etapas 0+1):** ~6 horas. Se cubrió la documentación de Etapa 0, instalación del toolchain, implementación de gramática + driver + tests + walkthrough.
- **2026-05-17 (Etapa 2):** ~4 horas. Análisis semántico completo + tests + docs.
- **2026-06-XX (Etapa 3):** ~5 horas. Generador de cuádruplos + memoria virtual + tests + docs (2 HTMLs adicionales).

Cada sesión cerró con `tests/run_tests.sh` pasando 100% antes de declararse terminada.
