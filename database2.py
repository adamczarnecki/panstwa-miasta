import sqlite3


def sql_connection():
    try:
        con = sqlite3.connect('baza-hasel2.db')
        return con
    except Error:
        print(Error)
    # finally:
    #     con.close()


def sql_create_table(con, table_name, table_columns):
    cursorObj = con.cursor()
    query = 'CREATE TABLE IF NOT EXISTS %s(%s);' % (table_name, table_columns)
    print(query)
    cursorObj.execute(query)
    con.commit()


def sql_clear_table(con, table):
    cursorObj = con.cursor()
    print("DELETE FROM %s" % table)
    cursorObj.execute("DELETE FROM %s" % table)
    con.commit()


def sql_insert(con, table, values):
    cursorObj = con.cursor()
    query = '''INSERT INTO `%s` (`name`) VALUES('%s') ''' % (table, values)
    print(query)
    cursorObj.execute(query)
    con.commit()


def sql_create_rodzaj(con, rodzaj):
    sql_insert(con, 'rodzaje', rodzaj)

    cursorObj = con.cursor()
    query = '''SELECT `id` FROM `rodzaje` WHERE `name` = "%s" ''' % (rodzaj)
    print(query)
    rows = cursorObj.execute(query)
    rodzaj_id = list(rows)[0][0]
    print('ID: ', rodzaj_id)
    return rodzaj_id


def sql_create_and_insert(con, rodzaj, iterable):
    cursorObj = con.cursor()
    rodzaj_id = sql_create_rodzaj(con, rodzaj)

    print('INSERT INTO `hasla` (`rodzaj`, `name`) VALUES(%s, ?)' % (rodzaj_id))
    cursorObj.executemany('INSERT INTO `hasla` (`rodzaj`, `name`) VALUES(%s, ?)' % (rodzaj_id), [(x, ) for x in iterable])
    """.executemany iteruje po każdym obiekcie w iterable. Dlatego musi być dawać się iterować (srt, tuple list),
        ale dlatego też każdy dający sie przeiterować będzie podany jako osobny argument.
        Dlatego:
        cursorObj.executemany('INSERT INTO `hasla` (`rodzaj`, `name`) VALUES(%s, ?)' % (rodzaj_id), iterable)
        zwraca błąd:
        sqlite3.ProgrammingError: Incorrect number of bindings supplied. The current statement uses 1, and there are 10 supplied.
        ponieważ 'Afganistan' ma 10 liter...
        Dlatego musimy podać listę haseł jako listę krotek z jedną wartością.
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
