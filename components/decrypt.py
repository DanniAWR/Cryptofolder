import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import cryptography
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

def decrypt_file(file_path, key):
    f = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        logging.info(f"File decrypted successfully: {file_path}")
    except cryptography.fernet.InvalidToken:
        logging.error(f"Failed to decrypt {file_path}: Invalid key or corrupted data")
    except Exception as e:
        logging.error(f"Failed to decrypt {file_path}: {e}")

def decrypt_folder(folder_path, password, app_directory):
    salt_path = os.path.join(app_directory, 'salt')  # Utilisez le même chemin pour le fichier salt
    if not os.path.exists(salt_path):
        raise FileNotFoundError("Le fichier salt est introuvable. Assurez-vous qu'il est au bon endroit.")
    
    with open(salt_path, 'rb') as salt_file:
        salt = salt_file.read()

    key = derive_key(password.encode(), salt)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            decrypt_file(file_path, key)
