import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
import app

class TestGenerateReport(unittest.TestCase):

    def test_generate_report(self):
        # Mock the Tkinter root
        mock_root = MagicMock()
        
        # Create an instance of App with the mocked root
        app_generate_instance = app.App(mock_root)
        
        # Mock the required attributes for the test
        app_generate_instance.__root = mock_root
        app_generate_instance.__combined_data = pd.DataFrame({
            'Child_Date_of_Birth': [datetime(2015, 5, 1), datetime(2020, 6, 1), None],
            'Assign Nurse': ['Nurse A', 'Nurse B', None],
            'State': ['State x', 'State y', 'State z'],
            'Child_First_Name': ['Alice', 'Bob', 'John'],
            'Child_Last_Name': ['Lucas', 'Jasitos', 'Bowen']
        })

        with patch("app.tk.Toplevel") as mock_toplevel, \
             patch("app.ttk.Treeview") as mock_treeview, \
             patch("app.tk.Label") as mock_label, \
             patch("app.messagebox.showerror") as mock_showerror:
            # Call the method to test
            app_generate_instance.generate_report()

            # Assert the mocked components were called
            mock_toplevel.assert_awaited_once()
            mock_treeview.assert_called()
            mock_label.assert_called()

            # Check the label text (adjust if needed to match your implementation)
            assert mock_label.call_args_list[0][0][0] == "Total children Assign: 3"
            assert mock_label.call_args_list[1][0][0] == "Unassigned children: 1"
            
            # Ensure no errors were shown
            mock_showerror.assert_not_called()

if __name__ == "__main__":
    unittest.main()

