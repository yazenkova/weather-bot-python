import sqlite3


def connect():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS [user] (
                    user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    chat_id varchar(20) NOT NULL,
                    city varchar(20) NOT NULL,
                    date_and_time datetime NOT NULL);""")
    conn.commit()
    return cursor, conn


def add(chat_id, city):
    cursor, conn = connect()
    cursor.executemany('INSERT INTO user '
                       '(chat_id, city, date_and_time) VALUES'
                       ' (?, ?, date(\'now\'));', [(chat_id, city)])
    conn.commit()


def remove_all_for_user(chat_id):
    cursor, conn = connect()
    cursor.execute('DELETE FROM user WHERE chat_id = ? ;', [(chat_id)])
    conn.commit()


def get_cities(chat_id):
    cursor, conn = connect()
    cursor.execute('SELECT city FROM user WHERE chat_id = ?;', [(chat_id)])
    list_of_cities = []
    for row in cursor:
        list_of_cities.append(row[0])
    return list_of_cities
