import urllib.request
from bs4 import BeautifulSoup
import sys
import os
import time
from langdetect import detect


def get_all_pages_names(link):

    listy_kategorii = []
    lista_elementow_docelowych = []
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    h1 = soup.select('h1')[0].getText()
    print('Czytam stronę: %s' % (h1))
    current_page = soup.select('.mw-category-generated li', href=True)
    is_next = soup.select('.mw-category-generated a', href=True)[-1]
    if 'następna strona' in is_next.getText():
        print('Jest następna strona %s' % (is_next['href']))
        listy_kategorii.append(is_next['href'])

    for elem in current_page:
        if elem.select('.CategoryTreeSection') == []:
            lista_elementow_docelowych.append(elem.getText())
        else:
            listy_kategorii.append(elem.select('a', href=True)[0]['href'])

    for url in listy_kategorii:
        page = urllib.request.urlopen('https://pl.wikipedia.org' + url)
        soup = BeautifulSoup(page, 'html.parser')
        h1 = soup.select('h1')[0].getText()
        if 'ymarłe' in h1:
            pass
        else:
            print('Czytam stronę: "%s"' % (h1))
            current_page = soup.select('.mw-category-generated li', href=True)
            is_next = soup.select('.mw-category-generated a', href=True)[-1]
            if 'następna strona' in is_next.getText():
                print('Jest następna strona %s' % (is_next['href']))
                listy_kategorii.append(is_next['href'])
            for elem in current_page:
                if elem.select('.CategoryTreeSection') == []:
                    lista_elementow_docelowych.append(elem.getText())
                else:
                    listy_kategorii.append(elem.select('a', href=True)[0]['href'])

    return lista_elementow_docelowych


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    if iteration == total: 
        print()


def remove_not_pl(lista):
    print('Przed czyszczeniem: %s' % (len(lista)))
    polska_lista = []
    count = 0
    printProgressBar(count, len(lista), prefix = 'Czyszczenie:', length = 50)
    for x in lista:
        if str(detect(x)) == 'pl':
            polska_lista.append(x)
        else:
            pass
        count += 1
        printProgressBar(count, len(lista), prefix = 'Czyszczenie:', length = 50)

    return polska_lista


if __name__ == '__main__':
    try:
        file_name = str(sys.argv[1])
        url = str(sys.argv[2])
        if 'https://pl.wikipedia.org/wiki/Kategoria:' not in url:
            print('Link musi prowadzić do strony kategorii na wikipedii!')
            raise
        remove_latin = int(sys.argv[3])
        if remove_latin not in [0, 1]:
            print('Podaj wartość 0 (znaczy nie usuwaj łaciny) lub 1 (znaczy usuń łacinę)')
            raise
    except IndexError:
        print('Podaj nazwę pliku docelowego, adres pierwszej strony z kategorii na wikipedii oraz czy usunąć nie polskie nazwy (0 lub 1)')
        raise

    start = time.time()
    k = sorted(get_all_pages_names(url))
    bez_powtorzen = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i - 1]]
    if remove_latin == 0:
        to_save = bez_powtorzen
    elif remove_latin == 1:
        to_save = remove_not_pl(bez_powtorzen)
    print('Gotowych do zapisania %s nazw' % (len(to_save)))

    path = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(path + file_name + '.txt', 'w', encoding='utf-8') as f:
        f.write(str(to_save))    
    end = time.time()
    print('\nTOTAL TIME: {} min. {} sec.\n'.format(int((end - start) // 60), int((end - start) % 60)))
