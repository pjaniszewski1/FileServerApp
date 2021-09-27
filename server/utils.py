import random
import string
from builtins import range
from datetime import datetime

string_length = 8


class SingletonMeta(type):
    __instance = None

    def __call__(cls):
        if not isinstance(cls.__instance, cls):
            cls.__instance = super().__call__()

        return cls.__instance


def convert_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y.%m.%d %H:%M:%S')


def generate_string():
    letters = string.ascii_letters
    digits = string.digits

    return ''.join([random.choice(letters + digits) for i in range(string_length)])
