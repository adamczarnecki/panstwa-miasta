import random
from data import *


def find_3(litera, lista):
    litera = str(litera)[0].upper()
    wybrane = []
    for element in lista:
        if litera == element[0]:
            wybrane.append(element)

    if len(wybrane) < 3:
        for x in wybrane:
            print(x)
    else:
        for x in random.sample(wybrane, 3):
            print(x)


def raz_dwa_trzy(litera):
    litera = str(litera)[0].upper()
    print('\n3 państwa na literę %s:' % (litera))
    find_3(litera, panstwa)

    print('\n3 miasta w Polsce na literę %s:' % (litera))
    find_3(litera, polskie_miasta)

    print('\n3 miasta na świecie na literę %s:' % (litera))
    find_3(litera, miasta_swiata)

    print('\n3 imiona żeńskie na literę %s:' % (litera))
    find_3(litera, imiona_damskie)

    print('\n3 imiona męskie na literę %s:' % (litera))
    find_3(litera, imiona_meskie)


if __name__ == '__main__':
    try:
        while True:
            litera = input('\nJaka litera? ')
            raz_dwa_trzy(litera)

    except KeyboardInterrupt:
        print('\n\nKoniec psot\n')
