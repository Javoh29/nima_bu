import base64
import uuid
import hashlib
import logging
from typing import List
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util import Counter


class Obfuscator:
    def __init__(self):
        self.salt = b"b723375b3aac60afa239c149"  # Converted to bytes

    def reveal(self, obfuscated: List[int]) -> str:
        salt = self.salt
        n = len(salt)
        result_bytes = bytes([obfuscated[i] ^ salt[i % n] for i in range(len(obfuscated))])
        return result_bytes.decode('utf-8')


class Cryptographer:
    def __init__(self, array_key: List[int] = [
            84, 7, 81, 11, 3, 86, 84, 91, 82, 0, 85, 86, 83, 3, 83, 94,
            4, 10, 2, 15, 6, 3, 81, 90, 7, 5, 7, 4, 1, 82, 5, 87, 4, 85,
            89, 80, 82, 0, 89, 7, 85, 87, 5, 12, 87, 6, 82, 9, 90, 2,
            84, 85, 2, 86, 84, 1, 1, 84, 83, 83, 84, 7, 82, 94
        ]
    ):
        self.array_key = array_key
        self.obfuscator = Obfuscator()

    def encode(self, plaintext: str) -> str | None:
        try:
            original_bytes = plaintext.encode('utf-8')
            revealed_key = self.obfuscator.reveal(self.array_key)
            key_hash_hex = hashlib.sha256(revealed_key.encode('utf-8')).hexdigest()

            i = None

            def encrypt_once(data: bytes) -> str:
                iv = get_random_bytes(16)
                ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
                cipher = AES.new(bytes.fromhex(key_hash_hex), AES.MODE_CTR, counter=ctr)
                ciphertext = cipher.encrypt(data)
                return base64.b64encode(iv + ciphertext).decode('utf-8')

            for _ in range(3):
                data = i.encode('utf-8') if i else original_bytes
                i = encrypt_once(data)

            return i
        except Exception as e:
            logging.error("Ошибка при шифровании: %s", e)
            return None

    def decode(self, encoded: str) -> str | None:
        try:
            revealed_key = self.obfuscator.reveal(self.array_key)
            key_hash_hex = hashlib.sha256(revealed_key.encode('utf-8')).hexdigest()
            n = encoded

            def decrypt_once(enc_str: str) -> str:
                raw = base64.b64decode(enc_str)
                iv = raw[:16]
                ciphertext = raw[16:]
                ctr = Counter.new(128, initial_value=int.from_bytes(iv, byteorder='big'))
                cipher = AES.new(bytes.fromhex(key_hash_hex), AES.MODE_CTR, counter=ctr)
                return cipher.decrypt(ciphertext).decode('utf-8')

            for _ in range(3):
                n = decrypt_once(n)

            return n
        except Exception as e:
            logging.error("Ошибка при расшифровании: %s", e)
            return None

    def generate_encrypted_headers(self) -> dict:
        raw_uuid = str(uuid.uuid4())
        return {
            "uuid": raw_uuid,
            "encodedUuid": self.encode(f"RequestUUID:{raw_uuid}")
        }

if __name__ == "__main__":
    secret_key_array = [
        84, 7, 81, 11, 3, 86, 84, 91, 82, 0, 85, 86, 83, 3, 83, 94,
        4, 10, 2, 15, 6, 3, 81, 90, 7, 5, 7, 4, 1, 82, 5, 87, 4, 85,
        89, 80, 82, 0, 89, 7, 85, 87, 5, 12, 87, 6, 82, 9, 90, 2,
        84, 85, 2, 86, 84, 1, 1, 84, 83, 83, 84, 7, 82, 94
    ]

    crypt = Cryptographer(secret_key_array)
    print(crypt.generate_encrypted_headers())
