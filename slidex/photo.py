from datetime import datetime

def save_photo(new_file):
    fname = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    file_path = './static/images/' + fname

    new_file.save(file_path)

    return file_path