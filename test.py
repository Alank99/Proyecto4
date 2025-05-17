from globalTypes import *
from semantica import *
from Parser import *

    



f = open("testconerror.c-", "r")
program = f.read()
programLong = len(program)
program = program + "$"
posicion = 0

#funciones para pasar los valores iniciales de las variables globales

globales(program, posicion, programLong)

#caso de prueba con error

AST,Error = parser(True)

if Error == True:
    print("Error en el analisis sintactico")
else:
    semantica(AST, True)


    f = open("testoriginal.c-", "r")
    program = f.read()
    programLong = len(program)
    program = program + "$"
    posicion = 0

    #Caso de prueba original

    globales(program, posicion, programLong)

    AST = parser(False)

    semantica(AST, True)


    