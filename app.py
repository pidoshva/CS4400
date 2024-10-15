import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import logging
from invoker import ReadExcelCommand, CombineDataCommand, Invoker

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    """
    The main application class for combining two Excel files.
    It handles user interactions for reading files, combining data, and displaying profiles.
    
    Attributes:
        root (Tk): The main root window for tkinter.
        invoker (Invoker): The Invoker object that stores and executes commands.
        data_frames (list): List to store the data frames from two Excel files.
        combined_data (DataFrame): The combined data after merging the two data frames.
    """
    def __init__(self, root):
        """
        Initialize the main application, setup the UI, and initialize variables.

        Args:
            root (Tk): The main root window for tkinter.
        """
        self.root = root
        self.root.title("Excel Combiner")

        # Initialize variables
        self.invoker = Invoker()  # Create an Invoker to manage commands
        self.data_frames = []  # Store the two data frames to be combined
        self.combined_data = None  # Store the combined data

        logging.info("Application initialized.")
        
        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """
        Create the UI elements including buttons to read Excel files, combine data, and display profiles.
        """
        # Buttons for reading two Excel files
        self.read_button1 = tk.Button(self.root, text="Read Excel File 1", command=self.read_excel_file)
        self.read_button1.pack(pady=5)

        self.read_button2 = tk.Button(self.root, text="Read Excel File 2", command=self.read_excel_file)
        self.read_button2.pack(pady=5)

        # Button to combine the data
        self.combine_button = tk.Button(self.root, text="Combine Data", command=self.combine_data)
        self.combine_button.pack(pady=5)

        logging.info("UI widgets created.")

    def read_excel_file(self):
        """
        Read an Excel file and append its data to the list of data frames.
        """
        command = ReadExcelCommand(self)
        self.invoker.add_command(command)
        data_frame = command.execute()
        if data_frame is not None:
            self.data_frames.append(data_frame)
            logging.info(f"Data from {command.filepath} successfully read and added to data frames.")
        else:
            logging.warning("No data frame returned from the file read.")

    def combine_data(self):
        """
        Combine the two read Excel files and display the combined names.
        This is done using the CombineDataCommand which merges the two data frames.
        """
        if len(self.data_frames) >= 2:
            logging.info("Attempting to combine data from two Excel files.")
            command = CombineDataCommand(self, self.data_frames)
            self.invoker.add_command(command)
            combined_data = command.execute()

            if combined_data is not None:
                # Store combined data in app
                self.combined_data = combined_data
                # Display the combined names in the UI window
                self.display_combined_names()
                logging.info("Data combined and displayed successfully.")
        else:
            messagebox.showwarning("Warning", "Please read two Excel files first.")
            logging.warning("Attempted to combine data with less than two files.")

    def display_combined_names(self):
        """
        Display a new window with the list of combined names (Mother ID, Child Name, DOB) 
        and add a search bar for filtering.
        """
        combined_names_window = tk.Toplevel(self.root)
        combined_names_window.title("Combined Data")

        logging.info("Displaying combined names window.")

        # Frame for search bar and button
        search_frame = tk.Frame(combined_names_window)
        search_frame.pack(fill=tk.X, pady=5)

        # Search Entry widget
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        # Search Button
        search_button = tk.Button(search_frame, text="Search", command=self.search_combined_names)
        search_button.pack(side=tk.RIGHT, padx=10)

        # Listbox to display combined names
        self.listbox = tk.Listbox(combined_names_window)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        # Add the combined names to the listbox (Mother ID, Child Name, DOB)
        self.update_combined_names_listbox()

        # Bind double-click event to open child profile
        self.listbox.bind('<Double-1>', lambda event: self.show_child_profile(event, self.listbox))

    def update_combined_names_listbox(self):
        """
        Update the Listbox with combined names (Mother ID, Child Name, DOB), 
        filtering the results based on the search term.
        """
        self.listbox.delete(0, tk.END)  # Clear the Listbox
        search_term = self.search_var.get().lower()

        for index, row in self.combined_data.iterrows():
            display_text = f"{row['Mother_ID']} {row['Child_First_Name']} {row['Child_Last_Name']} (DOB: {row['Child_Date_of_Birth']})"
            
            # Only add the name if it matches the search term (or if the search term is empty)
            if search_term in display_text.lower():
                self.listbox.insert(tk.END, display_text)
        
        logging.info("Listbox updated with filtered names.")

    def search_combined_names(self):
        """
        Filter the combined names based on the search term.
        """
        logging.info(f"Searching names with term: {self.search_var.get()}")
        self.update_combined_names_listbox()

    def show_child_profile(self, event, listbox):
        """
        Show child profile when a name is double-clicked from the listbox.

        Args:
            event: The event that triggers the double-click.
            listbox: The listbox widget containing the combined names.
        """
        selected_index = listbox.curselection()
        if not selected_index:
            return  # If no selection, return

        # Get selected entry text
        selected_name = listbox.get(selected_index)

        # Extract the Mother ID and the child's full name from the selection
        selected_name_parts = selected_name.split(" ")
        mother_id = selected_name_parts[0]
        child_first_name = selected_name_parts[1]
        child_last_name = selected_name_parts[2]
        child_dob = selected_name_parts[-1].strip('()')  # Assuming the DOB is at the end

        # Query the child's profile from the combined data
        try:
            child_data = self.combined_data.loc[
                (self.combined_data['Mother_ID'].astype(str) == str(mother_id)) &
                (self.combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
                (self.combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
                (self.combined_data['Child_Date_of_Birth'] == child_dob)
            ]
            
            if child_data.empty:
                messagebox.showerror("Error", f"No data found for {child_first_name} {child_last_name}.")
                return

            # Get the first matching row
            child_data = child_data.iloc[0]

            # Show profile window
            profile_window = tk.Toplevel(self.root)
            profile_window.title(f"Profile of {child_first_name} {child_last_name}")

            # Create a frame for the profile layout
            profile_frame = tk.Frame(profile_window, padx=10, pady=10)
            profile_frame.pack(fill=tk.BOTH, expand=True)

            # Create a Text widget to display the profile information (copyable)
            text_widget = tk.Text(profile_frame, wrap=tk.WORD)
            text_widget.pack(fill=tk.BOTH, expand=True)

            # Insert Mother's information
            mother_info = f"Mother's Information\n" \
                        f"--------------------\n" \
                        f"Mother ID: {child_data['Mother_ID']}\n" \
                        f"Mother First Name: {child_data['Mother_First_Name']}\n" \
                        f"Mother Last Name: {child_data['Mother_Last_Name']}\n\n"
            text_widget.insert(tk.END, mother_info)

            # Insert Child's information
            child_info = f"Child's Information\n" \
                        f"-------------------\n" \
                        f"Child First Name: {child_data['Child_First_Name']}\n" \
                        f"Child Last Name: {child_data['Child_Last_Name']}\n" \
                        f"Child Date of Birth: {child_data['Child_Date_of_Birth']}\n\n"
            text_widget.insert(tk.END, child_info)

            # Insert Address and Contact Info if available
            if 'Street' in child_data and not pd.isnull(child_data['Street']):
                address_info = f"Address & Contact Information\n" \
                            f"-----------------------------\n" \
                            f"Street: {child_data['Street']}\n" \
                            f"City: {child_data['City']}\n" \
                            f"State: {child_data['State']}\n" \
                            f"ZIP: {child_data['ZIP']}\n" \
                            f"Phone #: {child_data['Phone_#']}\n" \
                            f"Mobile #: {child_data['Mobile_#']}\n"
                text_widget.insert(tk.END, address_info)

            # Make the text widget read-only
            text_widget.config(state=tk.DISABLED)

        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
