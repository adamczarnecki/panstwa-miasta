import sqlite3


def sql_connection():
    try:
        con = sqlite3.connect('baza-hasel2.db')
        # to niżej printuje zapytania sql
        # https://nelsonslog.wordpress.com/2016/03/18/python-sqlite3-query-logging/
        con.set_trace_callback(print)
        return con
    except Error:
        print(Error)
    # finally:
    #     con.close()


def sql_create_table(con, table_name, table_columns):
    cursorObj = con.cursor()
    query = 'CREATE TABLE IF NOT EXISTS %s(%s);' % (table_name, table_columns)
    cursorObj.execute(query)
    con.commit()


def sql_clear_table(con, table):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM %s" % (table))
    con.commit()


def sql_create_rodzaj(con, rodzaj):
    cursorObj = con.cursor()
    # insert rodzaj
    con.set_trace_callback(print)
    cursorObj.execute('''INSERT INTO `rodzaje` (`name`) VALUES(?);''', (rodzaj, ))
    con.commit()

    # Get id of inserted rodzaj
    rows = cursorObj.execute('''SELECT `id` FROM `rodzaje` WHERE `name` = ?;''', (rodzaj, ))
    rodzaj_id = list(rows)[0][0]
    return rodzaj_id


def sql_create_and_insert(con, rodzaj, iterable):
    cursorObj = con.cursor()
    rodzaj_id = sql_create_rodzaj(con, rodzaj)

    con.set_trace_callback(None)
    cursorObj.executemany('INSERT INTO `hasla` (`rodzaj`, `name`) VALUES(?, ?);', [(rodzaj_id, x) for x in iterable])
    """execute() i executemany przyjmuje tylko dwa arguenty. kwerenda i (ewentualnie) iterowalny obiekt to podstawiania "?"
        obiekt do podstawienia zostanie przeiterowany w poszukiwaniu pojedyńczych elementów.
        String możę być iterowany po każdej literze, więc jeżeli chcesz podstawić tylko jeden obiekt, trzeba go umiescić w ktotkę albo listę
        Jak się parametryzuje całe zapytanie to to staje sie logiczne i przestaje w ogóle dziwić ;P
    """


if __name__ == '__main__':
    con = sql_connection()

    columns = '''
        id integer NOT NULL PRIMARY KEY,
        name text NOT NULL
    '''
    sql_create_table(con, 'rodzaje', columns)
    columns = '''
        id integer NOT NULL PRIMARY KEY,
        rodzaj integer NOT NULL,
        name text NOT NULL,
        FOREIGN KEY (rodzaj) REFERENCES rodzaje (id)
    '''
    sql_create_table(con, 'hasla', columns)

    from data import *

    sql_clear_table(con, 'hasla')
    sql_clear_table(con, 'rodzaje')
    sql_create_and_insert(con, 'Państwa', panstwa)
    sql_create_and_insert(con, 'Polskie miasta', polskie_miasta)
    sql_create_and_insert(con, 'Imiona męskie', imiona_meskie)
    sql_create_and_insert(con, 'Imiona damskie', imiona_damskie)
    sql_create_and_insert(con, 'Miasta świata', miasta_swiata)
    sql_create_and_insert(con, 'Góry', gory)
    sql_create_and_insert(con, 'Zwierzeta', zwierzeta)
    sql_create_and_insert(con, 'Rośliny', rosliny)

    con.close()
