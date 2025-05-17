from Parser import *
from globalTypes import *

#Archivo donde se genera el codigo maquina para mips
#imprime la tabla de simbolos y la tabla de funciones
#Creado para C- 
#Creado por: Alan Anthony Hernandez Perez
#Creado el: 29/05/2025
#con el asistente de copilot de vscode



def recorrerPostorden(nodo, indent=0):
    if isinstance(nodo, list):
        for subnodo in nodo:
            recorrerPostorden(subnodo, indent)
        return

    if nodo is None:
        return

    for hijo in (
        nodo.hijoIzquierdo,
        nodo.hijoDerecho,
        nodo.parteInterna,
        nodo.expresion,
        nodo.entonces,
        nodo.sino,
        nodo.condicion
    ):
        recorrerPostorden(hijo, indent + 1)

    for lista in (
        nodo.parametros,
        nodo.sentencias,
        nodo.argumentos,
    ):
        if lista:
            for subnodo in lista:
                recorrerPostorden(subnodo, indent + 1)

    tipo_nodo = nodo.tipoNodo.name if nodo.tipoNodo else "Ninguno"
    print("  " * indent + f"[POST] Nodo: {tipo_nodo} - {nodo.nombre or nodo.valor or nodo.operador}")


    





f = open("testoriginal.c-", "r")
program = f.read()
programLong = len(program)
program = program + "$"
posicion = 0
globales(program, posicion, programLong)



AST, Error = parser(False)

recorrerPostorden(AST)

