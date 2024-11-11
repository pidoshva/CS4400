import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
import pandas as pd
import app  #  app.py class APP


class TestAssignNurse(unittest.TestCase):

    @patch('tkinter.Toplevel')  # Mocking the creation of the Toplevel window
    def test_assign_nurse_creates_window(self, MockToplevel):
        # Mock the profile window and other parameters
        mock_profile_window = MagicMock()
        child_data = {'Child_First_Name': 'John', 'Child_Last_Name': 'Doe', 'Mother_ID': 123, 'Child_Date_of_Birth': '2010-01-01'}
        mock_nurse_info_label = MagicMock()

        # Create an instance of the app class
        app_instance = app.App(mock_profile_window)  # Creating App instance

        # Mock the combined data to test nurse assignment
        app_instance._App__combined_data = pd.DataFrame({
            'Mother_ID': [123],
            'Child_First_Name': ['John'],
            'Child_Last_Name': ['Doe'],
            'Child_Date_of_Birth': ['2010-01-01'],
            'Assigned Nurse': [None]
        })

        # Simulate assigning a nurse
        app_instance.assign_nurse(child_data, mock_profile_window, mock_nurse_info_label)

        # Mock the user entering a nurse name
        mock_nurse_info_label.config.assert_called_once_with(text="Name: Nurse A")

        # Check that the DataFrame was updated with the nurse's name
        updated_data = app_instance._App__combined_data
        self.assertEqual(updated_data.at[0, 'Assigned Nurse'], 'Nurse A')

        # Check if the messagebox was shown
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            app_instance.assign_nurse(child_data, mock_profile_window, mock_nurse_info_label)
            mock_showinfo.assert_called_with("Success", "Nurse 'Nurse A' assigned successfully.")

        # Verify that Toplevel window was opened
        MockToplevel.assert_called_once_with(mock_profile_window)

    def test_assign_empty_nurse_name(self):
        app_instance = app.App()
        child_data = {
            'Child_First_Name': 'John',
            'Child_Last_Name': 'Doe',
            'Mother_ID': 123,
            'Child_Date_of_Birth': '2010-01-01'
        }
        mock_profile_window = MagicMock()
        mock_nurse_info_label = MagicMock()

        # Call the assign_nurse method with an empty nurse name
        with self.assertRaises(ValueError):  # Or check the specific error type/message expected
            app_instance.assign_nurse(child_data, mock_profile_window, mock_nurse_info_label, "")



if __name__ == '__main__':
    unittest.main()