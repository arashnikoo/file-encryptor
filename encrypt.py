#!/usr/bin/env python3
import argparse
import os
import sys
from getpass import getpass

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

SALT_SIZE = 16
IV_SIZE = 16
KEY_SIZE = 32
PBKDF2_ITERATIONS = 600_000


def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
        backend=default_backend(),
    )
    return kdf.derive(password.encode("utf-8"))


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file with a password")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        sys.exit(f"Error: '{args.file}' is not a file")

    password = getpass("Password: ")
    if not password:
        sys.exit("Error: password cannot be empty")

    if args.decrypt:
        decrypt_file(args.file, args.output, password)
    else:
        encrypt_file(args.file, args.output, password)


if __name__ == "__main__":
    main()
