# file-encryptor

Encrypt and decrypt files with a password using AES-256-CBC.

## Why?

I built this primarily for my personal backup workflow: encrypt files before syncing them to cloud storage, so a compromised account doesn't expose everything. But the use cases go well beyond that, sharing secrets with teammates, committing encrypted configs to a repo, securing database dumps, encrypting files before sending them over insecure channels, and more.

The common thread is simple: take a file, lock it with a password, and get a single opaque blob that's safe to store or transmit anywhere. No keyrings, no PKI, no recipient setup. Just a password.

The output is a self-contained encrypted file, salt, IV, and ciphertext in one binary blob. The recipient only needs this script (or Docker) and the password. No keys, no config, no fuss.

## Setup

```bash
./encrypt.sh -i myfile.txt -o myfile.txt.enc
```

The wrapper script auto-creates a virtualenv and installs dependencies on first run.

## Usage

```
usage: main.py [-h] -i INPUT -o OUTPUT [-d] [-p PASSWORD]

Encrypt or decrypt a file with a password

options:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Path to the input file
  -o OUTPUT, --output OUTPUT
                        Path to the output file
  -d, --decrypt         Decrypt the file
  -p PASSWORD, --password PASSWORD
                        Password (if not provided, will prompt)
```

### Examples

```bash
# Encrypt (prompts for password)
./encrypt.sh -i myfile.txt -o myfile.txt.enc

# Encrypt with password on command line
./encrypt.sh -i myfile.txt -o myfile.txt.enc -p mypassword

# Decrypt
./encrypt.sh -d -i myfile.txt.enc -o myfile.txt -p mypassword
```

You can also use the Python script directly after installing dependencies:

```bash
pip install -r requirements.txt
python -m src.main -i myfile.txt -o myfile.txt.enc -p mypassword
python -m src.main -d -i myfile.txt.enc -o myfile.txt -p mypassword
```

## Docker

```bash
# Build
docker build -t file-encryptor .

# Encrypt
docker run --rm -v "$PWD:/data" file-encryptor -i /data/myfile.txt -o /data/myfile.txt.enc

# Decrypt
docker run --rm -v "$PWD:/data" file-encryptor -d -i /data/myfile.txt.enc -o /data/myfile.txt
```

## Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```
