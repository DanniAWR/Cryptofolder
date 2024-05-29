import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import logging




def derive_key(password: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_file(file_path, key):
    f = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = f.encrypt(file_data)
        with open(file_path, "wb") as file:
            file.write(encrypted_data)
        logging.info(f"File encrypted successfully: {file_path}")
    except Exception as e:
        logging.error(f"Failed to encrypt {file_path}: {e}")

def encrypt_folder(folder_path, password, app_directory):
    salt_path = os.path.join(app_directory, 'salt')  # Chemin fixe pour le fichier salt
    if not os.path.exists(salt_path):  # Si le fichier salt n'existe pas, créez-le
        salt = os.urandom(16)
        with open(salt_path, 'wb') as salt_file:
            salt_file.write(salt)
    else:
        with open(salt_path, 'rb') as salt_file:
            salt = salt_file.read()

    key = derive_key(password.encode(), salt)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            encrypt_file(file_path, key)

