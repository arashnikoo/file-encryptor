# file-encryptor

Encrypt and decrypt files with a password using AES-256-CBC.

## Why?

You're about to send your tax documents to your accountant over email. You could zip them with a password — but ZipCrypto is broken and AES-256 zip support is spotty across platforms. You could use GPG, but your accountant doesn't have a GPG key and you don't want to walk them through setting one up.

This tool solves that: one command, one password, no setup. The output is a single self-contained file you can attach to an email, upload to cloud storage, or commit to a repo. The recipient just needs this script (or Docker) and the password to decrypt it. No keys, no config, no fuss.

## Setup

```bash
./encrypt.sh myfile.txt -o myfile.txt.enc
```

The wrapper script auto-creates a virtualenv and installs dependencies on first run.

## Usage

```bash
# Encrypt
./encrypt.sh myfile.txt -o myfile.txt.enc

# Decrypt
./encrypt.sh -d myfile.txt.enc -o myfile.txt
```

You can also use the Python script directly after installing dependencies:

```bash
pip install -r requirements.txt
python src/encrypt.py myfile.txt -o myfile.txt.enc
python src/encrypt.py -d myfile.txt.enc -o myfile.txt
```

## Docker

```bash
# Build
docker build -t file-encryptor .

# Encrypt
docker run --rm -v "$PWD:/data" file-encryptor /data/myfile.txt -o /data/myfile.txt.enc

# Decrypt
docker run --rm -v "$PWD:/data" file-encryptor -d /data/myfile.txt.enc -o /data/myfile.txt
```

## Tests

```bash
pip install -r requirements.txt
python -m pytest tests/ -v
```
