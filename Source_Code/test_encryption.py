import unittest
import pandas as pd
import os
import sys
import app_crypto

import cryptography


class testfileEncryption(unittest.TestCase):
 def setUp(self):
  self.input_file = "input_test"
  self.encrypted_file ='encypt_test'
  self.decypted_file ='decrypted_test'
  data = {
            'Name': ['Alice', 'Bob', 'Charlie'],
            'Age': [25, 30, 35],
            'City': ['New York', 'Los Angeles', 'Chicago']
        }
  df = pd.DataFrame(data)
  df.to_excel(self.input_file, index=False)
  
  with open(self.input_file, 'w') as file:
   file.write("this is a test file for encryption")
   
   self.crypto_key = b'1234567890abcdef'  # 16 bytes for 128-bit AES encryption

def test_file_encryption_decription(self) :
  self.app_crypto.crypto.encrypt_file(self.input_file,self.crypto_key)
  with open(self.encrypted_file, 'r') as file:
    try:
        file_content = file.read()
        # If it's not readable, it's likely encrypted
        self.assertTrue(is_binary(file_content), "Encrypted file should contain binary data.")
    except UnicodeDecodeError:
        self.assertTrue(True, "Encrypted file is not human-readable, as expected.")
  self.app_crypto.crypto.decrypt_file(self.encrypted_file,self.crypto_key)
  with open(self.input_file, 'rb') as originalFile, open(self.decypted_file,'rb') as decriptedfile:
   original_file = originalFile.read()
   decrip_file = decriptedfile.read()
   self.assertEqual(original_file,decrip_file),
   #should I run teardown function here?
     # checks for data that is not text
  #if the byte sequence can be successfully decoded into a string using the UTF-8 encoding.
  def is_binary(data):
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
             
if __name__ == '__main__':
    unittest.main()