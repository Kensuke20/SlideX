import lib.sqlite_op
import routing

def init_slidex_db():
    lib.sqlite_op.exec_db('''
            /* photo info */
            CREATE TABLE IF NOT EXISTS photos (
            photo_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path       TEXT,
            created_year    INTEGER,
            created_month   INTEGER,
            created_day     INTEGER
            )
            ''')

    lib.sqlite_op.exec_db('''
            /* album info */
            CREATE TABLE IF NOT EXISTS albums (
            album_id      INTEGER PRIMARY KEY AUTOINCREMENT,
            album_name    TEXT
            )
            ''')

    lib.sqlite_op.exec_db('''
            /* mapping info */
            CREATE TABLE IF NOT EXISTS album_photo_map (
            album_id        INTEGER,
            photo_id        INTEGER,
            PRIMARY KEY(photo_id, album_id)
            )
            ''')


if __name__ == '__main__':
    init_slidex_db()
    routing.app.run(debug=True, host='0.0.0.0')