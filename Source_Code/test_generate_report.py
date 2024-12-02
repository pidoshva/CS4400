import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
import app

class TestGenerateReport(unittest.TestCase):

    @patch("app.tk.Toplevel")  # Mock the Tkinter Toplevel class
    @patch("app.ttk.Treeview")  # Mock the Treeview class
    @patch("app.tk.Label")      # Mock the Label class
    @patch("app.messagebox.showerror")  # Mock the showerror function
    def test_generate_report(self, mock_showerror, mock_label, mock_treeview, mock_toplevel):
        # Mock the Tkinter root
        mock_root = MagicMock()

        # Create an instance of App with the mocked root
        app_instance = app.App(mock_root)
        
        # Mock the combined data as an instance variable
        app_instance._App__combined_data = pd.DataFrame = pd.DataFrame({
            'Child_Date_of_Birth': [datetime(2015, 5, 1), datetime(2020, 6, 1), None],
            'Assigned Nurse': ['Nurse A', 'Nurse B', None],
            'State': ['State x', 'State y', 'State z'],
            'Child_First_Name': ['Alice', 'Bob', 'John'],
            'Child_Last_Name': ['Lucas', 'Jasitos', 'Bowen']
        })

        # Call the instance method to test
        app_instance.generate_report()  # Call the method on the instance

        # Assert the mocked components were called
        mock_toplevel.assert_called_once()  
        mock_treeview.assert_called()
        mock_label.assert_called()

        # Print the entire call_args_list to see the passed arguments
        print(mock_label.call_args_list)

        # Check the label text 
        assert mock_label.call_args_list[0][1]["text"] == "Total Children: 3"
        assert mock_label.call_args_list[1][1]["text"] == "Unassigned Children: 1"
        
        # Ensure no errors were shown
        mock_showerror.assert_not_called()

if __name__ == "__main__":
    unittest.main()





