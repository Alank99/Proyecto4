from globalTypes import *
from semantica import *
from Parser import *
from cgen import pasarACódigo



f = open("test5.c-", "r")
program = f.read()
programLong = len(program)
program = program + "$"
posicion = 0

# Caso de prueba original

globales(program, posicion, programLong)

AST: list[NodoArbol]
AST, Error = parser(True)

semantica(AST, True)

pasarACódigo(AST)
