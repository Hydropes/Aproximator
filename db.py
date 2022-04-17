import sqlite3 as sq

with sq.connect('sq2048.db') as con:
    cur =con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        name TEXT,
        score INTEGER
        )""")
