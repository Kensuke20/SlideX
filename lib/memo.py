import os

def save_memo(file_name, contents):
    path = f'./static/memo/{file_name}.txt'
    try:
        with open(path, mode='x') as f:
            f.write(contents)
    except FileExistsError:
        print('ONO Error: ' + path + 'is already exists. by ONO in memo.py.')

    return path


def update_memo(path, contents):
    if not os.path.isfile(path):
        print('ONO Error: ' + path + ' does not exist. by ONO')
        print('in memo.py. [2]')
    else:
        with open(path, mode='w') as f:
            f.write(contents)


def read_file(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        print('ONO Error: ' + path + ' does not exist. by ONO')
        print('in memo.py. [3]')