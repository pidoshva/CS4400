import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
import app

class TestDateOfBirthSort(unittest.TestCase):

    @patch("app.messagebox.showerror")
    def test_date_of_birth(self, mock_showerror):
        # Create the app instance and mock UI elements
        mock_root = MagicMock()
        app_instance = app.App(mock_root)
        
        # Mock the combined data (DataFrame with date of birth)
        app_instance._App__combined_data = pd.DataFrame({
            'Child_Date_of_Birth': [datetime(2019, 5, 20), datetime(2015, 1, 4), datetime(2018, 8, 15)],
            'Child_Name': ['Alacran', 'Snoopy', 'Twopac']
        })
        
        # Mock the Treeview and Sort button
        mock_treeview = MagicMock()
        mock_sort_button = MagicMock()
        
        # Mock method to update names
        app_instance.update_combined_names = MagicMock()

        # Test the descending order (sort by oldest first)
        app_instance.sort_combined_data(mock_treeview, mock_sort_button)
        
        # Expected result after descending sort
        expected_descending = [pd.Timestamp(datetime(2019, 5, 20)),
                               pd.Timestamp(datetime(2018, 8, 15)),
                               pd.Timestamp(datetime(2015, 1, 4))]

        # Actual sorted result
        actual_descending = app_instance._App__combined_data['Child_Date_of_Birth'].tolist()

        self.assertEqual(actual_descending, expected_descending)

        # Check if button text was updated to show descending order
        mock_sort_button.config.assert_called_with(text="Sort by DOB ▼")

        # Ensure update_combined_names was called once
        app_instance.update_combined_names.assert_called_once()

        # Test the second click (ascending order)
        app_instance.sort_combined_data(mock_treeview, mock_sort_button)

        # Expected result after ascending sort
        expected_ascending = [pd.Timestamp(datetime(2015, 1, 4)),
                              pd.Timestamp(datetime(2018, 8, 15)),
                              pd.Timestamp(datetime(2019, 5, 20))]

        # Actual sorted result after the second click
        actual_ascending = app_instance._App__combined_data['Child_Date_of_Birth'].tolist()

        self.assertEqual(actual_ascending, expected_ascending)

        # Check if button text was updated to show ascending order
        mock_sort_button.config.assert_called_with(text="Sort by DOB ▲")

        # Ensure update_combined_names was called twice
        self.assertEqual(app_instance.update_combined_names.call_count, 2)

        # Test for empty DataFrame and error handling
        app_instance._App__combined_data = pd.DataFrame()
        app_instance.sort_combined_data(mock_treeview, mock_sort_button)
        mock_showerror.assert_called_once_with("Error", "No data available for sorting.")

if __name__ == "__main__":
    unittest.main()





  
  
  