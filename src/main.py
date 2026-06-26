#!/usr/bin/env python3
import argparse
import os
import sys
from getpass import getpass

from .encrypt import encrypt_file
from .decrypt import decrypt_file


def main() -> None:
    parser = argparse.ArgumentParser(description="Encrypt or decrypt a file with a password")
    parser.add_argument("file", help="Path to the input file")
    parser.add_argument("-o", "--output", required=True, help="Path to the output file")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Decrypt the file")
    parser.add_argument("-p", "--password", help="Password (if not provided, will prompt)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        sys.exit(f"Error: '{args.file}' is not a file")

    if args.password:
        password = args.password
    else:
        password = getpass("Password: ")

    if not password:
        sys.exit("Error: password cannot be empty")

    if args.decrypt:
        decrypt_file(args.file, args.output, password)
    else:
        encrypt_file(args.file, args.output, password)


if __name__ == "__main__":
    main()
