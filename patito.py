import sys

sys.path.insert(0, 'generated')

from antlr4 import FileStream, CommonTokenStream
from antlr4.error.ErrorListener import ErrorListener
from PatitoLexer import PatitoLexer
from PatitoParser import PatitoParser

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
    
    def syntaxError(self, recognizer, offendingSymbol, line, col, msg, e):
        # Imprimir error de sintaxis y contar los errores. (Las 6 params son de la libreria antlr4)
        # por ahora solo ocpamos linea, columna y mensaje.
        print(f"{recognizer} linea {line}:{col}  {msg}", file=sys.stderr)
        self.errores += 1
        
# ============================================================
# PARTE 2 - DRIVER
# ============================================================

def main ():
    # revisa que se haya pasado un archivo como argumento por eso son 2 (python patito.py(1) archivo.patito(2))
    if len(sys.argv) < 2:
        print("Uso: python patito.py archivo.patito", file=sys.stderr)
        sys.exit(2)
    
    # pipeline de lectura y analisis
    # archivo -> stream -> lexer -> tokens -> parser -> arbol sintactico
    archivo = sys.argv[1] # lee el archivo que se pasa como argumento
    steam = FileStream(archivo) # crea un stream del archivo "el flujo de caracteres que vas a consumir es éste"
    lexer = PatitoLexer(steam) # crea un lexer del stream "el flujo de caracteres que vas a consumir es éste"
    tokens = CommonTokenStream(lexer)  # buffer de tokens para que parser pueda hacer un peek/lookahead
    parser = PatitoParser(tokens) # crea un instancia del parser autogenerado por antlr4
    
    #reemplazamos el error listener default por el nuestro (en lexer y parser)
    err = ContadorErrores()
    
    lexer.removeErrorListeners()
    lexer.addErrorListener(err)
    
    parser.removeErrorListeners()
    parser.addErrorListener(err)
    
    # indica que la regla programa es la raiz del arbol sintactico y de ahi empieza el parse(entry point)
    # desencadena muchas llamadas hasta llegar a las hojas (tokens individuales como PROGRAMA, ID, PCOMA, etc.)
    # devuelve Programa Context (el nodo raiz del arbol sintactico)
    parser.programa()
    
    # si hay errores, sale con codigo 1 (error)
    # si no hay errores, sale con codigo 0 (exito)
    sys.exit(1 if err.errores > 0 else 0)
    
if __name__ == "__main__":
    main()
