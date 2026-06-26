import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from .crypto import derive_key, SALT_SIZE, IV_SIZE


def decrypt_file(filepath: str, outpath: str, password: str) -> None:
    with open(filepath, "rb") as f:
        data = f.read()

    salt = data[:SALT_SIZE]
    iv = data[SALT_SIZE:SALT_SIZE + IV_SIZE]
    ciphertext = data[SALT_SIZE + IV_SIZE:]

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    pad_len = plaintext[-1]
    if pad_len < 1 or pad_len > 16:
        sys.exit("Error: wrong password or corrupted file")
    plaintext = plaintext[:-pad_len]

    with open(outpath, "wb") as f:
        f.write(plaintext)

    print(f"Decrypted: {filepath} -> {outpath}")
