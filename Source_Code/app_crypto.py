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
    @staticmethod
    def encrypt_file(file_path, key):
        fernet = Fernet(key)
        """encrypts the given file using the provided Fernet key"""
        with open(file_path, "rb") as file:
              
            
            original_data = file.read()

        
        encrypted_data = fernet.encrypt(original_data)

        with open(file_path, "wb") as file:
            file.write(encrypted_data)
    @staticmethod
    def decrypt_file(file_path, key):
        """Decrypts the given file using the provided Fernet key"""

        fernet = Fernet(key)

        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        
        decrypted_data = fernet.decrypt(encrypted_data)

        with open(file_path, "wb") as file:
            file.write(decrypted_data)

    def is_encrypted(filepath):
        """
        Checks if a file is encrypted with Fernet.

        Args:
            filepath: The path to the file.
            key: The Fernet key used for encryption.

        Returns:
            True if the file is encrypted, False otherwise.
        """

        key = Crypto.loadKey()

        fernet = Fernet(key)

        try:
            with open(filepath, 'rb') as file:
                data = file.read()
                fernet.decrypt(data)
                return True
        except:
            return False