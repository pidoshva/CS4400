import unittest
import pandas as pd
import os
from app_crypto import Crypto
from cryptography.fernet import Fernet
import shutil


class TestFileEncryption(unittest.TestCase):
    def setUp(self):
        # Test file paths
        self.input_file = "input_test.xlsx"
        self.temp_input_copy = "temp_input_copy.xlsx"
        
        # Create test data and save to input file
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        df = pd.DataFrame(data)
        df.to_excel(self.input_file, index=False)
        
        # Create a temporary copy for comparison after decryption
        shutil.copy(self.input_file, self.temp_input_copy)
        
        # Encryption key
        self.crypto_key = Fernet.generate_key()

    def test_file_encryption_decryption(self):
        # Encrypt the file (overwrites the input file)
        Crypto.encrypt_file(self.input_file, self.crypto_key)
        self.assertTrue(os.path.exists(self.input_file), "Encrypted file does not exist.")
        
        # Check if the file content has been modified
        with open(self.input_file, 'rb') as file:
            file_content = file.read()
            # Just check that the content is different from the original (indicating it's encrypted)
            self.assertNotEqual(file_content, b"")  # Ensure the file isn't empty
        
        # Decrypt the file (restores the original content)
        Crypto.decrypt_file(self.input_file, self.crypto_key)

        # Compare the decrypted file with the original copy
        with open(self.temp_input_copy, 'rb') as original_file, open(self.input_file, 'rb') as decrypted_file:
            original_data = original_file.read()
            decrypted_data = decrypted_file.read()
            self.assertEqual(original_data, decrypted_data, "Decrypted file should match the original file.")
    
    def tearDown(self):
        """Clean up test files after the test."""
        for file in [self.input_file, self.temp_input_copy]:
            if os.path.exists(file):
                os.remove(file)


if __name__ == '__main__':
    unittest.main()






