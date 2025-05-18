from io import TextIOWrapper
from Parser import *
from globalTypes import NodoArbol
from globalTypes import TipoExpresion as Enu_ex
from semantica import *

#region variables globales
word_size = 4
variables_globales= {}
offset = 0
temp = 0




# region recorrer
def recorrer(file: TextIOWrapper, AST):
    '''
    recorrer Recorre todo el AST para generar código UwU

    Potri si ves esto, Hice un cambio a la forma de generar el código, para asi tener un mejor control de los nodos
    Siendo que el AST lo manejamos como una lista, pero por cada elemento de la lista, es una función
    
    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    global variables_globales, offset,temp

    tabla_resultado = regresar_tabla()#tabla de simbolos de la semantica a analizar

    for var in tabla_resultado["global"]:
        #A considerar el array a futuro
        if var['tipo'] == "int":
            offset -= word_size
            variables_globales[var.nombre] = offset

    for nodo in AST:
        if nodo.tipoNodo == Enu_ex.FunDec:# aqui empezamos a definir la funcion osea el collee
            #siendo el caso de una funcion
            generador_callee(file, nodo)
                           
                

#Aqui se maneja la el DecFuncion
def generador_callee(file: TextIOWrapper, nodo: NodoArbol):
    '''
    Potri Aqui se maneja la el DecFuncion
    de la forma de que el profesor nos dijo que lo hiciéramos
    Solo manejor el main diferente debido a que es la primera funcion
    por ende no tiene un control link
    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''

    file.write(f'  .{nodo.nombre}:\n')
    if nodo.nombre != "main":
        file.write(f'    move $fp $sp\n')
        file.write(f'    addiu $sp $sp -{word_size}\n')

    if nodo.parteInterna:
        for sub_nodo in nodo.parteInterna.sentencias:
            #print(sub_nodo)
            generador_parteInterna(file, sub_nodo)

    if nodo.nombre == "main":
        file.write(f'    li $v0 10\n')
        file.write(f'    syscall\n')
    else:
        file.write(f'    lw $ra {word_size}($sp)\n')
        if nodo.parametros:
            longitud = len(nodo.parametros)
            file.write(f'    addiu $sp $sp {longitud * word_size+8}\n')
            file.write(f'    lw $fp 0($sp)\n')
            file.write(f'    jr $ra\n')


def  generador_parteInterna(file: TextIOWrapper, nodo: NodoArbol):
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

    print('tipo de nodo')
    print(tipoNodo)

    match tipoNodo:
        case None:
            pass
        case Enu_ex.ExpreStmt:
            #aqui se maneja la expresion
            #es decir la suma, resta, multiplicacion y division
            if(nodo.expresion):
                generador_expresion(file, nodo.expresion)
        case Enu_ex.Op:
            if tipoOperador == "=":
                #aqui se maneja la asignacion
                var_temp = nodo.hijoIzquierdo.nombre
                valor = generador_expresion(file, nodo.hijoDerecho)
                offset = variables_globales[var_temp]
                if offset is not None:
                    file.write(f'  sw {valor} {offset}($sp)\n')
        case Enu_ex.While:
            raise NotImplementedError()
        case Enu_ex.If:
            #aqui podriamos implementar un funcion que administres las etiquetas
            #a los ifs u whiles
            raise NotImplementedError()
        
            #aqui administramos el else
            #if nodo.sino:
            #    nodo.sino.TipoNodo = Enu_ex.compoundStmt
            #    for sub_nodo in nodo.sino:
            #        generador_parteInterna(file, sub_nodo)
            # else:
            #     generador_parteInterna(file, nodo.sino)
        case Enu_ex.Return:
            raise NotImplementedError()
                

def generador_expresion(file: TextIOWrapper, nodo: NodoArbol):
    '''
    Potri Aqui se maneja la expresion
    siendo la suma, resta, multiplicacion y division
    operadores logicos
    y el coller/call de la funcion
    siendo aqui que si podemos manejar el yield
     Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    tipoNodo: Enu_ex | None
    tipoNodo = nodo.tipoNodo
    tipoOperador: str | None = nodo.operador
    print('entre a expresion soy del tipo ' , tipoNodo)
    match tipoNodo:
        case None:
            pass
        case Enu_ex.Const:
            const(file, nodo.valor)

        case Enu_ex.Op:
            match tipoOperador:
                case "+":
                    for n in suma(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        print(n)
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
                case "==":
                    raise NotImplementedError()
                case "!=":
                    raise NotImplementedError()
                case "<":
                    raise NotImplementedError()
                case ">":
                    raise NotImplementedError()
                case "<=":
                    raise NotImplementedError()
                case ">=":
                    raise NotImplementedError()
                case "=":
                    raise NotImplementedError()
        case Enu_ex.Var:
            raise NotImplementedError()
        case Enu_ex.Call:
            raise NotImplementedError()




def pasarACódigo(AST, filename: str = 'out.asm') -> None:
    with open(filename, 'x') as f:
        f.write(f' .text\n')
        f.write(f' .globl main\n')
        recorrer(f, AST)


# endregion

# region cmd ops

def suma(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  add $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def resta(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  sub $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def mult(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  mul $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def div(file: TextIOWrapper, nodos):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  div $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


# endregion
# region cmd var/const/etc

def const(file: TextIOWrapper, valor):
    file.write(f'  li $a0 {valor}\n')


def var_write(file: TextIOWrapper,):
    raise NotImplementedError()


def var_read(file: TextIOWrapper,):
    raise NotImplementedError()


# endregion
# region cmd sys-call


def read(file: TextIOWrapper, nodos):
    raise NotImplementedError()


def write(file: TextIOWrapper, nodos):
    raise NotImplementedError()


# endregion
# region conditionals and loops


def make_if(file: TextIOWrapper, nodos):
    raise NotImplementedError()


def make_while(file: TextIOWrapper, nodos):
    raise NotImplementedError()


# endregion
# region functions


def define_function(file: TextIOWrapper, nodos):
    raise NotImplementedError()


def call_function(file: TextIOWrapper, nodos):
    raise NotImplementedError()


# endregion
