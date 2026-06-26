import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from encrypt import encrypt_file, decrypt_file, SALT_SIZE, IV_SIZE


def test_encrypt_decrypt_roundtrip():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"Hello, World!")
        plain_path = f.name

    enc_path = plain_path + ".enc"
    dec_path = plain_path + ".dec"

    try:
        encrypt_file(plain_path, enc_path, "mypassword")
        assert os.path.isfile(enc_path)

        with open(enc_path, "rb") as f:
            data = f.read()
        assert len(data) > SALT_SIZE + IV_SIZE

        decrypt_file(enc_path, dec_path, "mypassword")
        assert os.path.isfile(dec_path)

        with open(dec_path, "rb") as f:
            decrypted = f.read()
        assert decrypted == b"Hello, World!"
    finally:
        for p in (plain_path, enc_path, dec_path):
            if os.path.isfile(p):
                os.unlink(p)


def test_wrong_password_fails():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"secret data")
        plain_path = f.name

    enc_path = plain_path + ".enc"
    dec_path = plain_path + ".dec"

    try:
        encrypt_file(plain_path, enc_path, "correct")
        with pytest.raises(SystemExit):
            decrypt_file(enc_path, dec_path, "wrong")
    finally:
        for p in (plain_path, enc_path, dec_path):
            if os.path.isfile(p):
                os.unlink(p)


def test_empty_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        plain_path = f.name

    enc_path = plain_path + ".enc"
    dec_path = plain_path + ".dec"

    try:
        encrypt_file(plain_path, enc_path, "password")
        decrypt_file(enc_path, dec_path, "password")

        with open(dec_path, "rb") as f:
            decrypted = f.read()
        assert decrypted == b""
    finally:
        for p in (plain_path, enc_path, dec_path):
            if os.path.isfile(p):
                os.unlink(p)


def test_binary_data():
    data = bytes(range(256)) * 10
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(data)
        plain_path = f.name

    enc_path = plain_path + ".enc"
    dec_path = plain_path + ".dec"

    try:
        encrypt_file(plain_path, enc_path, "password")
        decrypt_file(enc_path, dec_path, "password")

        with open(dec_path, "rb") as f:
            decrypted = f.read()
        assert decrypted == data
    finally:
        for p in (plain_path, enc_path, dec_path):
            if os.path.isfile(p):
                os.unlink(p)


def test_encrypted_files_differ():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"same data")
        plain_path = f.name

    enc1 = plain_path + ".enc1"
    enc2 = plain_path + ".enc2"

    try:
        encrypt_file(plain_path, enc1, "password")
        encrypt_file(plain_path, enc2, "password")

        with open(enc1, "rb") as f:
            d1 = f.read()
        with open(enc2, "rb") as f:
            d2 = f.read()
        assert d1 != d2
    finally:
        for p in (plain_path, enc1, enc2):
            if os.path.isfile(p):
                os.unlink(p)
