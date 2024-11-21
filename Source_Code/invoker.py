import pandas as pd
from tkinter import filedialog, messagebox
import logging
from app_crypto import *

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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

    def execute(self, filepath):
        """
        Execute the file selection and read the Excel data into a pandas DataFrame.
        
        Returns:
            DataFrame: A pandas DataFrame representing the content of the Excel file.
        """
        
        if not filepath:
            logging.error("No file selected.")
            messagebox.showerror("Error", "No file selected.")
            return None

        try:
            # Read the Excel file into a DataFrame and normalize column names
            data = pd.read_excel(filepath)
            data.columns = [column.replace(" ", "_") for column in data.columns]
            logging.info(f"Successfully read file: {filepath}")
            return (data)
        except Exception as e:
            logging.error(f"Error reading file '{filepath}': {e}")
            messagebox.showerror("Error", f"Error reading file '{filepath}': {e}")
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
            DataFrame: A pandas DataFrame containing the combined data.
        """
        try:
            # Extract the two data frames
            database_data = self.data_frames[0]
            medicaid_data = self.data_frames[1]

            # Standardize columns for merging
            database_data.rename(columns={'DOB': 'Child_Date_of_Birth'}, inplace=True)
            medicaid_data.rename(columns={'Child_DOB': 'Child_Date_of_Birth', 'Last_Name': 'Mother_Last_Name'}, inplace=True)

            # Normalize the names for matching
            for df in [database_data, medicaid_data]:
                for col in ['Mother_First_Name', 'Mother_Last_Name']:
                    df[col] = df[col].str.lower().str.replace(r'\W', '', regex=True)

            # Convert DOB columns to consistent date format
            database_data['Child_Date_of_Birth'] = pd.to_datetime(database_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')
            medicaid_data['Child_Date_of_Birth'] = pd.to_datetime(medicaid_data['Child_Date_of_Birth'], errors='coerce').dt.strftime('%Y-%m-%d')

            # Merge to get combined data
            combined_data = pd.merge(
                database_data,
                medicaid_data,
                on=['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth'],
                how='inner',
                suffixes=('_db', '_medicaid')
            )
            logging.info("Matched data combined successfully.")

            
            # Identify unmatched data
            unmatched_database = database_data[~database_data.apply(
                lambda row: ((combined_data['Mother_First_Name'] == row['Mother_First_Name']) &
                            (combined_data['Mother_Last_Name'] == row['Mother_Last_Name']) &
                            (combined_data['Child_Date_of_Birth'] == row['Child_Date_of_Birth'])).any(), axis=1)].copy()
            unmatched_database['Source'] = 'Database'

            unmatched_medicaid = medicaid_data[~medicaid_data.apply(
                lambda row: ((combined_data['Mother_First_Name'] == row['Mother_First_Name']) &
                            (combined_data['Mother_Last_Name'] == row['Mother_Last_Name']) &
                            (combined_data['Child_Date_of_Birth'] == row['Child_Date_of_Birth'])).any(), axis=1)].copy()
            unmatched_medicaid['Source'] = 'Medicaid'


            # Check if there are unmatched rows in either data frame
            if not unmatched_database.empty or not unmatched_medicaid.empty:
                # Standardize unmatched data columns to align with combined_data
                unmatched_database = unmatched_database.reindex(columns=combined_data.columns.tolist() + ['Source'], fill_value='')
                unmatched_medicaid = unmatched_medicaid.reindex(columns=combined_data.columns.tolist() + ['Source'], fill_value='')

                # Concatenate unmatched records
                unmatched_data = pd.concat([unmatched_database, unmatched_medicaid], ignore_index=True)

                # Capitalize all names in unmatched data
                for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                    if col in unmatched_data.columns:
                        unmatched_data[col] = unmatched_data[col].str.capitalize()

                # Save the unmatched data to an Excel file
                unmatched_file_path = 'unmatched_data.xlsx'
                unmatched_data.to_excel(unmatched_file_path, index=False)
                logging.info(f"Unmatched data saved to {unmatched_file_path}")
            else:
                logging.info("No unmatched data found; skipping unmatched data file creation.")

            # Capitalize all names in matched data
            for col in ['Mother_First_Name', 'Mother_Last_Name', 'Child_First_Name', 'Child_Last_Name']:
                if col in combined_data.columns:
                    combined_data[col] = combined_data[col].str.capitalize()

            # Save the matched data
            matched_file_path = 'combined_matched_data.xlsx'
            combined_data.to_excel(matched_file_path, index=False)
            logging.info(f"Matched data saved to {matched_file_path}")

            # Return matched data to the app for display
            self.app.combined_data = combined_data
            return combined_data

        except Exception as e:
            logging.error(f"Error combining data: {e}")
            messagebox.showerror("Error", f"Error combining data: {e}")
            return None


class GenerateKeyCommand(Command):
    def __init__(self, app):
        self.app = app
    
    def execute(self):
            Crypto.generateKey()
    
class DeleteFileCommand(Command):
    def __init__(self, app):
        self.app = app

    def execute(self, path):
        os.remove(path)

class EncryptFileCommand(Command):
    def __init__(self, app):
        self.app = app
    
    def execute(self, filepath = None):
        try:
            logging.info("Attempting to encrypt files.")
            if filepath == None:
                logging.info("Browsing file.")
                filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
            key = Crypto.loadKey()
            Crypto.encrypt_file(filepath, key)
            logging.info("Files encrypted")
            return True
        except:
            logging.info("Files could not be encrypted")
            return False

class DecryptFileCommand(Command):
    def __init__(self, app):
        self.app = app
    
    def execute(self, filepath):
        try:
            key = Crypto.loadKey()
            Crypto.decrypt_file(filepath, key)
            return True
        except:
            return False
        

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
        logging.info(f"Command added: {command.__class__.__name__}")

    def execute_commands(self):
        """
        Execute all commands in sequence.
        """
        for command in self.commands:
            command.execute()
            logging.info(f"Executed command: {command.__class__.__name__}")
