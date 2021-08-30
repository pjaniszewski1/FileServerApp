import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes

key_folder = os.environ["KEY_DIR"]


class HashAPI(object):
    @staticmethod
    def hash_sha512(input_str):
        # type (ste) -> str

        assert input_str, "Hash: input string is not set"
        hash_obj = hashlib.sha512(input_str.encode())

        return hash_obj.hexdigest()

    @staticmethod
    def hash_md5(input_str):
        # type (str) -> str

        assert input_str, "Hash: input string is not set"
        hash_obj = hashlib.md5(input_str.encode())

        return hash_obj.hexdigest()


class BaseCipher(object):

    def __init__(self):
        if not os.path.exists(key_folder):
            os.mkdir(key_folder)

    def encrypt(self, data):
        # type (bytes) -> typle
        pass

    def decrypt(self, input_file, filename):
        # type (BinaryIO, str) -> bytes

        return input_file.read()

    def write_cipher_text(self, data, out_file, filename):
        # type (bytes, BinaryIO, str) -> None

        out_file.write(data)


class AESCipher(BaseCipher):

    def __init__(self, file_folder):
        # type (str) -> None
        super(BaseCipher, self).__init__()
        self.file_folder = file_folder

    def encrypt(self, data):
        # type (bytes) -> tuple

        session_key = get_random_bytes(16)
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        cipher_text, tag = cipher_aes.encrypt_and_digest(data)

        return cipher_text, tag, cipher_aes.nonce, session_key

    def decrypt(self, input_file, filename):
        # type (BinaryIO, str) -> bytes

        nonce, tag, cipher_text = [input_file.read(x) for x in (16, 16, -1)]
        session_key_file = "{}/{}.bin".format(self.file_folder, filename)
        session_key = open(session_key_file, "rb").read()

        return self.decrypt_aes_data(cipher_text, tag, nonce, session_key)

    @staticmethod
    def decrypt_aes_data(cipher_text, tag, nonce, session_key):
        # type (bytes, bytes, bytes, bytes) -> bytes

        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(cipher_text, tag)

        return data

    def write_cipher_text(self, data, out_file, filename):
        # type (bytes, BinaryIO, str) -> None

        cipher_text, tag, nonce, session_key = self.encrypt(data)
        session_key_file = "{}/{}.bin".format(self.file_folder, filename)

        if not os.path.exists(session_key_file):
            with open(session_key, "wb") as f:
                f.write(session_key)

        out_file.write(nonce)
        out_file.write(tag)
        out_file.write(cipher_text)
