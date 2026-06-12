import sqlite3
from config import path_db
from db import queries


def init_db():
    conn = sqlite3.connect("db/todo.db")
    cursor = conn.cursor()
    cursor.execute(queries.create table)
    print
    conn.commit()
    conn.close() 