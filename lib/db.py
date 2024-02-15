import lib.sqlite_op

def init_db():
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

def add_photo(file_path, birth_time):

    photo_id = lib.sqlite_op.exec_db('''
        INSERT INTO photos (file_path, created_year, created_month, created_day)
        VALUES (?, ?, ?, ?)''',
        file_path, birth_time.year, birth_time.month, birth_time.day
    )
    return photo_id


def remove_photo(photo_id):
    lib.sqlite_op.exec_db('DELETE FROM photos WHERE photo_id=?', photo_id)


# すべての写真を取得
def get_all_photos():
    return lib.sqlite_op.select_db('SELECT * FROM photos ORDER BY photo_id DESC LIMIT 50')




def add_album(album_name):
    album_id = lib.sqlite_op.exec_db('''
        INSERT INTO albums (album_name)
        VALUES (?)''',
        album_name
    )
    return album_id

def remove_album(album_id):
    lib.sqlite_op.exec_db('DELETE FROM albums WHERE album_id=?', album_id)




# Register photos in an album
def update_album(album_id, photo_ids):
    for photo_id in photo_ids:
        lib.sqlite_op.exec_db('''
                INSERT INTO album_photo_map (album_id, photo_id)
                VALUES (?,?)''',
                album_id, photo_id
        )