def hacerif(listaDeCodigos):
    print('Linea codigo if 1')
    yield listaDeCodigos[0]
    print('Linea codigo else')
    yield listaDeCodigos[1]
    print('Linea codigo end')

for instruction in hacerif([' codigo para if', ' codigo para else']):
    print(instruction)