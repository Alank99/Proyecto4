from io import TextIOWrapper
from Parser import *
from globalTypes import NodoArbol
from globalTypes import TipoExpresion as Enu_ex
from semantica import regresar_tabla

#region variables globales
word_size = 4
offset_variables = {}
offset = 0
temp = 0



# region recorrer
def recorrer(file: TextIOWrapper, nodo: NodoArbol | list[NodoArbol]):
    '''
    recorrer Recorre todo el AST para generar código UwU

    Args:
        file (TextIOWrapper): el archivo
        nodo (NodoArbol | list[NodoArbol]): Una lista de nodos o el nodo como tal 
    '''
    if isinstance(nodo, list):
        # en caso de que sea una lista porque no existe estandarización aqu
        for sub_nodo in nodo:
            recorrer(file, sub_nodo)
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
        recorrer(file,  hijo)

    for lista in (
        nodo.parametros,
        nodo.sentencias,
        nodo.argumentos,
    ):
        if lista:
            for sub_nodo in lista:
                recorrer(file, sub_nodo)



    tipoNodo: Enu_ex | None
    tipoNodo = nodo.tipoNodo


    tipoOperador: str | None = nodo.operador

    match tipoNodo:
        case None:
            pass
        case Enu_ex.Op:
            match tipoOperador:
                case "+":
                    for n in suma(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        print(n)
                        recorrer(file, n)

                case "-":
                    for n in resta(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        recorrer(file, n)

                case "*":
                    for n in mult(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        recorrer(file, n)

                case "/":
                    for n in div(file, [nodo.hijoIzquierdo, nodo.hijoDerecho]):
                        recorrer(file, n)
        case Enu_ex.Const:
            const(file, nodo.valor)

        case Enu_ex.Var:
            var(file, )

        case Enu_ex.Call:
            for n in call_function(file, []):  # TODO definir nodos
                recorrer(file, n)

        case Enu_ex.VarDec:
            raise NotImplementedError()

        case Enu_ex.FunDec:
            pass
            for n in define_function(file, []):  # TODO definir nodos
                recorrer(file, n)

        case Enu_ex.ExpreStmt:
            raise NotImplementedError()
        case Enu_ex.Op:
            raise NotImplementedError()

        case Enu_ex.Return:
            raise NotImplementedError()

        case Enu_ex.If:
            for n in make_if(file, []):  # TODO definir nodos
                recorrer(file, n)

        case Enu_ex.While:
            for n in make_while(file, []):  # TODO definir nodos
                recorrer(file, n)

        case Enu_ex.compoundStmt:
            raise NotImplementedError()


def pasarACódigo(AST: list[NodoArbol], filename: str = 'out.asm') -> None:
    with open(filename, 'x') as f:
        f.write(f' .text\n')
        f.write(f' .globl main\n')
        f.write(f' main:\n')
        recorrer(f, AST)


# f = open("testoriginal.c-", "r")
# program = f.read()
# programLong = len(program)
# program = program + "$"
# posicion = 0
# globales(program, posicion, programLong)


# AST, Error = parser(False)

# endregion

# region cmd ops

def suma(file: TextIOWrapper, nodos: list[NodoArbol]):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  add $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def resta(file: TextIOWrapper, nodos: list[NodoArbol]):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  sub $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def mult(file: TextIOWrapper, nodos: list[NodoArbol]):
    yield nodos[0]
    file.write(f'  sw $a0 0($sp)\n')
    file.write(f'  addiu $sp $sp -{word_size}\n')

    yield nodos[1]
    file.write(f'  lw $t1 {word_size} ($sp)c\n')
    file.write(f'  mul $a0 $t1 $a0\n')
    file.write(f'  addiu $sp $sp {word_size}\n')


def div(file: TextIOWrapper, nodos: list[NodoArbol]):
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


def read(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


def write(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


# endregion
# region conditionals and loops


def make_if(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


def make_while(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


# endregion
# region functions


def define_function(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


def call_function(file: TextIOWrapper, nodos: list[NodoArbol]):
    raise NotImplementedError()


# endregion
