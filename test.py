import unittest
import pandas as pd
import logging
from invoker import CombineDataCommand

# Setup logging for test outputs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestCombineDataCommand(unittest.TestCase):
    
    def setUp(self):
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
        print("\n***Test #1: Functionality of CombineDataCommand***\n")
        # Simulate the app object and data frames list to avoid GUI and isolate CombineDataCommand
        class MockApp: #By mocking App like this, we isolate the logic of the command and make sure we test the exact behavior we care about: how well the command combines data.
            def __init__(self):
                self.combined_data = None
        
        app = MockApp()

        # Print detailed step-by-step responses during the test
        print("Step 1: Creating CombineDataCommand with mock data...")
        
        # Instantiate the CombineDataCommand
        command = CombineDataCommand(app, [self.mock_db_data, self.mock_medicaid_data])

        print("Step 2: Executing CombineDataCommand...")
        
        # Execute the combine logic
        combined_data = command.execute()

        print("Step 3: Verifying combined data is not None...")
        
        # Assert that the data was combined successfully
        self.assertIsNotNone(combined_data, "The combined data should not be None. ❌")
        print("Combined data is not None. ✅")

        print("Step 4: Checking the number of rows in the combined data...")
        
        # Verify that we have the correct number of rows (in this case, 2 rows)
        self.assertEqual(len(combined_data), 2, "The combined data should have 2 rows. ❌")
        print(f"Combined data has {len(combined_data)} rows. ✅")

        print("Step 5: Checking the contents of combined data columns...")
        
        # Check if the resulting dataframe has the expected columns
        expected_columns = ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name', 'Child_Date_of_Birth']
        for col in expected_columns:
            self.assertIn(col, combined_data.columns, f"Column '{col}' should be in the combined data. ❌")
            print(f"Verified column '{col}' exists in the combined data. ✅")
        
        # Print combined data to verify visually
        print("Final combined data output:")
        print(combined_data)

        print("Step 6: Confirming that the test passed!")
        logging.info("Test passed: CombineDataCommand executed successfully and data was combined correctly.")

# Running the test
if __name__ == "__main__":
    unittest.main()
