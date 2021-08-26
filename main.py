import argparse
import os
import sys
import json

import server.file_service_no_class as FileServiceNoClass


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--folder',
        default=os.getcwd(),
        help='Working directory (absolute or relative path, default: current app folder FileServer)'
    )
    parser.add_argument('-i', '--init', action='store_true', help='initialize database')

    return parser


def get_file_data():
    print('Input filename (without extension):')
    filename = input()

    data = FileServiceNoClass.get_file_data(filename)

    return data


def create_file():
    print('Input content:')
    content = input()

    data = FileServiceNoClass.create_file(content)

    return data


def delete_file():
    print('Input filename (without extension)')

    filename = input()

    data = FileServiceNoClass.delete_file(filename)

    return data


def change_dir():
    print('Input new working directory path:')
    new_path = input()

    FileServiceNoClass.change_dir(new_path)

    return 'Working directory is successfully changed. New path is {}'.format(new_path)


def main():
    parser = commandline_parser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.folder
    FileServiceNoClass.change_dir(path)

    print('Commands:')
    print('list - get files list')
    print('get - get file data')
    print('create - create a file')
    print('delete - delete a file')
    print('chdir - change working directory')
    print('exit - exit from app')

    while True:
        try:
            print('Input command:')
            command = input()

            if command == 'list':
                data = FileServiceNoClass.get_files()

            elif command == 'get':
                data = get_file_data()

            elif command == 'create':
                data = create_file()

            elif command == 'delete':
                data = delete_file()

            elif command == 'chdir':
                data = change_dir()

            elif command == 'exit':
                return

            else:
                raise ValueError('Invalid command')

            print('\n{}\n'.format({
                'status': 'success',
                'result': json.dumps(data)
            }))
        except (ValueError, AssertionError) as err:
            print('\n{}\n'.format({
                'status': 'error',
                'message': err.message if sys.version_info[0] < 3 else err
            }))


if __name__ == '__main__':
    main()
