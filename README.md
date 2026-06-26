# file-encryptor

Encrypt and decrypt files with a password using AES-256-CBC.

## Why?

You need to store a production database dump in S3 for debugging, but the dump contains PII. You need to share an `.env` file with a teammate over Slack. You want to commit encrypted secrets to a public repo so your CI pipeline can decrypt them at runtime. You're backing up a server config to a USB drive that could get lost.

In all these cases you need one thing: take a file, lock it with a password, and get a single opaque blob that's safe to store or transmit anywhere. No keyrings, no PKI, no recipient setup. Just a password.

This tool does exactly that. The output is a self-contained encrypted file — salt, IV, and ciphertext in one binary blob. The recipient only needs this script (or Docker) and the password. No keys, no config, no fuss.

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
