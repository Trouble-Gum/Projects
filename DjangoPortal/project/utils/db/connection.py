import sqlite3
from sqlite3 import Error


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        return conn
    except Error as e:
        print(e)

    return conn


def disconnect(conn: sqlite3.Connection):
    try:
        conn.close()
    except Error as e:
        print(e)
