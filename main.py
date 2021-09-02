import argparse
import os
import sys
import json

from server.file_service import FileService, FileServiceSigned


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


def get_file_data(cwd):
    # type (str) -> dict
    print('Input filename (without extension):')
    filename = input()

    print('Check sign? y/n:')
    is_signed = input()

    if is_signed == 'y':
        data = FileServiceSigned(path=cwd).get_file_data(filename)
    elif is_signed == 'n':
        data = FileService(path=cwd).get_file_data(filename)
    else:
        raise ValueError('Invalid value')

    return data


def create_file(cwd):
    # type (str) -> dict
    print('Input content:')
    content = input()

    print('Input security level (low, medium, high):')
    security_level = input()

    assert security_level in ['low', 'medium', 'high'], 'Invalid security level'

    print('Sign file? y/n:')
    is_signed = input()

    if is_signed == 'y':
        data = FileServiceSigned(path=cwd).create_file(content, security_level)
    elif is_signed == 'n':
        data = FileService(path=cwd).create_file(content, security_level)
    else:
        raise ValueError('Invalid value')

    return data


def delete_file(cwd):
    # type (str) -> dict
    print('Input filename (without extension)')

    filename = input()

    data = FileService(path=cwd).delete_file(filename)

    return data


def change_dir(cwd):
    print('Input new working directory path:')
    new_path = input()

    FileService(path=cwd).change_dir(new_path)

    return 'Working directory is successfully changed. New path is {}'.format(new_path)


def main():
    parser = commandline_parser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.folder

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
                data = FileService(path=path).get_files()

            elif command == 'get':
                data = get_file_data(path)

            elif command == 'create':
                data = create_file(path)

            elif command == 'delete':
                data = delete_file(path)

            elif command == 'chdir':
                data = change_dir(path)

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
