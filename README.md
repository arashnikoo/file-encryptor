# file-encryptor

Encrypt and decrypt files with a password using AES-256-CBC.

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
