"""
Cubo semantico para el lenguaje Patito

Solamente se declaran los datos y el Cubo que utiliza para resolver las expresiones.
"""


# Tipos de datos, por lo pronto no tenemos nula. 
ENTERO = 'entero'
FLOTANTE = 'flotante'
BOOL = 'bool'
# NULA = 'nula'

# Cubo semantico
_CUBO = {
    #Aritmeticos SUMA
    ("+", ENTERO, ENTERO): ENTERO,
    ("+", ENTERO, FLOTANTE): FLOTANTE,
    ("+", FLOTANTE, ENTERO): FLOTANTE,
    ("+", FLOTANTE, FLOTANTE): FLOTANTE,
    
    #Aritmeticos RESTA
    ("-", ENTERO, ENTERO): ENTERO,
    ("-", ENTERO, FLOTANTE): FLOTANTE,
    ("-", FLOTANTE, ENTERO): FLOTANTE,
    ("-", FLOTANTE, FLOTANTE): FLOTANTE,
    
    #Aritmeticos MULTIPLICACION
    ("*", ENTERO, ENTERO): ENTERO,
    ("*", ENTERO, FLOTANTE): FLOTANTE,
    ("*", FLOTANTE, ENTERO): FLOTANTE,
    ("*", FLOTANTE, FLOTANTE): FLOTANTE,
    
    #Aritmeticos DIVISION
    ("/", ENTERO, ENTERO): ENTERO,
    ("/", ENTERO, FLOTANTE): FLOTANTE,
    ("/", FLOTANTE, ENTERO): FLOTANTE,
    ("/", FLOTANTE, FLOTANTE): FLOTANTE,
    
    #Artimeticos Relacionales menor que
    ("<", ENTERO, ENTERO): BOOL,
    ("<", ENTERO, FLOTANTE): BOOL,
    ("<", FLOTANTE, ENTERO): BOOL,
    ("<", FLOTANTE, FLOTANTE): BOOL,
    
    #Artimeticos Relacionales mayor que
    (">", ENTERO, ENTERO): BOOL,
    (">", ENTERO, FLOTANTE): BOOL,
    (">", FLOTANTE, ENTERO): BOOL,
    (">", FLOTANTE, FLOTANTE): BOOL,
    
    #Artimeticos Relacionales igual que
    ("==", ENTERO, ENTERO): BOOL,
    ("==", ENTERO, FLOTANTE): BOOL,
    ("==", FLOTANTE, ENTERO): BOOL,
    ("==", FLOTANTE, FLOTANTE): BOOL,
    
    #Artimeticos Relacionales distinto que
    ("!=", ENTERO, ENTERO): BOOL,
    ("!=", ENTERO, FLOTANTE): BOOL,
    ("!=", FLOTANTE, ENTERO): BOOL,
    ("!=", FLOTANTE, FLOTANTE): BOOL,
    
    # Asignacion
    # entero=entero ok, flotante=flotante ok, flotante=enero ok, entero=flotante no
    ("=", ENTERO, ENTERO): ENTERO,
    ("=", FLOTANTE, FLOTANTE): FLOTANTE,
    ("=", FLOTANTE, ENTERO): FLOTANTE,
    # Rechazamos asignaciones de entero a flotante, para evitar perder el decimal. (NO AGREGAR)
}


# solo importamos esta funcion a otros archivos. Mantenemos el cubo encapsulado. 
def tipo_resultado(op, tipo_izq, tipo_der):
    """
    Retorna el tipo de resultado de la operacion. 
    si la combinacion de tipos no esta definida, retorna None.
    """
    
    return _CUBO.get((op, tipo_izq, tipo_der))
