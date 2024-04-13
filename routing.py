from flask import Flask, render_template, redirect, request
import glob, os
import lib.photo, lib.db, lib.memo

app = Flask(__name__)

# top page
@app.route('/')
def index():
    return render_template('index.html', albums=lib.db.get_all_albums())


@app.route('/photo_page/<album_id>')
def photo_page(album_id):
    image_urls = [d.get('file_path') for d in lib.db.get_photos_from_album(album_id)]
    music_urls = [d.replace("./static/", "/static/") for d in glob.glob("./static/music/*.mp3")]
    return render_template('photo_page.html', image_urls=image_urls, music_urls=music_urls, album=lib.db.get_album_info(album_id))


@app.route('/upload_page')
def upload_page():
    return render_template('upload_page.html')

@app.route('/upload', methods=['POST'])
def upload_try():
    upfile = request.files['upfile']
    if upfile.filename == '': return 'アップロード失敗：ファイルを選択してください'

    image_url = lib.photo.save_photo(upfile)
    lib.db.add_photo(image_url)

    return redirect('/')


@app.route('/update')
def update_try():
    lib.db.clear_db()
    lib.db.init_db()

    lib.photo.bmp2jpg(glob.glob("./static/images/*.bmp"))
    lib.photo.bmp2jpg(glob.glob("./static/images/*.BMP"))

    image_urls = glob.glob("./static/images/*.jpg")
    image_urls += glob.glob("./static/images/*.JPG")
    image_urls += glob.glob("./static/images/*.jpeg")
    for image_url in image_urls:
        lib.db.add_photo(image_url)

    return redirect('/')

@app.route('/take_notes_page/<album_id>')
def take_notes_page(album_id):
    return render_template('take_notes_page.html', album=lib.db.get_album_info(album_id))


@app.route('/take_notes/<album_id>', methods=['POST'])
def take_notes(album_id):
    contents = request.form.get('contents', "")
    lib.memo.update_memo(lib.db.get_album_info(album_id)['memo_path'], contents)
    print("take_notes!!!")
    return redirect(f'/photo_page/{album_id}')


@app.template_filter('readfile')
def readfile_filter(path):
    return lib.memo.read_file(path)

@app.template_filter('removedot')
def removedot_filter(path):
    return path.removeprefix('.')


# Automatically add version after static file
@app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)
def staticfile_cp(fname):
    import os
    path = os.path.join(app.root_path, 'static', fname)
    mtime = str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)