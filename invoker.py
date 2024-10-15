import pandas as pd
from tkinter import filedialog, messagebox

class Command:
    """
    Command Interface:
    Abstract Command inherited by other commands invoked by tkinter buttons.
    """
    def execute(self):
        """
        Abstract method that contains the logic of the sub-commands.
        """
        raise NotImplementedError("Subclasses must implement the 'execute' method")

class ReadExcelCommand(Command):
    """
    Command to read Excel files.
    This command prompts a file explorer for selecting Excel files.
    
    Args:
        app: The application object that holds the application state.
    """
    def __init__(self, app):
        self.app = app
        self.filepath = None

    def execute(self):
        """
        Execute the file selection and read the Excel data into a pandas DataFrame.
        
        Returns:
            DataFrame: A pandas DataFrame representing the content of the Excel file.
        """
        self.filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not self.filepath:
            messagebox.showerror("Error", "No file selected.")
            return None

        try:
            # Read the Excel file into a DataFrame and normalize column names
            data = pd.read_excel(self.filepath)
            data.columns = [column.replace(" ", "_") for column in data.columns]
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file '{self.filepath}': {e}")
            return None

class CombineDataCommand(Command):
    """
    Command to combine two data sets (Excel files) by Mother's Name and Child's Date of Birth.
    
    Args:
        app: The application object.
        data_frames (list): List of data frames from the two Excel files.
    """
    def __init__(self, app, data_frames):
        self.app = app
        self.data_frames = data_frames

    def execute(self):
        """
        Execute the combination of two data frames based on Mother's Name and Child's Date of Birth.
        The result is saved to an Excel file and returned for UI display.

        Returns:
            DataFrame: A
            DataFrame: A pandas DataFrame containing the combined data.
        """
        try:
            # Extract the two data frames
            database_data = self.data_frames[0]
            medicaid_data = self.data_frames[1]

            # Normalize names by stripping spaces, converting to lowercase, and removing non-alphabetic characters
            def normalize_name(name):
                if isinstance(name, str):
                    return ''.join(e for e in name if e.isalnum()).strip().lower()
                return name

            # Normalize the data for consistent merging
            database_data['Mother_First_Name'] = database_data['Mother_First_Name'].apply(normalize_name)
            database_data['Mother_Last_Name'] = database_data['Mother_Last_Name'].apply(normalize_name)
            medicaid_data['Mother_First_Name'] = medicaid_data['Mother_First_Name'].apply(normalize_name)
            medicaid_data['Last_Name'] = medicaid_data['Last_Name'].apply(normalize_name)

            # Ensure both datasets have a standardized Child Date of Birth column
            database_data.rename(columns={'DOB': 'Child_Date_of_Birth'}, inplace=True)
            medicaid_data.rename(columns={'Child_DOB': 'Child_Date_of_Birth'}, inplace=True)

            # Convert Child_Date_of_Birth to a consistent format
            database_data['Child_Date_of_Birth'] = pd.to_datetime(database_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')
            medicaid_data['Child_Date_of_Birth'] = pd.to_datetime(medicaid_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')

            # Merge the two datasets based on Mother's First Name, Last Name, and Child's Date of Birth
            combined_data = pd.merge(
                database_data,
                medicaid_data,
                left_on=['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth'],
                right_on=['Mother_First_Name', 'Last_Name', 'Child_Date_of_Birth'],
                how='inner',  # Use inner join to ensure only exact matches are included
                suffixes=('_db', '_medicaid')
            )

            # Drop the duplicated 'Last_Name' column from Medicaid data
            combined_data.drop(columns=['Last_Name'], inplace=True)

            # Capitalize the first letter of first names and last names
            combined_data['Mother_First_Name'] = combined_data['Mother_First_Name'].str.capitalize()
            combined_data['Mother_Last_Name'] = combined_data['Mother_Last_Name'].str.capitalize()
            combined_data['Child_First_Name'] = combined_data['Child_First_Name'].str.capitalize()
            combined_data['Child_Last_Name'] = combined_data['Child_Last_Name'].str.capitalize()

            # Save the matched data to an Excel file
            matched_file_path = 'combined_matched_data.xlsx'
            combined_data.to_excel(matched_file_path, index=False)
            print(f"Matched data saved to {matched_file_path}")

            # Return the matched data to the app for display
            self.app.combined_data = combined_data
            return combined_data

        except Exception as e:
            messagebox.showerror("Error", f"Error combining data: {e}")
            return None

class Invoker:
    """
    Invoker class to store and execute commands.
    The Invoker contains the history of all commands issued. It is responsible for executing these commands sequentially.
    """
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        """
        Add a command to the invoker.

        Args:
            command (Command): The command to be added.
        """
        self.commands.append(command)

    def execute_commands(self):
        """
        Execute all commands in sequence.
        """
        for command in self.commands:
            command.execute()
