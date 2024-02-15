from flask import Flask, render_template, redirect, request
from datetime import datetime
import glob, os
import lib.photo, lib.db

app = Flask(__name__)

# top page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/photo_page')
def photo_page():
    image_urls = [d.get('file_path') for d in lib.db.get_all_photos()]
    st_birthtime = os.stat(image_urls[0]).st_ctime      # remove later
    birth_time = datetime.fromtimestamp(st_birthtime)   # remove later
    return render_template('photo_page.html', image_urls=image_urls, time=birth_time)


@app.route('/upload_page')
def upload_page():
    return render_template('upload_page.html')

@app.route('/upload', methods=['POST'])
def upload_try():
    upfile = request.files['upfile']
    if upfile.filename == '': return 'アップロード失敗：ファイルを選択してください'

    file_path = lib.photo.save_photo(upfile)
    birth_time = datetime.fromtimestamp(os.stat(file_path).st_ctime)
    lib.db.add_photo(file_path, birth_time)

    return redirect('/')



# Automatically add version after static file
@app.context_processor
def add_staticfile():
    return dict(staticfile=staticfile_cp)
def staticfile_cp(fname):
    import os
    path = os.path.join(app.root_path, 'static', fname)
    mtime = str(int(os.stat(path).st_mtime))
    return '/static/' + fname + '?v=' + str(mtime)