import unittest
from unittest.mock import patch, MagicMock
import sys

# Add the project directory to the system path
sys.path.append('..')

# Import the main application code
from app import App

class TestApp(unittest.TestCase):

    @patch('app.filedialog.askopenfilename')  # Mock the file dialog to avoid manual file selection
    @patch('app.ReadExcelCommand')  # Mock the command execution to avoid real file reading
    def test_read_excel_file(self, mock_read_excel_command, mock_filedialog):
        # Create a root window mock
        root = MagicMock()

        # Instantiate the App class with a mock root window
        app = App(root)
        
       
        # Setup mock for file dialog return value
        mock_filedialog.return_value = "dummy_path.xlsx"

        # Setup mock for the command execute method
        mock_command_instance = mock_read_excel_command.return_value
        mock_command_instance.execute.return_value = MagicMock()  # Simulate returning a DataFrame

        # Call the function under test
        app.read_excel_file()

        # is the data frame appended to the data_frames list
        self.assertEqual(len(app._App__data_frames), 1)  #was 1 DataFrame is added
        mock_read_excel_command.assert_called_once()  # Verify the command was called
        
    @patch('app.filedialog.askopenfilename')  # Mock the file dialog to avoid manual file selection
    @patch('app.ReadExcelCommand')  # Mock the command execution to avoid real file reading
    def test_read_excel_file_no_file(self, mock_read_excel_command, mock_filedialog):
        
        root = MagicMock()
        app = App(root)

        # Setup mock for file dialog to simulate no file selection
        mock_filedialog.return_value = None  # Simulate no file selected
        app.read_excel_file()

        
        self.assertEqual(len(app._App__data_frames), 0)  # Check if no DataFrame was added
        mock_read_excel_command.assert_not_called() 

if __name__ == "__main__":
    unittest.main()

