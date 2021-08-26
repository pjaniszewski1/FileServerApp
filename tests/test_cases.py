import pytest
import server.file_service_no_class as FileServerNoClass
import logging
import os

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

test_folder = '../test_folder'

extension = 'txt'
test_file_1 = 'test1.txt'
test_file_2 = 'test2.txt'
test_file_3 = 'test3.txt'
test_file_4 = 'test4.txt'
test_file_5 = 'test5.txt'

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
        data = bytes(test_content)
        file_handler.write(data)

    full_test_file2 = '{}\{}'.format(test_folder, test_file_2)
    with open(full_test_file2, 'wb') as file_handler:
        data = bytes(test_content)
        file_handler.write(data)

    full_test_file3 = '{}\{}'.format(test_folder, test_file_3)
    with open(full_test_file3, 'wb') as file_handler:
        data = bytes(test_content)
        file_handler.write(data)

    full_test_file4 = '{}\{}'.format(test_folder, test_file_4)
    with open(full_test_file4, 'wb') as file_handler:
        data = bytes(test_content)
        file_handler.write(data)

    full_test_file5 = '{}\{}'.format(test_folder, test_file_5)
    with open(full_test_file5, 'wb') as file_handler:
        data = bytes(test_content)
        file_handler.write(data)


@pytest.fixture(scope='function')
def prepare_data(request):
    logger.info('Prepare test data in database')
    create_and_move_to_test_folder()
    create_test_files()


class TestSuite:
    def test_get_files(self, prepare_data):
        logger.info('Test request')
        data = FileServerNoClass.get_files()
        exists_files = list(filter(
            lambda file: file.get('name') in [test_file_1, test_file_2, test_file_3, test_file_4, test_file_5],
            data
        ))
        exists_files = list(map(lambda file: file.get('name'), exists_files))

        assert len(exists_files) == 5
        assert test_file_1 in exists_files
        assert test_file_2 in exists_files
        assert test_file_3 in exists_files
        assert test_file_4 in exists_files
        assert test_file_5 in exists_files

        logger.info('Test passed')




