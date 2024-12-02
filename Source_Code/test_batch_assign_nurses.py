import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import tkinter as tk  # Import tkinter for StringVar
import app

class TestBatchAssignNurse(unittest.TestCase):
    @patch("app.messagebox.showinfo")  # Mock the messagebox.showinfo call
    @patch("app.messagebox.showerror")  # Mock the messagebox.showerror call
    def test_batch_assign_nurse(self, mock_showerror, mock_showinfo):
        root = MagicMock()
        app_batch_instance = app.App(root)

        # Mock the combined data
        app_batch_instance._App__combined_data = pd.DataFrame({
            'City': ['CityA', 'CityB'],
            'ZIP Code': ['84601', '84604'],
            'Assigned Nurse': [None, None]
        })

        # Mock the tk.StringVar.get method for inputs
        with patch.object(tk.StringVar, "get", side_effect=["CityA", "84601", "Nurse1"]):
            app_batch_instance.batch_assign_nurses()

            # Check if mock_showinfo was called
            print("showinfo called:", mock_showinfo.called)
            mock_showinfo.assert_called_once_with("Success", "Batch assignment completed for 1 row.")

            # Check if mock_showerror was called
            print("showerror called:", mock_showerror.called)

            # Assertions to check if the nurse was assigned correctly
            self.assertEqual(app_batch_instance._App__combined_data['Assigned Nurse'][0], 'Nurse1')
            self.assertIsNone(app_batch_instance._App__combined_data['Assigned Nurse'][1])

    @patch("app.messagebox.showerror")
    def test_empty_combined_data(self, mock_showerror):
        root = MagicMock()
        app_batch_instance = app.App(root)

        # Mock empty combined data
        app_batch_instance._App__combined_data = pd.DataFrame()

        # Mock the tk.StringVar.get method for inputs
        with patch.object(tk.StringVar, "get", side_effect=["CityA", "84601", "Nurse1"]):
            app_batch_instance.batch_assign_nurses()

            # Assertions for error handling
            mock_showerror.assert_called_once_with("Error", "No data available for batch assignment.")

    @patch("app.messagebox.showinfo")
    def test_missing_city_or_zip(self, mock_showinfo):
        root = MagicMock()
        app_batch_instance = app.App(root)

        # Mock the combined data
        app_batch_instance._App__combined_data = pd.DataFrame({
            'City': ['CityA', None],
            'ZIP Code': ['84601', None],
            'Assigned Nurse': [None, None]
        })

        # Mock the tk.StringVar.get method for inputs
        with patch.object(tk.StringVar, "get", side_effect=["CityA", "", "Nurse1"]):  # Missing ZIP Code
            app_batch_instance.batch_assign_nurses()

            # Assertions for handling missing ZIP Code
            self.assertEqual(app_batch_instance._App__combined_data['Assigned Nurse'][0], 'Nurse1')
            self.assertIsNone(app_batch_instance._App__combined_data['Assigned Nurse'][1])

# Run the tests
if __name__ == "__main__":
    unittest.main()



    

  
 
 