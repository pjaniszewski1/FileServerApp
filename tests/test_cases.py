from builtins import bytes
from builtins import str
from builtins import object
from collections import OrderedDict

import pytest
from aiohttp import web

import server.file_service_no_class as FileServerNoClass
import logging
import os
import json
import server.utils as utils

from server.crypto import HashAPI, AESCipher, RSACipher
from server.file_service import FileService, FileServiceSigned
from server.handler import Handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

test_folder = '../test_folder'

extension = 'txt'
test_file_1 = 'test1_low.txt'
test_file_2 = 'test2_test.txt'
test_file_3 = 'test3.txt'
test_file_4 = 'test4_low.txt'
test_signature_file_4 = 'test4_low.md5'
test_file_5 = 'test5_low.txt'
test_signature_file_5 = 'test5_low.md5'
test_file_6 = 'test6_medium.txt'
test_signature_file_6 = 'test6_medium.md5'
test_file_7 = 'test7_high.txt'
test_signature_file_7 = 'test7_high.md5'
test_file_8 = 'test8_low.txt'

test_content = 'Test content\n'


def create_and_move_to_test_folder():
    # type () -> None
    if not os.path.exists(test_folder):
        os.mkdir(test_folder)

    os.chdir(test_folder)


def create_test_files():
    # type () -> None

    full_test_file1 = '{}\{}'.format(test_folder, test_file_1)
    with open(full_test_file1, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        file_handler.write(data)

    full_test_file2 = '{}\{}'.format(test_folder, test_file_2)
    with open(full_test_file2, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        file_handler.write(data)

    full_test_file3 = '{}\{}'.format(test_folder, test_file_3)
    with open(full_test_file3, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        file_handler.write(data)

    full_test_file4 = '{}\{}'.format(test_folder, test_file_4)
    with open(full_test_file4, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        file_handler.write(data)

    full_test_file5 = '{}\{}'.format(test_folder, test_file_5)
    with open(full_test_file5, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        file_handler.write(data)


@pytest.fixture
def client(loop, aiohttp_client):
    create_and_move_to_test_folder()
    create_test_files()

    handler = Handler(test_folder)
    app = web.Application()
    app.router.add_get('/', handler.handle)
    app.router.add_get('/files/list', handler.get_files)
    app.router.add_get('/files', handler.get_file_info)
    app.router.add_post('/files', handler.create_file)
    app.router.add_delete('file/{filename}', handler.delete_file)
    app.router.add_post('/change_file_dir', handler.change_file_dir)

    return loop.run_until_complete(aiohttp_client(app)), handler


@pytest.fixture(scope='function')
def prepare_data(request):
    logger.info('Prepare test data in database')

    full_test_file_4 = '{}\{}'.format(test_folder, test_file_4)
    file_dict_4 = OrderedDict(
        name=test_file_4,
        create_date=utils.convert_date(os.path.getctime(full_test_file_4)),
        size=os.path.getsize(full_test_file_4),
        content=test_content
    )
    full_test_signature_file_4 = '{}/{}'.format(test_folder, test_signature_file_4)
    signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(file_dict_4.values()))))
    with open(full_test_signature_file_4, 'wb') as file_handler:
        data = bytes(signature, 'utf-8')
        file_handler.write(data)

    # file5
    full_test_file_5 = '{}\{}'.format(test_folder, test_file_5)
    file_dict_5 = OrderedDict(
        name=test_file_5,
        create_date=utils.convert_date(os.path.getctime(full_test_file_5)),
        size=os.path.getsize(full_test_file_5),
        content=test_content
    )
    full_test_signature_file_5 = '{}/{}'.format(test_folder, test_signature_file_5)
    signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(file_dict_5.values()))))
    with open(full_test_signature_file_5, 'wb') as file_handler:
        data = bytes(signature, 'utf-8')
        file_handler.write(data)

    # file6
    cipher = AESCipher(test_folder)
    full_test_file_6 = '{}\{}'.format(test_folder, test_file_6)
    with open(full_test_file_6, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        cipher.write_cipher_text(data, file_handler, test_file_6.split('.')[0])

    file_dict_6 = OrderedDict(
        name=test_file_6,
        create_date=utils.convert_date(os.path.getctime(full_test_file_6)),
        size=os.path.getsize(full_test_file_6),
        content=test_content
    )
    full_test_signature_file_6 = '{}/{}'.format(test_folder, test_signature_file_6)
    signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(file_dict_6.values()))))
    with open(full_test_signature_file_6, 'wb') as file_handler:
        data = bytes(signature, 'utf-8')
        file_handler.write(data)

    #file7
    cipher = RSACipher(test_folder)
    full_test_file_7 = '{}\{}'.format(test_folder, test_file_7)
    with open(full_test_file_7, 'wb') as file_handler:
        data = bytes(test_content, 'utf-8')
        cipher.write_cipher_text(data, file_handler, test_file_7.split('.')[0])

    file_dict_7 = OrderedDict(
        name=test_file_7,
        create_date=utils.convert_date(os.path.getctime(full_test_file_7)),
        size=os.path.getsize(full_test_file_7),
        content=test_content
    )
    full_test_signature_file_7 = '{}/{}'.format(test_folder, test_signature_file_7)
    signature = HashAPI.hash_md5('_'.join(list(str(x) for x in list(file_dict_7.values()))))
    with open(full_test_signature_file_7, 'wb') as file_handler:
        data = bytes(signature, 'utf-8')
        file_handler.write(data)

    request.addfinalizer(teardown)
    yield


