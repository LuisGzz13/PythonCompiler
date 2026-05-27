grammar Patito;

// =================================================================
// PARSER RULES (no-terminales)
// Traduccion 1:1 de la CFG de Etapa 0
// =================================================================

programa
    : PROGRAMA ID PCOMA varsOpc funcsOpc INICIO cuerpo FIN
    ;

varsOpc
    : vars
    |
    ;

funcsOpc
    : funcs funcsOpc
    |
    ;

vars
    : VARS declaracionList
    ;

declaracionList
    : declaracion declaracionList
    | declaracion
    ;

declaracion
    : idLista DPUNTOS tipo PCOMA
    ;

idLista
    : ID idResto
    ;

idResto
    : COMA ID idResto
    |
    ;

tipo
    : ENTERO
    | FLOTANTE
    ;

funcs
    : tipoFunc ID PIZQ paramsOpc PDER LLAVEIZQ varsOpc cuerpo LLAVEDER PCOMA
    ;

tipoFunc
    : NULA
    | tipo
    ;

paramsOpc
    : paramLista
    |
    ;

paramLista
    : ID DPUNTOS tipo paramResto
    ;

paramResto
    : COMA ID DPUNTOS tipo paramResto
    |
    ;

llamada
    : ID PIZQ argsOpc PDER
    ;

argsOpc
    : argLista
    |
    ;

argLista
    : expresion argResto
    ;

argResto
    : COMA expresion argResto
    |
    ;

cuerpo
    : LLAVEIZQ estatutoList LLAVEDER
    ;

estatutoList
    : estatuto estatutoList
    |
    ;

estatuto
    : asigna
    | condicion
    | ciclo
    | llamada PCOMA
    | imprime
    ;

asigna
    : ID IGUAL expresion PCOMA
    ;

condicion
    : SI PIZQ expresion PDER cuerpo sinoOpc PCOMA
    ;

sinoOpc
    : SINO cuerpo
    |
    ;

ciclo
    : MIENTRAS PIZQ expresion PDER HAZ cuerpo PCOMA
    ;

imprime
    : ESCRIBE PIZQ impLista PDER PCOMA
    ;

impLista
    : impElem impResto
    ;

impResto
    : COMA impElem impResto
    |
    ;

impElem
    : expresion
    | LETRERO
    ;

expresion
    : exp relOpc
    ;

relOpc
    : opRel exp
    |
    ;

opRel
    : MAYOR
    | MENOR
    | DISTINTO
    | IGUAL2
    ;

exp
    : exp MAS termino
    | exp MENOS termino
    | termino
    ;

termino
    : termino POR factor
    | termino ENTRE factor
    | factor
    ;

factor
    : PIZQ expresion PDER
    | llamada
    | signoOpc ID
    | signoOpc cte
    ;

signoOpc
    : MAS
    | MENOS
    |
    ;

cte
    : CTE_ENT
    | CTE_FLOT
    ;

// =================================================================
// LEXER RULES (tokens)
// Las palabras reservadas van ANTES de ID para que ganen el match
// =================================================================

// Palabras reservadas
PROGRAMA : 'programa' ;
INICIO   : 'inicio' ;
FIN      : 'fin' ;
VARS     : 'vars' ;
ENTERO   : 'entero' ;
FLOTANTE : 'flotante' ;
ESCRIBE  : 'escribe' ;
SI       : 'si' ;
SINO     : 'sino' ;
MIENTRAS : 'mientras' ;
HAZ      : 'haz' ;
NULA     : 'nula' ;

// Operadores
MAS      : '+' ;
MENOS    : '-' ;
POR      : '*' ;
ENTRE    : '/' ;
MAYOR    : '>' ;
MENOR    : '<' ;
DISTINTO : '!=' ;
IGUAL2   : '==' ;
IGUAL    : '=' ;

// Puntuacion
PCOMA    : ';' ;
COMA     : ',' ;
DPUNTOS  : ':' ;
PIZQ     : '(' ;
PDER     : ')' ;
LLAVEIZQ : '{' ;
LLAVEDER : '}' ;

// Identificadores y literales
// CTE_FLOT debe ir antes que CTE_ENT para que 3.14 no se parsee como CTE_ENT '.' CTE_ENT
ID       : [a-zA-Z] [a-zA-Z0-9_]* ;
CTE_FLOT : [0-9]+ '.' [0-9]+ ;
CTE_ENT  : [0-9]+ ;
LETRERO  : '"' ~["\r\n]* '"' ;

// Espacios en blanco: se descartan
WS       : [ \t\r\n]+ -> skip ;
