import unittest
import pandas as pd
import os
import app_crypto
from cryptography.fernet import Fernet

class testfileEncryption(unittest.TestCase):
    def setUp(self):
        self.input_file = "input_test.xlsx"  # Add .xlsx extension for Excel format
        self.encrypted_file = 'encrypt_test'
        self.decrypted_file = 'decrypted_test'
        
        data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
        
        # Save the DataFrame as an Excel file
        df = pd.DataFrame(data)
        df.to_excel(self.input_file, index=False)

        # Write text to the file as per your test's requirements
        with open(self.input_file, 'w') as file:
            file.write("this is a test file for encryption")
        
        # Generate a valid Fernet key (32 bytes, base64-encoded)
        self.crypto_key = Fernet.generate_key()  # This is now a valid key

    def test_file_encryption_decription(self):
        # Call app_crypto.crypto directly
        app_crypto.Crypto.encrypt_file(self.input_file, self.crypto_key)
        with open(self.encrypted_file, 'rb') as file:
            try:
                file_content = file.read()
                # If it's not readable, it's likely encrypted
                self.assertTrue(self.is_binary(file_content), "Encrypted file should contain binary data.")
            except UnicodeDecodeError:
                self.assertTrue(True, "Encrypted file is not human-readable, as expected.")
        
        app_crypto.Crypto.decrypt_file(self.encrypted_file, self.crypto_key)
        
        with open(self.input_file, 'rb') as originalFile, open(self.decrypted_file, 'rb') as decryptedfile:
            original_file = originalFile.read()
            decrypted_file = decryptedfile.read()
            self.assertEqual(original_file, decrypted_file)
        
    def is_binary(self, data):
        try:
            data.decode('utf-8')
        except UnicodeDecodeError:
            return True
        return False
    
    def tearDown(self):
        """Clean up test files after the test."""
        for file in [self.input_file, self.encrypted_file, self.decrypted_file]:
            if os.path.exists(file):
                os.remove(file)