def teardown():
    test_key_file_6 = '{}/{}.{}'.format(test_folder, test_file_6.split('.')[0], 'bin')
    test_key_file_7 = '{}/{}.{}'.format(test_folder, test_file_7.split('.')[0], 'bin')

    if os.path.exists(test_key_file_6):
        os.remove(test_key_file_6)

    if os.path.exists(test_key_file_7):
        os.remove(test_key_file_7)


class TestSuite(object):
    async def test_connection(self, client):
        client, handler = tuple(client)

        logger.info('Test request. Method not allow')
        resp = await client.put('/')
        assert resp.status == 405
        logger.info('Test passed')

        logger.info('Test request')
        resp = await client.get('/')
        assert resp.status == 200
        result = json.loads(await resp.text())
        assert result.get('status') == 'success'
        logger.info('Test passed')

    def test_get_files(self, client, prepare_data):
        client, handler = tuple(client)

        logger.info('Test request. Method not allowed.')
        resp = await client.put('/files/list')
        assert resp.status == 405
        logger.info('Test passed')

        logger.info('Test request')
        resp = await client.get('/files/list')
        assert resp.status == 200
        result = json.loads(await resp.text())
        assert result.get('status') == 'success'
        data = result.get('data')

        exists_files = list([file for file in data if file.get('name') in [test_file_1, test_file_2, test_file_3, test_file_4, test_file_5, test_file_6, test_file_7]])
        exists_files = list([file.get('name') for file in exists_files])

        assert len(exists_files) == 7
        assert test_file_1 in exists_files
        assert test_file_2 in exists_files
        assert test_file_3 in exists_files
        assert test_file_4 in exists_files
        assert test_file_5 in exists_files
        assert test_file_6 in exists_files
        assert test_file_7 in exists_files
        assert not (test_file_8 in exists_files)

        logger.info('Test passed')

    def test_get_file_info(self, client, prepare_data):
        client, handler = tuple(client)
        test_file_part = test_file_4.split('.')[0]

        logger.info('Test request. Method not allowed')
        resp = await client.put('/files?filename?={}&is_signed={}'.format(test_file_part, 'false'))
        assert resp.status == 405
        logger.info('Test passed')

        logger.info('Test request. File exists. Security level low.')
        resp = await client.get('/files?filename={}&is_signed={}'.format(test_file_part, 'false'))
        assert resp.status == 200
        result = json.loads(await resp.text())
        assert result.get('status') == 'success'

        filename = result.get('data').get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert filename == test_file_4

        content = result.get('data').get('content')
        assert content == test_content

        logger.info('Test request. File exists. Security level medium.')
        test_file_part = test_file_6.split('.')[0]
        resp = await client.get('/files?filename={}&is_signed={}'.format(test_file_part, 'true'))
        assert resp.status == 200
        result = json.loads(await resp.text())
        assert result.get('status') == 'success'

        filename = result.get('data').get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert filename == test_file_6
        content = result.get('data').get('content')
        assert content == test_content

        logger.info('Test request. File exists. Security level high.')
        test_file_part = test_file_7.split('.')[0]
        resp = await client.get('/files?filename={}&is_signed={}'.format(test_file_part, 'true'))
        assert resp.status == 200
        result = json.loads(await resp.text())
        assert result.get('status') == 'success'

        filename = result.get('data').get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert filename == test_file_7
        content = result.get('data').get('content')
        assert content == test_content

        logger.info('Test request. File exists. Security level medium. Signatures are match')
        test_file_part = test_file_6.split('.')[0]
        data = FileServiceSigned(path=test_folder).get_file_data(test_file_part)
        filename = data.get('name')

        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert filename == test_file_6
        content = data.get('content')
        assert content == test_content

        logger.info('Test request. File exists. Security level high. Signatures are match')
        test_file_part = test_file_7.split('.')[0]
        data = FileServiceSigned(path=test_folder).get_file_data(test_file_part)
        filename = data.get('name')

        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert filename == test_file_7
        content = data.get('content')
        assert content == test_content

        logger.info('Test passed')

    def test_create_file_with_content(self, prepare_data):
        logger.info('Test request. Content is not empty. Security level is high')
        data = FileService(path=test_folder).create_file(content=test_content, security_level='high')
        filename = data.get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))

        logger.info('Test request. Content is not empty. Security level is medium')
        data = FileService(path=test_folder).create_file(content=test_content, security_level='medium')
        filename = data.get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))

        logger.info('Test request. Content is not empty. Security level is low')
        data = FileService(path=test_folder).create_file(content=test_content, security_level='low')
        filename = data.get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))

        logger.info('Test request. Content is not empty. Security level is high. File is signed.')
        data = FileServiceSigned(path=test_folder).create_file(content=test_content, security_level='high')
        filename = data.get('name')
        signature_file = '{}.{}'.format(filename.split('.')[0], 'md5')
        assert os.path.exists('{}/{}'.format(test_folder, filename))
        assert os.path.exists('{}/{}'.format(test_folder, signature_file))

        logger.info('Test passed')

    def test_create_file_without_content(self, prepare_data):
        logger.info('Test request. Content is empty')

        data = FileService(path=test_folder).create_file(security_level='high')
        filename = data.get('name')
        assert os.path.exists('{}/{}'.format(test_folder, filename))

        logger.info('Test passed')

    def test_delete_file(self, prepare_data):
        logger.info('Test request. File exists')

        test_file_path = test_file_6.split('.')[0]
        FileService(path=test_folder).delete_file(test_file_path)
        signature_file = '{}/{}'.format(test_folder, test_file_6)
        assert not os.path.exists('{}/{}'.format(test_folder, test_file_6))
        assert not os.path.exists('{}/{}'.format(test_folder, signature_file))

        logger.info('Test passed')

    def test_change_file_dir(self, prepare_data):
        new_test_folder = '../test_folder'

        file_service = FileService(path=test_folder)
        file_service_signed = FileServiceSigned(path=test_folder)
        file_service.path = new_test_folder
        file_service_signed.path = new_test_folder

        assert file_service.path == new_test_folder
        assert file_service_signed.path == new_test_folder

        logger.info('Test passed')
