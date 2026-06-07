import sys
from cubo import tipo_resultado

sys.path.insert(0, 'generated')

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener
from PatitoLexer import PatitoLexer
from PatitoParser import PatitoParser
from semantico import SemanticAnalyzer
from vm import MaquinaVirtual

# ============================================================
# PARTE 1 - MANEJO DE ERRORES
# ============================================================

class ContadorErrores(ErrorListener):
    """
    ErrorListener custom: imprime el error a stderr Y mantiene un contador.
    Sin esto, ANTLR imprime errores pero el parser sigue, asi que no sabriamos
    al final si hubo o no errores para decidir el exit code.
    """
    def __init__(self): # Constructor: corre automaticamente al hacer ContadorErrores()
        super().__init__() # Inicializa el padre (ErrorListener) antes de agregar lo nuestro
        self.errores = 0 # Contador de errores acumulados; arranca en 0
    
    def syntaxError(self,recognizer, offendingSymbol, line, col, msg, e): # e es el error
        # Imprimir error de sintaxis y contar los errores. (Las 6 params son de la libreria antlr4)
        # por ahora solo ocpamos linea, columna y mensaje.
        print(f"linea {line}:{col}  {msg}", file=sys.stderr)
        self.errores += 1
        
    #errores semanticos estan en clase SemanticAnalyzer por simplicidad.


# ============================================================
# PARTE 2 - DRIVER
# ============================================================

def main ():
    # revisa que se haya pasado un archivo como argumento por eso son 2 (python patito.py(1) archivo.patito(2))
    if len(sys.argv) < 2:
        print("Uso: python patito.py [--cuadruplos] [--dir] [--ejecutar] archivo.patito", file=sys.stderr)
        sys.exit(2)
    
    args = sys.argv[1:]
    imprimir_cuadruplos = "--cuadruplos" in args
    ejecutar = "--ejecutar" in args
    imprimir_directorio = "--dir" in args
    
    archivos = [a for a in args if not a.startswith("--")]
    if len(archivos) != 1:
        print("Uso: python patito.py [--cuadruplos] [--dir] [--ejecutar] archivo.patito", file=sys.stderr)
        sys.exit(2)
    
    # pipeline de lectura y analisis
    # archivo -> stream -> lexer -> tokens -> parser -> arbol sintactico
    archivo = archivos[0]# lee el archivo que se pasa como argumento
    stream = FileStream(archivo) # crea un stream del archivo "el flujo de caracteres que vas a consumir es éste"
    lexer = PatitoLexer(stream) # crea un lexer del stream "el flujo de caracteres que vas a consumir es éste"
    tokens = CommonTokenStream(lexer)  # buffer de tokens para que parser pueda hacer un peek/lookahead
    parser = PatitoParser(tokens) # crea un instancia del parser autogenerado por antlr4
    
    #reemplazamos el error listener default por el nuestro (en lexer y parser)
    err_sintaxis = ContadorErrores()
    
    lexer.removeErrorListeners()
    lexer.addErrorListener(err_sintaxis)
    
    parser.removeErrorListeners()
    parser.addErrorListener(err_sintaxis)
    
    
    # indica que la regla programa es la raiz del arbol sintactico y de ahi empieza el parse(entry point)
    # desencadena muchas llamadas hasta llegar a las hojas (tokens individuales como PROGRAMA, ID, PCOMA, etc.)
    # devuelve Programa Context (el nodo raiz del arbol sintactico)
    tree = parser.programa()
    # Si hubo errores sintacticos, no tiene sentido seguir
    if err_sintaxis.errores > 0:
        sys.exit(1)
   
    # Analisis semantico, y trackeo de errores semanticos
    analizador = SemanticAnalyzer()
    walker = ParseTreeWalker()
    walker.walk(analizador, tree) 
    
    # si hay errores en la semantica, sale con codigo 1 (error)
    # si no hay errores, sale con codigo 0 (exito)
    if analizador.errores > 0:
        sys.exit(1)
    # si se paso el flag --cuadruplos, imprime la tabla de constantes y la fila de cuadruplos
    if imprimir_cuadruplos:
        analizador.cte.imprimir()
        print()
        analizador.gen.imprimir_fila()
    # si se paso el flag --ejecutar, ejecuta la maquina virtual
    if ejecutar:
        try:
            MaquinaVirtual(analizador).ejecutar()
        except RuntimeError as e:
            print(f"VM error: {e}", file=sys.stderr)
            sys.exit(1)
    if imprimir_directorio:
        analizador.imprimir_directorio()
    sys.exit(0) # si no hay errores, sale con codigo 0 (exito)
    
if __name__ == "__main__":
    main()
