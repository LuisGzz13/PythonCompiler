import sys
sys.path.insert(0, 'generated')
from antlr4 import InputStream, CommonTokenStream, ParseTreeWalker
from PatitoLexer import PatitoLexer
from PatitoParser import PatitoParser
from semantico import SemanticAnalyzer
from vm import MaquinaVirtual


def correr(src, etiqueta):
    print(f"--- {etiqueta} ---")
    lex = PatitoLexer(InputStream(src))
    p = PatitoParser(CommonTokenStream(lex))
    a = SemanticAnalyzer()
    ParseTreeWalker().walk(a, p.programa())
    if a.errores > 0:
        print(f"!! errores de compilacion: {a.errores}")
        return
    vm = MaquinaVirtual(a)
    vm.ejecutar()


# 1. Hello world
correr("""
programa hola;
inicio { escribe("Hola Mundo!"); } fin
""", "hola mundo")

# 2. Aritmetica + impresion
correr("""
programa aritm;
vars x : entero;
inicio {
    x = 2 + 3 * 4;
    escribe("resultado = ", x);
} fin
""", "aritmetica (precedencia)")

# 3. Ciclo que imprime 1..5
correr("""
programa cuenta;
vars i : entero;
inicio {
    i = 1;
    mientras (i < 6) haz {
        escribe(i);
        i = i + 1;
    } ;
} fin
""", "mientras 1..5")

# 4. Llamada a funcion con parametro
correr("""
programa llamar;
vars n : entero;
nula doble(x : entero) {
    vars d : entero;
    { d = x + x; escribe("doble = ", d); }
} ;
inicio {
    n = 7;
    doble(n);
    escribe("listo");
} fin
""", "llamada con parametro")