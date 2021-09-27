from __future__ import print_function

import argparse
import logging
import os
import sys

from aiohttp import web

from server.database import DataBase
from server.handler import Handler


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', default='8080', help='port (default: 8080)')
    parser.add_argument(
        '-f',
        '--folder',
        default=os.getcwd(),
        help='Working directory (absolute or relative path, default: current app folder FileServer)'
    )
    parser.add_argument('-i', '--init', action='store_true', help='initialize database')

    return parser


def main():
    parser = commandline_parser()
    namespace = parser.parse_args(sys.argv[1:])

    db = DataBase()
    if namespace.init:
        db.init_system()

    handler = Handler(namespace.folder)
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.get('/files/list', handler.get_files),
        web.get('/files', handler.get_file_info),
        web.post('/files', handler.create_file),
        web.delete('/files/{filename}', handler.delete_file),
        web.post('/change_file_dir', handler.change_file_dir),
        web.post('/signup', handler.singup),
        web.post('/signin', handler.signin),
        web.put('/method/{method_name}', handler.add_method),
        web.delete('/method/{method_name}', handler.delete_method),
        web.put('/role/{role_name}', handler.add_role),
        web.delete('/role/{role_name}', handler.delete_role),
        web.post('/add_method_to_role', handler.add_method_to_role),
        web.post('/delete_method_from_role', handler.delete_method_from_role),
        web.post('/change_shared_prop', handler.change_shared_prop),
        web.post('/change_user_role', handler.change_user_role),
        web.get('/logout', handler.logout)
    ])
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, port=namespace.port)


if __name__ == '__main__':
    main()
