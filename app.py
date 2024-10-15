import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import logging
from invoker import ReadExcelCommand, CombineDataCommand, Invoker
import tkinter.ttk as ttk  # for treeview

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
        using a Treeview for better data organization and readability.
        """
        combined_names_window = tk.Toplevel(self.root)
        combined_names_window.title("Combined Data")

        logging.info("Displaying combined names window.")

        # Set the window size and allow resizing
        combined_names_window.geometry("1000x600")  # Set initial window size
        combined_names_window.minsize(800, 400)  # Set minimum window size
        combined_names_window.resizable(True, True)  # Allow both horizontal and vertical resizing

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

        # Create a Treeview widget to display the data in columns
        columns = ("Mother ID", "Child Name", "Child DOB")
        self.treeview = ttk.Treeview(combined_names_window, columns=columns, show='headings')

        # Define headings and column widths
        self.treeview.heading("Mother ID", text="Mother ID")
        self.treeview.heading("Child Name", text="Child Name")
        self.treeview.heading("Child DOB", text="Child DOB")
        
        self.treeview.column("Mother ID", width=150, anchor="center")
        self.treeview.column("Child Name", width=250, anchor="center")
        self.treeview.column("Child DOB", width=150, anchor="center")

        # Populate the treeview with the combined data
        self.update_combined_names()

        # Add the treeview to the window and make it fill the available space
        self.treeview.pack(fill=tk.BOTH, expand=True)

        # Bind double-click event to open child profile
        self.treeview.bind('<Double-1>', lambda event: self.show_child_profile(event))

    def update_combined_names(self):
        """
        Update the Treeview with combined names (Mother ID, Child Name, DOB), 
        filtering the results based on the search term.
        """
        # Clear the current contents of the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Get the search term for filtering
        search_term = self.search_var.get().lower()

        # Populate the treeview with matching data
        for index, row in self.combined_data.iterrows():
            child_name = f"{row['Child_First_Name']} {row['Child_Last_Name']}"
            display_text = f"{row['Mother_ID']} {child_name} (DOB: {row['Child_Date_of_Birth']})"

            # Only add the row if it matches the search term or if no search term is provided
            if search_term in display_text.lower():
                self.treeview.insert("", "end", values=(row['Mother_ID'], child_name, row['Child_Date_of_Birth']))

        logging.info("Treeview updated with filtered names.")

    def search_combined_names(self):
        """
        Filter the combined names based on the search term.
        """
        logging.info(f"Searching names with term: {self.search_var.get()}")
        self.update_combined_names()

    def show_child_profile(self, event):
        """
        Show child profile when a name is double-clicked from the Treeview.

        Args:
            event: The event that triggers the double-click.
        """
        selected_item = self.treeview.selection()
        if not selected_item:
            return  # If no selection, return

        # Get selected entry values
        selected_values = self.treeview.item(selected_item, 'values')

        # Extract the Mother ID and the child's full name from the selection
        mother_id = selected_values[0]
        child_name_parts = selected_values[1].split()
        child_first_name = child_name_parts[0]
        child_last_name = child_name_parts[1]
        child_dob = selected_values[2]

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

            # Group headers and display information
            mother_info_label = tk.Label(profile_frame, text="Mother's Information", font=("Arial", 14, "bold"))
            mother_info_label.pack(anchor='w', pady=(10, 0))

            mother_info_text = f"Mother ID: {child_data['Mother_ID']}\n" \
                            f"First Name: {child_data['Mother_First_Name']}\n" \
                            f"Last Name: {child_data['Mother_Last_Name']}\n"

            mother_info = tk.Label(profile_frame, text=mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
            mother_info.pack(anchor='w', pady=(5, 10))

            child_info_label = tk.Label(profile_frame, text="Child's Information", font=("Arial", 14, "bold"))
            child_info_label.pack(anchor='w', pady=(10, 0))

            child_info_text = f"First Name: {child_data['Child_First_Name']}\n" \
                            f"Last Name: {child_data['Child_Last_Name']}\n" \
                            f"Date of Birth: {child_data['Child_Date_of_Birth']}\n"

            child_info = tk.Label(profile_frame, text=child_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
            child_info.pack(anchor='w', pady=(5, 10))

            # Check for and display address if available
            address_info_text = None
            if 'Street' in child_data and not pd.isnull(child_data['Street']):
                address_info_label = tk.Label(profile_frame, text="Address & Contact Information", font=("Arial", 14, "bold"))
                address_info_label.pack(anchor='w', pady=(10, 0))

                address_info_text = f"Street: {child_data['Street']}\n" \
                                    f"City: {child_data['City']}\n" \
                                    f"State: {child_data['State']}\n" \
                                    f"ZIP: {child_data['ZIP']}\n" \
                                    f"Phone #: {child_data['Phone_#']}\n" \
                                    f"Mobile #: {child_data['Mobile_#']}\n"

                address_info = tk.Label(profile_frame, text=address_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
                address_info.pack(anchor='w', pady=(5, 10))

            # Option to copy text to clipboard
            copy_button = tk.Button(profile_frame, text="Copy Profile Info", command=lambda: self.copy_to_clipboard(mother_info_text, child_info_text, address_info_text))
            copy_button.pack(pady=(10, 5))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")
            logging.error(f"Error loading profile: {e}")


    def copy_to_clipboard(self, mother_info_text, child_info_text, address_info_text=None):
        """
        Copies the given text to the clipboard, formatted for better readability.
        
        Args:
            mother_info_text (str): Mother's information to be copied.
            child_info_text (str): Child's information to be copied.
            address_info_text (str, optional): Address and contact information to be copied.
        """
        # Organize the sections of the profile for copying
        copied_text = (
            f"--- Mother's Information ---\n"
            f"{mother_info_text}\n"
            f"--- Child's Information ---\n"
            f"{child_info_text}\n"
        )

        if address_info_text:
            copied_text += (
                f"--- Address & Contact Information ---\n"
                f"{address_info_text}"
            )

        # Clear the clipboard and append the formatted text
        self.root.clipboard_clear()
        self.root.clipboard_append(copied_text)
        messagebox.showinfo("Info", "Profile info copied to clipboard.")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

