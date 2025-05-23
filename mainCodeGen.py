from globalTypes import *
from semantica import *
from Parser import *
from cgen import pasarACódigo



f = open("test7.c-", "r")
program = f.read()
programLong = len(program)
program = program + "$"
posicion = 0

# Caso de prueba original

globales(program, posicion, programLong)

AST: list[NodoArbol]
AST, Error = parser(True)

if Error:
    print("Error en el parser")
    print("por ende no genera codigo")

Error = semantica(AST, True)

if Error:
    print("Error en la semantica")
    print("por ende no genera codigo")

if not Error:
    print("Generando código")
    # Generar código
    pasarACódigo(AST)
    print("Código generado")
