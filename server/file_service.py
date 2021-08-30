import os
import utils
import sys

from crypto import HashAPI


class FileService(object):
    """
    Singleton Class
    """
    __is_inited = False
    __instance = None
    extension = "txt"

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(FileService, cls).__new__(cls)
        return cls.__instance

    def __init__(self, *args, **kwargs):
        if not self.__is_inited:
            path = kwargs.get("path")

            if path:
                if not os.path.exists(path):
                    os.mkdir(path)

    @property
    def path(self):
        # type () -> str
        return self.__path

    @path.setter
    def path(self, value):
        # type (str) -> None
        if not os.path.exists(value):
            os.mkdir(value)

        self.__path = value

    @staticmethod
    # type (str) -> None
    def change_dir(path):
        assert os.path.exists(path), "Directory {} is not found".format(path)
        os.chdir(path)

    def get_files(self):
        data = []

        files = [f for f in os.listdir(self.path) if os.path.isfile("{}/{}".format(self.path, f))]
        files = [f for f in files if len(f.split('.')) > 1 and f.split(".")[1] == self.extension]

        for f in files:
            full_filename = "{}/{}".format(self.path, f)
            data.append({
                "name": f,
                "create_date": utils.convert_date(os.path.getctime(full_filename)),
                "edit_date": utils.convert_date(os.path.getmtime(full_filename)),
                "size": "{} bytes".format(os.path.getsize(full_filename))
            })

        return data

    def get_file_data(self, filename):
        short_filename = "{}.{}".format(filename, self.extension)
        full_filename = "{}/{}".format(self.path, short_filename)

        assert os.path.exists(full_filename), "File {} does not exist".format(short_filename)

        with open(full_filename, "rb") as file_handler:
            return {
                "name": short_filename,
                "create_date": utils.convert_date(os.path.getctime(full_filename)),
                "edit_date": utils.convert_date(os.path.getmtime(full_filename)),
                "size": os.path.getsize(full_filename),
                "content": file_handler.read()
            }

    def create_file(self, content=''):
        filename = "{}.{}".format(utils.generate_string(), self.extension)
        full_filename = "{}/{}".format(self.path, filename)
        print(filename)

        while os.path.exists(full_filename):
            filename = "{}.{}".format(utils.generate_string(), self.extension)
            full_filename = "{}/{}".format(self.path, filename)
            print(filename)

        with open(full_filename, "wb") as file_handler:
            if content:
                if sys.version_info[0] < 3:
                    data = bytes(content)
                else:
                    data = bytes(content, "utf-8")

                file_handler.write(data)

        return {
            "name": filename,
            "create_date": utils.convert_date(os.path.getctime(full_filename)),
            "size": os.path.getsize(full_filename),
            "content": content
        }

    def delete_file(self, filename):
        short_filename = "{}.{}".format(filename, self.extension)
        full_filename = "{}/{}".format(self.path, short_filename)

        assert os.path.exists(full_filename), "File {} does not exist".format(short_filename)

        os.remove(full_filename)

        return short_filename


class FileServiceSigned(FileService):
    """
    Singleton Child Class
    """
    def get_file_data(self, filename):
        # type (str) -> dict

        result = super(FileServiceSigned, self).get_file_data(filename)
        result_for_check = result
        result_for_check.pop("edit_date")

        short_filename = "{}.{}".format(filename, "md5")
        full_filename = "{}/{}".format(self.path, short_filename)
        assert os.path.exists(full_filename), "Signature file {} does not exist".format(short_filename)

        signature = HashAPI.hash_md5("_".join(list(str(x) for x in list(result_for_check.values()))))
        with open(full_filename, "rb") as file_handler:
            assert file_handler.read() == bytes(signature), "The signatures are different"

        return result

    def create_file(self, content=''):
        # type (str) -> dict

        result = super(FileServiceSigned, self).create_file(content)
        signature = HashAPI.hash_md5("_".join(list(str(x) for x in list(result.values()))))
        filename = "{}.{}".format(result["name"].split(".")[0], "md5")
        full_filename = "{}/{}".format(self.path, filename)

        with open(full_filename, "rb") as file_handler:
            data = bytes(signature)
            file_handler.write(data)

        return result
