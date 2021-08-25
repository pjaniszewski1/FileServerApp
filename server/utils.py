import string
import random
from datetime import datetime

string_length = 8


def convert_date(timestamp):
    return datetime.fromtimestamp(timestamp).strftime("%Y.%m.%d %H:%M:%S")


def generate_string():
    letters = string.ascii_letters
    digits = string.digits

    return "".join(random.choice(letters + digits) for i in range(string_length))