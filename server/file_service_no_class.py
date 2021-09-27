from __future__ import print_function

import os
import sys
from builtins import bytes

import server.utils as utils

extension = 'txt'


def change_dir(path):
    assert os.path.exists(path), 'Directory {} is not found'.format(path)
    os.chdir(path)


def get_files():
    path = os.getcwd()
    data = []

    files = [f for f in os.listdir(path) if os.path.isfile('{}/{}'.format(path, f))]
    files = [f for f in files if len(f.split('.')) > 1 and f.split('.')[1] == extension]

    for f in files:
        full_filename = '{}/{}'.format(path, f)
        data.append({
            'name': f,
            'create_date': utils.convert_date(os.path.getctime(full_filename)),
            'edit_date': utils.convert_date(os.path.getmtime(full_filename)),
            'size': '{} bytes'.format(os.path.getsize(full_filename))
        })

    return data


def get_file_data(filename):
    path = os.getcwd()
    short_filename = '{}.{}'.format(filename, extension)
    full_filename = '{}/{}'.format(path, short_filename)

    assert os.path.exists(full_filename), 'File {} does not exist'.format(short_filename)

    with open(full_filename, 'rb') as file_handler:
        return {
            'name': short_filename,
            'create_date': utils.convert_date(os.path.getctime(full_filename)),
            'edit_date': utils.convert_date(os.path.getmtime(full_filename)),
            'size': os.path.getsize(full_filename),
            'content': file_handler.read()
        }


def create_file(content=''):
    path = os.getcwd()
    filename = '{}.{}'.format(utils.generate_string(), extension)
    full_filename = '{}/{}'.format(path, filename)
    print(filename)

    while os.path.exists(full_filename):
        filename = '{}.{}'.format(utils.generate_string(), extension)
        full_filename = '{}/{}'.format(path, filename)
        print(filename)

    with open(full_filename, 'wb') as file_handler:
        if content:
            if sys.version_info[0] < 3:
                data = bytes(content)
            else:
                data = bytes(content, 'utf-8')

            file_handler.write(data)

    return {
        'name': filename,
        'create_date': utils.convert_date(os.path.getctime(full_filename)),
        'size': os.path.getsize(full_filename),
        'content': content
    }


def delete_file(filename):
    path = os.getcwd()
    short_filename = '{}.{}'.format(filename, extension)
    full_filename = '{}/{}'.format(path, short_filename)

    assert os.path.exists(full_filename), 'File {} does not exist'.format(short_filename)

    os.remove(full_filename)

    return short_filename
