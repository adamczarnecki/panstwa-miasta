import random
from helper import xyz


def losuj_litere():
    litery = 'ABCDEFGHIJKLMNOPRSTUWZ'
    litery_lista = [x for x in litery]
    wybrana_litera = ''

    print('\nAby wylosować literę, wciśnij ENTER')
    numer_rundy = 0
    while len(litery_lista) > 0:
        dummy_input = input('')
        if dummy_input != '':
            xyz(wybrana_litera)
            dummy_input = input('')
        numer_rundy += 1
        wybrana_litera = random.choice(litery_lista)
        print('\nWybrana litera: %s\t%s/22' % (wybrana_litera, numer_rundy))
        litery_lista.remove(wybrana_litera)

    print('\n KONIEC LITER\n')


if __name__ == '__main__':
    losuj_litere()
