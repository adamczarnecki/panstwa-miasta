import urllib.request
from bs4 import BeautifulSoup
import sys
import os


def get_all_pages_names(link):

    listy_kategorii = []
    lista_elementów_docelowych = []
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, 'html.parser')
    h1 = soup.select('h1')[0].getText()
    print('Czytam stronę %s' % (h1))
    current_page = soup.select('#mw-content-text li', href=True)

    for elem in current_page:
        if elem.select('.CategoryTreeSection') == []:
            lista_elementów_docelowych.append(elem.getText())
        else:
            listy_kategorii.append(elem.select('a', href=True)[0]['href'])

    for url in listy_kategorii:
        page = urllib.request.urlopen('https://pl.wikipedia.org' + url)
        soup = BeautifulSoup(page, 'html.parser')
        h1 = soup.select('h1')[0].getText()
        print('Czytam stronę "%s"' % (h1))
        current_page = soup.select('#mw-content-text li', href=True)
        for elem in current_page:
            if elem.select('.CategoryTreeSection') == []:
                lista_elementów_docelowych.append(elem.getText())
            else:
                listy_kategorii.append(elem.select('a', href=True)[0]['href'])

    return lista_elementów_docelowych


if __name__ == '__main__':
    try:
        file_name = str(sys.argv[1])
        url = str(sys.argv[2])
    except IndexError:
        print('Podaj nazwę pliku docelowego oraz adres pierwszej strony')

    path = os.path.dirname(os.path.abspath(__file__)) + '/'
    with open(path + file_name + '.txt', 'w', encoding='utf-8',) as f:
        k = sorted(get_all_pages_names(url))
        bez_powtorzen = [k[i] for i in range(len(k)) if i == 0 or k[i] != k[i - 1]]
        f.write(str(bez_powtorzen))
