import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from .crypto import derive_key, SALT_SIZE, IV_SIZE


def encrypt_file(filepath: str, outpath: str, password: str) -> None:
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = derive_key(password, salt)

    with open(filepath, "rb") as f:
        plaintext = f.read()

    pad_len = 16 - (len(plaintext) % 16)
    plaintext += bytes([pad_len]) * pad_len

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()

    with open(outpath, "wb") as f:
        f.write(salt + iv + ciphertext)

    print(f"Encrypted: {filepath} -> {outpath}")
