from __future__ import print_function
from __future__ import absolute_import
from builtins import bytes
from builtins import str
from builtins import object
import os
from collections import OrderedDict
from typing import Dict

from . import utils

from server.crypto import HashAPI, BaseCipher, AESCipher, RSACipher


class FileService(object):
    __is_inited = False
    __instance = None
    extension = 'txt'

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super(FileService, cls).__new__(cls)

        return cls.__instance

    def __init__(self, *args, **kwargs):
        if not self.__is_inited:
            path = kwargs.get('path')

            if path:
                if not os.path.exists(path):
                    os.mkdir(path)

                self.__path = path

            self.__is_inited = True

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
    def change_dir(path):
        # type (str) -> None
        assert os.path.exists(path), 'Directory {} is not found'.format(path)
        os.chdir(path)

    def get_files(self):
        # type () -> list
        data = []

        files = [f for f in os.listdir(self.path) if os.path.isfile('{}/{}'.format(self.path, f))]
        files = [f for f in files if len(f.split('.')) > 1 and f.split('.')[1] == self.extension]

        for f in files:
            full_filename = '{}/{}'.format(self.path, f)
            data.append({
                'name': f,
                'create_date': utils.convert_date(os.path.getctime(full_filename)),
                'edit_date': utils.convert_date(os.path.getmtime(full_filename)),
                'size': '{} bytes'.format(os.path.getsize(full_filename))
            })

        return data

    def get_file_data(self, filename):
        # type (str) -> dict
        short_filename = '{}.{}'.format(filename, self.extension)
        full_filename = '{}/{}'.format(self.path, short_filename)

        assert os.path.exists(full_filename), 'File {} does not exist'.format(short_filename)

        filename_parts = filename.split('_')
        assert len(filename_parts) == 2, 'Invalid format of file name'
        security_level = filename_parts[1]

        if not security_level or security_level == 'low':
            cipher = BaseCipher()
        elif security_level == 'medium':
            cipher = AESCipher(self.path)
        elif security_level == 'high':
            cipher = RSACipher(self.path)
        else:
            raise ValueError('Security level is invalid')

        with open(full_filename, 'rb') as file_handler:
            return OrderedDict(
                name=short_filename,
                create_date=utils.convert_date(os.path.getctime(full_filename)),
                edit_date=utils.convert_date(os.path.getmtime(full_filename)),
                size=os.path.getsize(full_filename),
                content=cipher.decrypt(file_handler, filename).decode('utf-8')
            )

    async def get_file_data_async(self, filename: str) -> Dict[str, str]:
        short_filename = '{}.{}'.format(filename, self.extension)
        full_filename = '{}/{}'.format(self.path, short_filename)

        assert os.path.exists(full_filename), 'File {} does not exist'.format(short_filename)

        filename_parts = filename.split('_')
        assert len(filename_parts) == 2, 'Invalid format of file name'
        security_level = filename_parts[1]

        if not security_level or security_level == 'low':
            cipher = BaseCipher()
        elif security_level == 'medium':
            cipher = AESCipher(self.path)
        elif security_level == 'high':
            cipher = RSACipher(self.path)
        else:
            raise ValueError('Security level is invalid')

        with open(full_filename, 'rb') as file_handler:
            return OrderedDict(
                name=short_filename,
                create_date=utils.convert_date(os.path.getctime(full_filename)),
                edit_date=utils.convert_date(os.path.getmtime(full_filename)),
                size=os.path.getsize(full_filename),
                content=cipher.decrypt(file_handler, filename).decode('utf-8')
            )

    async def create_file(self, content=None, security_level=None):
        # type (str, str) -> dict
        filename = '{}_{}.{}'.format(utils.generate_string(), security_level, self.extension)
        full_filename = '{}/{}'.format(self.path, filename)
        print(filename)

        while os.path.exists(full_filename):
            filename = '{}_{}.{}'.format(utils.generate_string(), security_level, self.extension)
            full_filename = '{}/{}'.format(self.path, filename)
            print(filename)

        if not security_level or security_level == 'low':
            cipher = BaseCipher()
        elif security_level == 'medium':
            cipher = AESCipher(self.path)
        elif security_level == 'high':
            cipher = RSACipher(self.path)
        else:
            raise ValueError('Security level is invalid')

        with open(full_filename, 'wb') as file_handler:
            if content:
                data = bytes(content, 'utf-8')
                cipher.write_cipher_text(data, file_handler, filename.split('.')[0])

        return OrderedDict(
            name=filename,
            create_date=utils.convert_date(os.path.getctime(full_filename)),
            size=os.path.getsize(full_filename),
            content=content)

    def delete_file(self, filename):
        # type (str) -> str
        short_filename = '{}.{}'.format(filename, self.extension)
        signature_file = '{}.{}'.format(filename, 'md5')
        full_filename = '{}/{}'.format(self.path, short_filename)
        full_signature_file = '{}/{}'.format(self.path, signature_file)

        assert os.path.exists(full_filename), 'File {} does not exist'.format(short_filename)

        os.remove(full_filename)

        if os.path.exists(full_signature_file):
            os.remove(full_signature_file)

        return short_filename


class FileServiceSigned(FileService):
    def get_file_data(self, filename):
        # type (str) -> dict

        result = super(FileServiceSigned, self).get_file_data(filename)
        result_for_check = result
        result_for_check.pop('edit_date')

        short_filename = '{}.{}'.format(filename, 'md5')
        full_filename = '{}/{}'.format(self.path, short_filename)
        assert os.path.exists(full_filename), 'Signature file {} does not exist'.format(short_filename)

        signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(result_for_check.values()))))

        with open(full_filename, 'rb') as file_handler:
            assert file_handler.read() == bytes(signature, 'utf-8'), 'The signatures are different'

        return result

    async def get_file_data_async(self, filename: str) -> Dict[str, str]:
        # type (str) -> dict

        result = await super(FileServiceSigned, self).get_file_data_async(filename)
        result_for_check = result
        result_for_check.pop('edit_date')

        short_filename = '{}.{}'.format(filename, 'md5')
        full_filename = '{}/{}'.format(self.path, short_filename)
        assert os.path.exists(full_filename), 'Signature file {} does not exist'.format(short_filename)

        signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(result_for_check.values()))))

        with open(full_filename, 'rb') as file_handler:
            assert file_handler.read() == bytes(signature, 'utf-8'), 'The signatures are different'

        return result

    async def create_file(self, content=None, security_level=None):
        # type (str, str) -> dict
        result = await super(FileServiceSigned, self).create_file(content, security_level)
        signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(result.values()))))
        filename = '{}.{}'.format(result['name'].split('.')[0], 'md5')
        full_filename = '{}/{}'.format(self.path, filename)

        with open(full_filename, 'wb') as file_handler:
            data = bytes(signature, 'utf-8')
            file_handler.write(data)

        return result
