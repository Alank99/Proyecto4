from io import TextIOWrapper
from Parser import *
from globalTypes import NodoArbol
from globalTypes import TipoExpresion as Enu_ex
from semantica import *
"""
Generador de código MIPS para C-
Creado por Alan Hernández y Alejandro Fernández
Fecha de entrega: 29 de mayo de 2025

"""

# region variables globales
word_size = 4
offset = 0
temp = 0
contador_etiquetas = 0

variables_locales = {}  # nombre funcion -> {nombre variable -> offset}
funcion_actual = None


def nueva_etiqueta(tipo: str = "etiqueta"):
    global contador_etiquetas
    etiqueta = f'{tipo}_{contador_etiquetas}'
    contador_etiquetas += 1
    return etiqueta


# region recorrer
def recorrer(file: TextIOWrapper, AST):
    '''
    recorrer Recorre todo el AST para generar código 
    ademas de generar las variables globales y locales
    busca por funciones y las genera

    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    global variables_globales, offset, temp, funcion_actual

    tabla_resultado: dict[str, list[dict[str, str | bool]]]
    tabla_resultado = regresar_tabla()  # tabla de simbolos de la semantica a analizar

    file.write(f'# variables\n')
    file.write(f'.data\n\n')
    #longitud = 0

    # Escribe las variables globales y locales
    for fname, funcData in tabla_resultado.items():
        file.write(f'  # v - {fname}\n')
        for var in funcData:
            if var["tipo"] == 'int':
                if var["tipo"] == 'int':
                    if var['array']:
                        longitud = int(var['tamaño']) * word_size
                        if fname == "global":
                            file.write(f'  var{var["nombre"]}: .space {longitud}\n')
                        if fname == "main":
                            file.write(f'  mvar{var["nombre"]}: .space {longitud}\n')
                        else:
                            file.write(f'  {fname}var{var["nombre"]}: .space {longitud}\n')
                        
                    else:
                        if fname == "global":
                            file.write(f'  var{var["nombre"]}: .word 0\n')
                        else:
                            if fname == "main":
                                file.write(f'  mvar{var["nombre"]}: .word 0\n')
                            else:
                                file.write(f'  {fname}var{var["nombre"]}: .word 0\n')

        file.write(f'  \n')

    file.write(f'.text\n')
    file.write(f'.globl main\n\n')

    for var in tabla_resultado["global"]:
        # A considerar el array a futuro
        if var['tipo'] == "int":
            offset -= word_size
            variables_globales[var['nombre']] = offset

    for nodo in AST:
        if nodo.tipoNodo == Enu_ex.FunDec:  # aqui empezamos a definir la funcion osea el collee
            funcion_actual = nodo.nombre
            # siendo el caso de una funcion
            generador_callee(file, nodo)


current_func = None

# Aqui se maneja la el DecFuncion

currentParams = []

def generador_callee(file: TextIOWrapper, nodo: NodoArbol):
    '''
    manejo de la generacion de la funcion de los callee y generacion internas de cada parte de la funcion
    y se administran los parametros de la funcion
    ademas de que se maneja el main como una funcion especial
    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    global currentParams

    currentParams = [n.nombre for n in nodo.parametros] if nodo.parametros != None else []

    if nodo.nombre != "main":
        file.write(f'func{nodo.nombre}:\n')
        file.write(f'  move $fp $sp\n')
        file.write(f'  sw $ra 0($sp)\n')
        file.write(f'  addiu\t $sp \t$sp \t-{word_size}\n')
        file.write(f'  # start function\n\n')
    else:
        file.write(f'main:\n')


    if nodo.parteInterna:
        for sub_nodo in nodo.parteInterna.sentencias:
            # print(sub_nodo)
            generador_parteInterna(file, sub_nodo)

    if nodo.nombre == "main":
        file.write(f'  # end call\n')
        file.write(f'  li $v0 10\n')
        file.write(f'  syscall\n\n')
    else:
        file.write(f'  \n')
        file.write(f'  # end function\n')
        file.write(f'  lw $ra {word_size}($sp)\n')
        if nodo.parametros:
            longitud = len(nodo.parametros)
            file.write(f'  addiu $sp $sp {longitud * word_size+8}\n')
            file.write(f'  lw $fp 0($sp)\n')
            file.write(f'  jr $ra\n')
        else:
            file.write(f'  addiu $sp $sp 8\n')
            file.write(f'  lw $fp 0($sp)\n')
            file.write(f'  jr $ra\n\n')


