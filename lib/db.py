import os
from datetime import datetime
import lib.sqlite_op
import lib.memo

def init_db():
    lib.sqlite_op.exec_db('''
            /* photo info */
            CREATE TABLE IF NOT EXISTS photos (
            photo_id        INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path       TEXT,
            st_mtime        INTEGER,
            created_year    INTEGER,
            created_month   INTEGER,
            created_day     INTEGER
            )
            ''')

    lib.sqlite_op.exec_db('''
            /* album info */
            CREATE TABLE IF NOT EXISTS albums (
            album_id      INTEGER PRIMARY KEY,
            title         TEXT,
            memo_path     TEXT,
            num_of_photo  INTEGER
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

def clear_db():
    db_filename = './db/slidex.sqlite3'
    if os.path.isfile(db_filename):
        os.remove(db_filename)


def add_photo(file_path):
    birth_time = datetime.fromtimestamp(os.stat(file_path).st_mtime)

    photo_id = lib.sqlite_op.exec_db('''
        INSERT INTO photos (file_path, st_mtime, created_year, created_month, created_day)
        VALUES (?, ?, ?, ?, ?)''',
        file_path, os.stat(file_path).st_mtime, birth_time.year, birth_time.month, birth_time.day
    )

    album_id = 0
    records = lib.sqlite_op.select_db('SELECT * FROM albums WHERE album_id=?', album_id)
    if records == []:
        create_album(album_id, '全期間の写真')
    register_album(album_id, [photo_id])

    album_id = birth_time.year
    records = lib.sqlite_op.select_db('SELECT * FROM albums WHERE album_id=?', album_id)
    if records == []:
        create_album(album_id, f'{birth_time.year}年の写真')
    register_album(album_id, [photo_id])

    return photo_id


def remove_photo(photo_id):
    lib.sqlite_op.exec_db('DELETE FROM photos WHERE photo_id=?', photo_id)


# アルバム情報を取得
def get_album_info(album_id):
    return lib.sqlite_op.select_db('SELECT * FROM albums WHERE album_id=?', album_id)[0]



def create_album(album_id, title):
    memo_path = lib.memo.save_memo(album_id, "")
    album_id = lib.sqlite_op.exec_db('''
        INSERT INTO albums (album_id, title, memo_path, num_of_photo)
        VALUES (?,?,?,?)''',
        album_id, title, memo_path, 0,
    )



def remove_album(album_id):
    lib.sqlite_op.exec_db('DELETE FROM albums WHERE album_id=?', album_id)



# Register photos in an album
def register_album(album_id, photo_ids):
    for photo_id in photo_ids:
        lib.sqlite_op.exec_db('''
                INSERT INTO album_photo_map (album_id, photo_id)
                VALUES (?,?)''',
                album_id, photo_id
        )
    num_of_photo = get_album_info(album_id)['num_of_photo'] + len(photo_ids)
    lib.sqlite_op.exec_db('UPDATE albums set num_of_photo=? WHERE album_id=?', num_of_photo, album_id)


# すべてのアルバムを取得
def get_all_albums():
    return lib.sqlite_op.select_db('SELECT * FROM albums ORDER BY album_id ASC')




# アルバムに登録されている写真を取得
def get_photos_from_album(album_id):
    records = lib.sqlite_op.select_db('SELECT photo_id FROM album_photo_map WHERE album_id=?', album_id)
    photos = []
    for record in records:
        photos.append(lib.sqlite_op.select_db('SELECT * FROM photos WHERE photo_id=?', record['photo_id'])[0])
        photos.sort(key=lambda x: x['st_mtime'])

    return photos