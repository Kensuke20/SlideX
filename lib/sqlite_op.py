import sqlite3

DB_FILE = './db/slidex.sqlite3'

# open data base
def open_db():
    # SELECT句の結果を辞書型で得られるようにする
    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = dict_factory
    return conn

# execute sql(EXECUTE)
def exec_db(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    db.commit()
    return c.lastrowid

# execute sql(SELECT)
def select_db(sql, *args):
    db = open_db()
    c = db.cursor()
    c.execute(sql, args)
    return c.fetchall()