def generador_parteInterna(file: TextIOWrapper, nodo: NodoArbol):
    '''
    Potri Aqui se maneja la parte de la funcion interna
    aqui podemos manejar el if, while, return y el compoundStmt y asignaciones
    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''

    tipoNodo: Enu_ex | None
    tipoNodo = nodo.tipoNodo
    tipoOperador: str | None = nodo.operador

    match tipoNodo:
        case None:
            pass
        case Enu_ex.ExpreStmt:
            # aqui se maneja la expresion
            # es decir la suma, resta, multiplicacion y division
            if (nodo.expresion):
                generador_expresion(file, nodo.expresion)
        case Enu_ex.Op:
            generador_expresion(file, nodo)
        case Enu_ex.While:
            for n in make_while(file, [nodo.condicion, nodo.entonces]):
                if n != None:
                    if n.sentencias:
                        for s in n.sentencias:
                            generador_parteInterna(file, s)

                    else:
                        generador_parteInterna(file, n)
        case Enu_ex.If:
            for n in make_if(file, [nodo.condicion, nodo.entonces, nodo.sino]):
                if n != None:
                    if n.sentencias:
                        for s in n.sentencias:
                            generador_parteInterna(file, s)

                    else:
                        generador_parteInterna(file, n)

        case Enu_ex.Return:
            make_return(file, nodo)


def generador_expresion(file: TextIOWrapper, nodo: NodoArbol):
    '''
   Aqui se maneja la expresion
    siendo la suma, resta, multiplicacion y division
    operadores logicos
    y el coller/call de la funcion
    donde lo hijos u operadores anidados se maneja con yield para un manejo mas eficiente y lectura del codigo sencilla
     Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    tipoNodo: Enu_ex | None
    tipoNodo = nodo.tipoNodo
    tipoOperador: str | None = nodo.operador
    match tipoNodo:
        case None:
            pass
        case Enu_ex.Const:
            const(file, nodo.valor)

        case Enu_ex.Op:
            match tipoOperador:
                case "+":
                    for n in suma(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)

                case "-":
                    for n in resta(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)

                case "*":
                    for n in mult(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)

                case "/":
                    for n in div(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)
                case "<":
                    for n in menor(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)
                case ">":
                    for n in mayor(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)
                case "==":
                    for n in igual(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        generador_expresion(file, n)
                case "= ":
                    # aqui se maneja la asignacion
                    if nodo.hijoIzquierdo.indice:
                        for n in var_write_array(file, [nodo.hijoIzquierdo.indice, nodo.hijoDerecho], nodo.hijoIzquierdo.nombre):
                            generador_expresion(file, n)
                    else:
                        var_temp = nodo.hijoIzquierdo
                        generador_expresion(file, nodo.hijoDerecho)
                        var_write(file, var_temp)
        case Enu_ex.Var:

            var_read(file, nodo)
        case Enu_ex.Call:
            call_function(file, nodo)


def pasarACódigo(AST, filename: str = 'out.asm') -> None:
    with open(filename, 'w') as f:
        recorrer(f, AST)


# endregion

# region cmd ops

def suma(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  # sumar\n')
    file.write(f'  sw \t$a0 \t0($sp)\n')
    file.write(f'  addiu \t$sp \t$sp \t-{word_size}\n\n')

    yield nodos[1]
    file.write(f'  # suma - guardar resultado\n')
    file.write(f'  lw \t$t1 \t{word_size}($sp)\n')
    file.write(f'  add \t$a0 \t$t1 \t$a0\n')
    file.write(f'  addiu \t$sp \t$sp \t{word_size}\n\n')


def resta(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  # resta\n')
    file.write(f'  sw \t$a0 \t0($sp)\n')
    file.write(f'  addiu \t$sp \t$sp \t-{word_size}\n\n')

    yield nodos[1]
    file.write(f'  # resta - guardar resultado\n')
    file.write(f'  lw \t$t1 \t{word_size}($sp)\n')
    file.write(f'  sub \t$a0 \t$t1 \t$a0\n')
    file.write(f'  addiu \t$sp \t$sp \t{word_size}\n\n')


def mult(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw \t$a0 \t0($sp)\n')
    file.write(f'  addiu \t$sp \t$sp \t-{word_size}\n')

    yield nodos[1]
    file.write(f'  lw \t$t1 \t{word_size}($sp)\n')
    file.write(f'  mul $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def div(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw \t$a0 \t0($sp)\n')
    file.write(f'  addiu \t$sp \t$sp \t-{word_size}\n')

    yield nodos[1]
    file.write(f'  lw \t$t1 \t{word_size}($sp)\n')
    file.write(f'  div \t$a0 \t$t1 \t$a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def menor(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  slt $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def mayor(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu \t$sp \t$sp \t-{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  slt $a0 $a0 $t1\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def igual(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  seq $a0 $a0 $t1\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def diferente(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  sne $a0 $a0 $t1\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def menor_igual(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp \t$sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  slt $a0 $t1 $a0\n')
    file.write(f'  xor $a0 $a0 1\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def mayor_igual(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size}($sp)\n')
    file.write(f'  slt $a0 $a0 $t1\n')
    file.write(f'  xor $a0 $a0 1\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


# endregion
# region cmd var/const/etc

def const(file: TextIOWrapper, valor):
    file.write(f'  # constante\n')
    file.write(f'  li $a0 {valor}\n\n')


def var_write_array(file: TextIOWrapper, nodos, name):
    global funcion_actual
    tabla_resultado = regresar_tabla()

    # Buscar el símbolo
    for simbolo in tabla_resultado[funcion_actual]:
        if simbolo['nombre'] == name:
            es_local = True
            break

    etiqueta = (
        f'{funcion_actual}var{name}' if funcion_actual != "main" and es_local else
        f'mvar{name}' if funcion_actual == "main" and es_local else
        f'var{name}'
    )

    #primero conseguimos el indice
    file.write(f'  # conseguimos el indice \n')  
    yield nodos[0]
    file.write(f'  # buscamos el lugar en el array\n')
    file.write(f'  mul $t0 $a0 4\n')  # multiplicamos el indice por 4
    #conseguimos el nuevo valor de la variable

    file.write(f'  # guardamos el valor en la variable\n')
    yield nodos[1]
    file.write(f'  sw $a0 {etiqueta}($t0)\n')  # guardamos el valor en la variable
    file.write(f'  # fin variable array {etiqueta}\n')

#codigo de inspiracion https://profile.iiita.ac.in/bibhas.ghoshal/COA_2020/Lab/Array_MIPS.pdf
def var_write(file: TextIOWrapper, nodo: NodoArbol):
    global funcion_actual
    tabla_resultado = regresar_tabla()

    # Buscar el símbolo
    for simbolo in tabla_resultado[funcion_actual]:
        if simbolo['nombre'] == nodo.nombre:
            es_local = True
            break

    etiqueta = (
        f'{funcion_actual}var{nodo.nombre}' if funcion_actual != "main" and es_local else
        f'mvar{nodo.nombre}' if funcion_actual == "main" and es_local else
        f'var{nodo.nombre}'
    )

    file.write(f'  sw $a0 {etiqueta}\n') 



def var_read(file: TextIOWrapper, nodo: NodoArbol):
    global funcion_actual

    # vemos si se busca un array
    is_array = False
    if nodo.indice:
         is_array = True


    if nodo.nombre in currentParams:
        #en caso de que sea un array
        if is_array:
        #hacer las operaciones internas del array
             file.write(f'  lw $a0 {4 + count - index}($sp)\n')
             generador_expresion(file, nodo.indice)
             file.write(f'  mul $a0 $a0 {word_size}\n')
             file.write(f'  add $a0 $a0 {index}\n')
             file.write(f'  lw $a0 {4 + count - index}($sp)\n')
             generador_expresion(file, nodo.indice)
             file.write(f'  mul $a0 $a0 {word_size}\n')
             file.write(f'  add $a0 $a0 {index}\n')
             file.write(f'  lw $a0 {4 + count - index}($sp)\n')
             return
        else:
            index = currentParams.index(nodo.nombre) * 4
            count = len(currentParams) * 4
            file.write(f'  lw $a0 {4 + count - index}($sp)\n')
            return
    
    tabla_resultado: dict[str, list[dict[str, str | bool]]]
    tabla_resultado = regresar_tabla()
    es_local = False    
    #buscamos el scoope de la variable

    for simbolo in tabla_resultado[funcion_actual]:
        if simbolo['nombre'] == nodo.nombre:
            es_local = True
            break

    etiqueta = f'{funcion_actual}var{nodo.nombre}' if funcion_actual != "main" and es_local else f'mvar{nodo.nombre}' if funcion_actual == "main" and es_local else f'var{nodo.nombre}'
    #para cuando es una variable en su funcion o global
    if is_array:
        generador_expresion(file, nodo.indice)
        file.write(f'  mul $t0, $a0, 4\n')      # índice * 4
        file.write(f'  lw $a0, {etiqueta}($t0)\n')  # acceso tipo arreglo(nombre) como en imagen
    else: # si fuera una variable normal
        file.write(f'  # variable {etiqueta}\n')
        file.write(f'  lw $a0 {etiqueta}\n')


# endregion
# region cmd sys-call


def read(file: TextIOWrapper, nodos):
    file.write(f'  # input\n')
    file.write(f'  li $v0 5\n')
    file.write(f'  syscall\n')
    file.write(f'  move $a0 $v0\n\n')


def write(file: TextIOWrapper, nodos):
    generador_expresion(file, nodos.argumentos[0])

    file.write(f'  # output\n')
    file.write(f'  li $v0 1\n')
    file.write(f'  syscall\n\n')


# endregion
# region conditionals and loops

def make_if(file: TextIOWrapper, nodos: list[NodoArbol]):

    # generacion de etiquetas
    nueva_etiquetaElse = nueva_etiqueta("else")
    nueva_etiquetaFin = nueva_etiqueta("fin")

    file.write(f'  # if statement\n')
    yield nodos[0]
    file.write(f'  beq $a0 $zero {nueva_etiquetaElse}\n')

    file.write(f'# if true\n')
    yield nodos[1]
    file.write(f'  j {nueva_etiquetaFin}\n\n')

    file.write(f'# if false\n')
    file.write(f'{nueva_etiquetaElse}:\n')
    yield nodos[2]
    file.write(f'  j {nueva_etiquetaFin}\n\n')

    file.write(f'# end if\n')
    file.write(f'{nueva_etiquetaFin}:\n')


def make_while(file: TextIOWrapper, nodos):
    nueva_etiquetaInicio = nueva_etiqueta("while")
    nueva_etiquetaFin = nueva_etiqueta("end")

    file.write(f'# While\n')
    file.write(f'{nueva_etiquetaInicio}:\n')
    file.write(f'# comparacion\n')

    yield nodos[0]

    file.write(f'  beq $a0 $zero {nueva_etiquetaFin}\n')
    file.write(f'# code\n')

    yield nodos[1]

    file.write(f'  j {nueva_etiquetaInicio}\n\n')
    file.write(f'# end while\n')
    file.write(f'{nueva_etiquetaFin}:\n\n')


def make_return(file: TextIOWrapper, nodos):
    if nodos.expresion:
        generador_expresion(file, nodos.expresion)
        file.write(f'  move $v0 $a0\n')


# endregion
# region functions

def call_function(file: TextIOWrapper, nodos: NodoArbol):

    if nodos.nombre == "input":
        read(file, nodos)
        return
    if nodos.nombre == "output":
        write(file, nodos)
        return

    file.write(f'  sw $fp 0($sp)\n')
    file.write(f'  addiu $t2 $sp -{word_size}\n')
    for param in nodos.argumentos:
        file.write(f'  # param {param.nombre}\n')
        generador_expresion(file, param)
        file.write(f'  # save param\n')
        file.write(f'  sw $a0 0($t2)\n')
        file.write(f'  addiu $t2 $t2 -{word_size}\n\n')
    file.write(f'  move $sp $t2\n')
    file.write(f'  jal func{nodos.nombre}\n')

# endregion