"""
conftest.py vacio. Su sola presencia le indica a pytest que esta carpeta es
un paquete de tests, y permite que pytest encuentre los fixtures (si los
agregas en el futuro) sin que tengas que importar nada explicitamente.

Por ahora no hay fixtures que compartir entre tests. Si mas adelante quieres,
por ejemplo, parsear un archivo .patito y reusar el AST entre varios tests,
aqui es donde definirias el fixture.
"""
