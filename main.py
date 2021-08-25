import argparse
import os
import sys
import json

import server.file_service_no_class as FileServiceNoClass


def commandline_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder", default=os.getcwd(), help="Working directory")
    parser.add_argument("-i", "--init", action="store_true", help="Initialize database")

    return parser


def get_file_data():
    print("Input file without extension")
    filename = input()

    data = FileServiceNoClass.get_file_data(filename)

    return data


def create_file():
    print("Input content:")
    content = input()

    data = FileServiceNoClass.create_file(content)

    return data


def delete_file():
    print("Input file without extension:")
    content = input()

    data = FileServiceNoClass.delete_file(content)

    return data


def change_directory():
    print("Input new working directory path:")
    new_path = input()

    FileServiceNoClass.change_dir(new_path)

    return "Working directory was successfully changed to {}".format(new_path)


def main():
    parser = commandline_parser()
    namespace = parser.parse_args(sys.argv[1:])
    path = namespace.folder
    FileServiceNoClass.change_dir("sample")

    print("Commands:")
    print("List - get files list")
    print("get - read from file")
    print("delete - delete a file")
    print("create - create a file")
    print("change - change working dir")
    print("exit - exit from application")

    while True:
        try:
            print("Input command:")
            command = input()
            if command == "list":
                data = FileServiceNoClass.get_files()
            elif command == "get":
                data = get_file_data()
            elif command == "delete":
                data = delete_file()
            elif command == "create":
                data = create_file()
            elif command == "change":
                data = change_directory()
            elif command == "exit":
                return
            else:
                raise ValueError("Input command was invalid")
            print("\n{}\n".format({
                "status": "success",
                "result": json.dumps(data)
            }))
        except (ValueError, AssertionError) as error:
            print("\n{}\n".format({
                "status": "error",
                "message": error.message if sys.version_info[0] < 3 else error
            }))


if __name__ == "__main__":
    main()
