import argparse
import os
import sys

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


def main():
    parser = commandline_parser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.folder
    FileServiceNoClass.change_dir(path)


if __name__ == '__main__':
    main()
