import sqlite_op, routing

def init_slidex_db():
    sqlite_op.exec_db('''
            /* photo info */
            CREATE TABLE IF NOT EXISTS photo (
            photo_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path       TEXT,
            created_year    INTEGER,
            created_month   INTEGER,
            created_day     INTEGER
            )
            ''')

    sqlite_op.exec_db('''
            /* album info */
            CREATE TABLE IF NOT EXISTS album (
            album_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            album_name    TEXT
            )
            ''')

    sqlite_op.exec_db('''
            /* mapping info */
            CREATE TABLE IF NOT EXISTS mapping (
            photo_id        INTEGER,
            album_id        INTEGER,
            PRIMARY KEY(photo_id, album_id)
            )
            ''')


if __name__ == '__main__':
    init_slidex_db()
    routing.app.run(debug=True, host='0.0.0.0')