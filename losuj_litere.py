# _*_ coding: utf-8 _*_
import random

litery = 'ABCDEFGHIJKLMNOPRSTUVWZ'
litery_lista = [x for x in litery]

print('\nAby wylosować literę, wciśnij ENTER')
numer_rundy = 0
while len(litery_lista) > 0:
    dummy_input = raw_input('')
    numer_rundy += 1
    wybrana_litera = random.choice(litery_lista)
    print('\nWybrana litera: %s\t%s/23' % (wybrana_litera, numer_rundy))
    litery_lista.remove(wybrana_litera)

print('\n KONIEC LITER\n')
