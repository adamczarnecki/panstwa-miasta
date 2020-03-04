import sqlite3


def sql_connection():
    try:
        con = sqlite3.connect('baza-hasel.db')
        return con
    except Error:
        print(Error)
    # finally:
    #     con.close()


def sql_table(con, table_name, table_columns):
    cursorObj = con.cursor()
    cursorObj.execute('CREATE TABLE %s(%s);' % (table_name, table_columns))
    con.commit()


def sql_insert(con, table_name, data):
    cursorObj = con.cursor()
    cursorObj.execute("INSERT INTO %s VALUES(%s);" % (table_name, data))
    con.commit()


def get_first_free_id(con, table):
    cursorObj = con.cursor()
    query = '''
            SELECT
              `id`
            FROM
              `%s`
            order by
              id desc
            limit
                1;

        ''' % (table)
    # print(query)
    rows = cursorObj.execute(query)
    try:
        return list(rows)[0][0] + 1
    except IndexError:
        return 1


def sql_insert_new_rodzaj(con, rodzaj):
    cursorObj = con.cursor()
    new_id = get_first_free_id(con, 'rodzaje')
    query = "INSERT INTO `rodzaje` VALUES(%s, '%s');" % (new_id, rodzaj)
    print(query)
    cursorObj.execute(query)
    con.commit()
    return new_id


def sql_insert_haslo(con, rodzaj_id, haslo):
    cursorObj = con.cursor()
    new_id = get_first_free_id(con, 'hasla')
    query = '''INSERT INTO `hasla` VALUES(%s, %s, "%s");''' % (new_id, rodzaj_id, haslo)
    try:
        cursorObj.execute(query)
    except sqlite3.OperationalError:
        print('ERROR:\n')
    print(query)
    con.commit()


def sql_create_and_insert(con, rodzaj, iterable):
    rodzaj_id = sql_insert_new_rodzaj(con, rodzaj)
    for obj in iterable:
        sql_insert_haslo(con, rodzaj_id, obj)


def sql_fetch_all(con, table_name):
    cursorObj = con.cursor()
    cursorObj.execute("SELECT * FROM `%s`;" % (table_name))
    for row in cursorObj.fetchall():
        print(row)


def sql_clear_table(con, table):
    cursorObj = con.cursor()
    cursorObj.execute("DELETE FROM %s" % table)
    con.commit()


if __name__ == '__main__':
    con = sql_connection()

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
