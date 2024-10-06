import pandas as pd
from tkinter import filedialog, messagebox

class Command:
    """Command Interface"""
    def execute(self):
        raise NotImplementedError("Subclasses must implement the 'execute' method")


class ReadExcelCommand(Command):
    """Command to read Excel files"""
    def __init__(self, app):
        self.app = app
        self.filepath = None

    def execute(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if not self.filepath:
            messagebox.showerror("Error", "No file selected.")
            return None

        try:
            # Read the Excel file and replace spaces in columns for easier access
            data = pd.read_excel(self.filepath)
            data.columns = [column.replace(" ", "_") for column in data.columns]
            return data
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file '{self.filepath}': {e}")
            return None


class CombineDataCommand(Command):
    """Command to combine two datasets by Mother's Name and Child's DOB"""
    def __init__(self, app, data_frames):
        self.app = app
        self.data_frames = data_frames

    def execute(self):
        try:
            # Extract the two data frames
            database_data = self.data_frames[0]
            medicaid_data = self.data_frames[1]

            # Normalize names by stripping spaces, converting to lowercase, and removing non-alphabetic characters
            def normalize_name(name):
                if isinstance(name, str):
                    return ''.join(e for e in name if e.isalnum()).strip().lower()
                return name

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

            # Debugging: Print out sample rows to check names before merge
            print("\nDatabase Data (sample rows):")
            print(database_data[['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth']].head())

            print("\nMedicaid Data (sample rows):")
            print(medicaid_data[['Mother_First_Name', 'Last_Name', 'Child_Date_of_Birth']].head())

            # Merge the two datasets based on Mother's First Name, Last Name, and Child's Date of Birth
            combined_data = pd.merge(
                database_data,
                medicaid_data,
                left_on=['Mother_First_Name', 'Mother_Last_Name', 'Child_Date_of_Birth'],
                right_on=['Mother_First_Name', 'Last_Name', 'Child_Date_of_Birth'],
                how='inner',  # Use inner to ensure only exact matches are pulled
                suffixes=('_db', '_medicaid')
            )

            # Handle matched and unmatched data
            unmatched_in_database = combined_data[combined_data['Mother_First_Name'].isna()]
            unmatched_in_medicaid = combined_data[combined_data['Mother_First_Name'].isna()]

            # Output unmatched Mother IDs in the console
            unmatched_mother_ids = unmatched_in_database['Mother_ID'].dropna().tolist()
            for mother_id in unmatched_mother_ids:
                print(f"Unmatched Mother ID from Database: {mother_id}")

            unmatched_mother_ids = unmatched_in_medicaid['Mother_ID'].dropna().tolist()
            for mother_id in unmatched_mother_ids:
                print(f"Unmatched Mother ID from Medicaid: {mother_id}")

            # Filter matched data (entries that exist in both datasets)
            matched_data = combined_data.dropna(subset=['Mother_First_Name'])

            # Save the matched data to an Excel file
            matched_file_path = 'combined_matched_data.xlsx'
            matched_data.to_excel(matched_file_path, index=False)
            print(f"Matched data saved to {matched_file_path}")

            # Return the matched data to the app for display
            self.app.combined_data = matched_data
            return matched_data

        except Exception as e:
            messagebox.showerror("Error", f"Error combining data: {e}")
            return None


class Invoker:
    """Invoker class to store and execute commands"""
    def __init__(self):
        self.commands = []

    def add_command(self, command):
        """Add a command to the invoker"""
        self.commands.append(command)

    def execute_commands(self):
        """Execute all commands in sequence"""
        for command in self.commands:
            command.execute()
