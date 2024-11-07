from cryptography.fernet import Fernet
import os

class Crypto:
    def generateKey():
            """Generates a new Fernet key and saves it to a file"""
            key = Fernet.generate_key()
            with open("key.txt", "wb") as key_file:
                key_file.write(key)

    def loadKey():
        """Loads the key from a file"""
        with open("key.txt", "rb") as key_file:
            key = key_file.read()
        return key

    def encrypt_file(file_path, key):
        """encrypts the given file using the provided Fernet key"""
        with open(file_path, "rb") as file:
            original_data = file.read()

        fernet = Fernet(key)
        encrypted_data = fernet.encrypt(original_data)

        with open(file_path, "wb") as file:
            file.write(encrypted_data)

    def decrypt_file(file_path, key):
        """Decrypts the given file using the provided Fernet key"""

        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path, "wb") as file:
            file.write(decrypted_data)