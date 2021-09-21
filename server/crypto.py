from __future__ import absolute_import
from builtins import object
import hashlib
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Random import get_random_bytes


key_folder = os.environ['KEY_DIR']


class HashAPI(object):
    @staticmethod
    def hash_sha512(input_str):
        # type (str) -> str

        assert input_str, 'Hash: input string is not set'
        hash_obj = hashlib.sha512(input_str.encode())

        return hash_obj.hexdigest()

    @staticmethod
    def hash_md5(input_str):
        # type (str) -> str

        assert input_str, 'Hash: input string is not set'
        hash_obj = hashlib.md5(input_str.encode())

        return hash_obj.hexdigest()


class BaseCipher(object):

    def __init__(self):
        if not os.path.exists(key_folder):
            os.mkdir(key_folder)

    def encrypt(self, data):
        # type (bytes) -> tuple
        pass

    def decrypt(self, input_file, filename):
        # type (BinaryIO, str) -> bytes

        return input_file.read()

    def write_cipher_text(self, data, out_file, filename):
        # type (bytes, BinaryIO, str) -> None

        out_file.write(data)


class AESCipher(BaseCipher):

    def __init__(self, user_id: int, file_folder: str) -> None:
        super(BaseCipher, self).__init__()
        self.user_id = user_id
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
        session_key_file = '{}/{}_{}.bin'.format(self.file_folder, self.user_id, filename)
        session_key = open(session_key_file, 'rb').read()

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
        session_key_file = '{}/{}_{}.bin'.format(self.file_folder, self.user_id, filename)

        if not os.path.exists(session_key_file):
            with open(session_key_file, 'wb') as f:
                f.write(session_key)

        out_file.write(nonce)
        out_file.write(tag)
        out_file.write(cipher_text)


class RSACipher(AESCipher):
    code = os.environ['CRYPTO_CODE']
    key_protection = 'scryptAndAES128-CBC'

    def __init__(self, user_id: int, file_folder: str) -> None:
        # type (str) -> None
        super(RSACipher, self).__init__(user_id, file_folder)
        key = RSA.generate(2048)

        encrypted_key = key.export_key(passphrase=self.code, pkcs=8, protection=self.key_protection)

        self.private_key_file = '{}/{}_private_rsa_key.bin'.format(key_folder, self.user_id)
        self.public_key_file = '{}/{}_public_rsa_key.pem'.format(key_folder, self.user_id)

        if not os.path.exists(self.private_key_file):
            with open(self.private_key_file, 'wb') as f:
                f.write(encrypted_key)

        if not os.path.exists(self.public_key_file):
            with open(self.public_key_file, 'wb') as f:
                f.write(key.publickey().exportKey())

    def encrypt(self, data):
        # type (bytes) -> tuple
        cipher_text, tag, nonce, session_key = super(RSACipher, self).encrypt(data)

        public_key = RSA.import_key(open(self.public_key_file).read())
        cipher_rsa = PKCS1_OAEP.new(public_key)
        enc_session_key = cipher_rsa.encrypt(session_key)

        return cipher_text, tag, nonce, enc_session_key

    def decrypt(self, input_file, filename):
        # type (BinaryIO, str) -> bytes

        private_key = RSA.import_key(open(self.private_key_file).read(), passphrase=self.code)
        nonce, tag, cipher_text = [input_file.read(x) for x in (16, 16, -1)]
        cipher_rsa = PKCS1_OAEP.new(private_key)
        session_key_file = '{}/{}_{}.bin'.format(self.file_folder, self.user_id, filename)

        enc_session_key = open(session_key_file, 'rb').read()
        session_key = cipher_rsa.decrypt(enc_session_key)

        return self.decrypt_aes_data(cipher_text, tag, nonce, session_key)

    def write_cipher_text(self, data, out_file, filename):
        # type (bytes, BinaryIO, str) -> None

        cipher_text, tag, nonce, session_key = self.encrypt(data)
        session_key_file = '{}/{}_{}.bin'.format(self.file_folder, self.user_id, filename)

        if not os.path.exists(session_key_file):
            with open(session_key_file, 'wb') as f:
                f.write(session_key)

        out_file.write(nonce)
        out_file.write(tag)
        out_file.write(cipher_text)
