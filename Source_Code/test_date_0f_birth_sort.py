import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import app

class TestDateOfBirthSort(unittest.TestCase):
 @patch("app.messagebox.showerror") 
 def test_date_of_birth(self, mock_showerror):
  mock_root = MagicMock()
  app_instance = app.App(mock_root)
  app_instance._App__combined_data = pd.DataFrame({'Child_Date_Of_Birth':[datetime(2019,5,20), datetime(2015,1,4), datetime(2018,8,15)],
                                                   'Child_Name':['Alacran', 'Snoopy', 'twopac']
			
   
   
		})
  mock_treeview = MagicMock()
  mock_sort_button = MagicMock()
  
  app_instance.update_combined_names = MagicMock()
  
  app_instance.sort_ascending =False
  app_instance.sort_combined_data(mock_treeview,mock_sort_button) 
  
  expected_ascending = app_instance._App__combined_data['Child_Date_Of_Birth'].tolist()
  self.assertEqual(expected_ascending,[datetime(2015,1,4),datetime(2018,8,15),datetime(2019,5,20)])
  #click event testing
  mock_sort_button.config.assert_called_with(text="Sort by DOB ▲")
  
  app_instance.update_combined_names.assert_called_once()
  
  app_instance.sort_combined_data(mock_treeview, mock_sort_button)
  expected_descending = app_instance._App__combined_data['Child_Date_Of_Birth'].tolist()
  self.assertEqual(expected_descending,[datetime(2019,5,20),datetime(2018,8,15),datetime(2015,1,4)])
  
  mock_sort_button.config.assert_called_with(text="Sort by DOB \u25BC ")
  self.assertEqual(app_instance.update_combined_names.call_count, 2)
  app_instance._App__combined_data = pd.DataFrame()
  app_instance.sort_combined_data(mock_treeview,mock_sort_button)
  mock_showerror.assert_called_once_with("Error","No sorting data found")
  
if __name__ == "__main__":
    unittest.main()
  
  
  