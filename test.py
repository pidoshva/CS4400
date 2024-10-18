# -*- coding: utf-8 -*-

import unittest
import pandas as pd
import logging
import os
from unittest.mock import patch, MagicMock
from invoker import CombineDataCommand
from app import App

# Setup logging for test outputs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestApp(unittest.TestCase):
    """
    Unit tests for the App class, focusing on reading Excel files 
    and mocking the behavior of the ReadExcelCommand.
    """

    @patch('app.filedialog.askopenfilename')  # Mock the file dialog to avoid manual file selection
    @patch('app.ReadExcelCommand')  # Mock the command execution to avoid real file reading
    def test_read_excel_file(self, mock_read_excel_command, mock_filedialog):
        """
        Test case for verifying the behavior of the read_excel_file method.
        This test ensures that the ReadExcelCommand is executed and that
        a DataFrame is appended to the data_frames list.
        """
        print("\n" + "*" * 50)
        print("*** Test #1: Read Excel File Functionality ***")
        print("*" * 50 + "\n")

        # Create a root window mock
        root = MagicMock()

        # Instantiate the App class with a mock root window
        app = App(root)

        # Setup mock for file dialog return value
        mock_filedialog.return_value = "dummy_path.xlsx"

        # Setup mock for the command execute method, simulating returning a DataFrame
        mock_command_instance = mock_read_excel_command.return_value
        mock_command_instance.execute.return_value = MagicMock()  

        # Step 1: Calling read_excel_file function
        print("Step 1: 📄 Calling read_excel_file function...")
        app.read_excel_file()

        # Step 2: Verifying that the data frame is appended
        print("Step 2: 🔍 Verifying the data frame was added to data_frames list...")
        self.assertEqual(len(app._App__data_frames), 1, "The data frame should be added to the data_frames list. [FAIL]")
        print("✅ Data frame successfully added.\n")

        # Step 3: Verifying the command was called
        print("Step 3: 🔄 Verifying that ReadExcelCommand was called once...")
        mock_read_excel_command.assert_called_once()
        print("✅ ReadExcelCommand was called once.\n")


class TestCombineDataCommand(unittest.TestCase):
    """
    Unit tests for the CombineDataCommand class, which combines data from
    two Excel files (hospital and Medicaid datasets). This test focuses on
    verifying the combination of data and file generation.
    """

    def setUp(self):
        """
        Set up mock data frames that simulate the structure of Excel data.
        These data frames represent the hospital and Medicaid datasets.
        """
        # Create mock dataframes to simulate Excel data
        self.mock_db_data = pd.DataFrame({
            'Child_Last_Name': ['Doe', 'Smith'],
            'Child_First_Name': ['Alice', 'Bob'],
            'Child_Middle_Name': ['Marie', 'James'],
            'DOB': ['2021-05-10', '2020-08-21'],  # Child's Date of Birth
            'Mother_Last_Name': ['Doe', 'Smith'],
            'Mother_First_Name': ['Jane', 'John'],
            'State_File_Number': [12345, 67890]  # Example data
        })

        self.mock_medicaid_data = pd.DataFrame({
            'Mother_First_Name': ['Jane', 'John'],
            'Last_Name': ['Doe', 'Smith'],
            'Mother_DOB': ['1980-05-10', '1978-12-22'],  # Mother's Date of Birth
            'Mother_ID': [98765, 54321],
            'Child_ID': [1001, 1002],
            'Child_DOB': ['2021-05-10', '2020-08-21'],  # Child's Date of Birth
            'Case_ID': [111, 222],
            'Phone_#': ['123-456-7890', '098-765-4321'],
            'Mobile_#': ['123-456-7891', '098-765-4322'],
            'Street': ['123 Main St', '456 Maple Ave'],
            'City': ['Springfield', 'Mapleton'],
            'State': ['UT', 'UT'],
            'ZIP': ['84001', '84002'],
            'County': ['Utah', 'Utah'],
            'Tobacco_Usage': [False, True],
            'Utah_First_Time_Man.': [False, True]
        })

    def test_combine_data(self):
        """
        Test case for the CombineDataCommand class. This test verifies that
        the CombineDataCommand successfully merges two datasets and produces
        the correct combined result.
        """
        print("\n" + "*" * 50)
        print("*** Test #2: Functionality of CombineDataCommand ***")
        print("*" * 50 + "\n")
        
        # Simulate the app object and data frames list to avoid GUI and isolate CombineDataCommand
        class MockApp: 
            def __init__(self):
                self.combined_data = None
        
        app = MockApp()

        # Step 1: Creating CombineDataCommand with mock data
        print("Step 1: 📑 Creating CombineDataCommand with mock data...")
        command = CombineDataCommand(app, [self.mock_db_data, self.mock_medicaid_data])

        # Step 2: Executing CombineDataCommand
        print("Step 2: ⚙️ Executing CombineDataCommand...")
        combined_data = command.execute()

        # Step 3: Verifying combined data is not None
        print("Step 3: 🔍 Verifying combined data is not None...")
        self.assertIsNotNone(combined_data, "The combined data should not be None. [FAIL]]")
        print("✅ Combined data is not None.\n")

        # Step 4: Checking the number of rows in the combined data
        print("Step 4: 🔢 Checking the number of rows in the combined data...")
        self.assertEqual(len(combined_data), 2, "The combined data should have 2 rows. [FAIL]")
        print(f"✅ Combined data has {len(combined_data)} rows.\n")

        # Step 5: Checking the contents of combined data columns
        print("Step 5: 📝 Checking the contents of combined data columns...")
        expected_columns = ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name', 'Child_Date_of_Birth']
        for col in expected_columns:
            self.assertIn(col, combined_data.columns, f"Column '{col}' should be in the combined data. [FAIL]")
            print(f"✅ Verified column '{col}' exists in the combined data.\n")

        # Step 6: Print the combined data
        print("📊 Final combined data output:")
        print(combined_data)

        # Step 7: Confirming that the test passed
        print("\nStep 7: ✅ Confirming that the test passed!")
        logging.info("Test passed: CombineDataCommand executed successfully and data was combined correctly.\n")

    def test_excel_file_generation(self):
        """
        Test case for verifying that the CombineDataCommand correctly generates
        an Excel file after data combination. The file is cleaned up after the test.
        """
        print("\n" + "*" * 50)
        print("*** Test #3: Excel File Generation After Data Combination ***")
        print("*" * 50 + "\n")
        
        # Simulate the app object
        class MockApp: 
            def __init__(self):
                self.combined_data = None
        
        app = MockApp()

        # Step 1: Executing CombineDataCommand with mock data
        print("Step 1: ⚙️ Executing CombineDataCommand...")
        command = CombineDataCommand(app, [self.mock_db_data, self.mock_medicaid_data])
        command.execute()

        # Step 2: Checking if the Excel file is generated
        print("Step 2: 📂 Checking if the Excel file is generated...")
        output_file = 'combined_matched_data.xlsx'
        self.assertTrue(os.path.exists(output_file), f"File '{output_file}' should exist after combination. [FAIL]")
        print(f"✅ File '{output_file}' was successfully generated.\n")

        # Step 3: Confirming file generation test passed
        print("Step 3: ✅ Confirming file generation test passed!")
        logging.info("Test passed: Excel file generated correctly.")

        # Cleanup: Remove the generated Excel file
        if os.path.exists(output_file):
            os.remove(output_file)
            print(f"✅ File '{output_file}' has been cleaned up after the test.\n")


# Running the tests
if __name__ == "__main__":
    unittest.main()

