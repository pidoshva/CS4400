import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import logging
from invoker import ReadExcelCommand, CombineDataCommand, GenerateKeyCommand, DeleteFileCommand, EncryptFileCommand, DecryptFileCommand, Invoker
import tkinter.ttk as ttk  # for treeview
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from app_crypto import *

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    """
    The main application class for combining two Excel files.
    It handles user interactions for reading files, combining data, and displaying profiles.
    """
    def __init__(self, root):
        """
        Initialize the application with a root window and set up UI widgets.

        Preconditions:
            - `root` is a valid Tk root instance or None.
        Postconditions:
            - Application window and buttons are created and displayed.
        """
        if root is not None:
            self.__root = root
            self.__root.title("Excel Combiner")
            self.create_widgets()
        else:
            self.__root = None

        self._combined_data = None
        self.__data_frames = []

    def create_widgets(self):
        """
        Create and display the main UI components including buttons.

        Preconditions:
            - The root window is initialized.
        Postconditions:
            - Buttons for reading files, combining data, and loading existing data are created.
        """
        self.__root.geometry("500x300")
        self.__root.minsize(500, 300)

        button_frame = tk.Frame(self.__root, padx=20, pady=20)
        button_frame.pack(expand=True)

        self.read_button1 = tk.Button(button_frame, text="Read Excel File 1", command=self.read_excel_file, width=30, height=2)
        self.read_button1.pack(pady=10)

        self.read_button2 = tk.Button(button_frame, text="Read Excel File 2", command=self.read_excel_file, width=30, height=2)
        self.read_button2.pack(pady=10)

        self.combine_button = tk.Button(button_frame, text="Combine Data", command=self.combine_data, width=30, height=2)
        self.combine_button.pack(pady=10)

        self.upload_existing_button = tk.Button(button_frame, text="Load Existing File", command=self.load_combined_data, width=30, height=2)
        self.upload_existing_button.pack(pady=10)

        logging.info("UI widgets created.")

    def read_excel_file(self):
        """
        Read an Excel file chosen by the user and add its data to the data frames list.

        Preconditions:
            - User selects a valid Excel file.
        Postconditions:
            - Data from the selected file is appended to `__data_frames` if read successfully.
        """
        command = ReadExcelCommand(self)
        data_frame = command.execute()
        if data_frame is not None:
            self.__data_frames.append(data_frame)
            logging.info(f"Data from {command.filepath} successfully read and added to data frames.")
        else:
            logging.warning("No data frame returned from the file read.")
    
    def load_combined_data(self):
        """
        Load existing combined data from 'combined_matched_data.xlsx' if available and display it.

        Preconditions:
            - The file 'combined_matched_data.xlsx' exists in the current directory.
        Postconditions:
            - Combined data is loaded and displayed in the combined names view.
        """
        file_path = 'combined_matched_data.xlsx'
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "No combined data file found. Please combine data first.")
            logging.error("No combined data file found.")
            return

        try:
            # Load the existing combined data
            self.__combined_data = pd.read_excel(file_path)
            logging.info("Successfully loaded combined data from 'combined_matched_data.xlsx'")

            # Display the combined data
            self.show_combined_data()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load combined data file: {e}")
            logging.error(f"Failed to load combined data file: {e}")

    def combine_data(self):
        """
        Combine data from the two Excel files read by the user and display it.
        
        Preconditions:
            - At least two Excel files have been read and stored in __data_frames.
        Postconditions:
            - Combined data is created, saved to 'combined_matched_data.xlsx', and displayed.
        """
        if len(self.__data_frames) >= 2:
            logging.info("Attempting to combine data from two Excel files.")
            command = CombineDataCommand(self, self.__data_frames)
            combined_data = command.execute()

            if combined_data is not None:
                self.__combined_data = combined_data
                # Save combined data to an Excel file
                self.__combined_data.to_excel('combined_matched_data.xlsx', index=False)
                logging.info("Combined data saved to 'combined_matched_data.xlsx'")

                # Display the combined data
                self.show_combined_data()
            else:
                logging.error("Failed to combine data.")
        else:
            messagebox.showwarning("Warning", "Please read two Excel files first.")
            logging.warning("Attempted to combine data with less than two files.")

    def show_combined_data(self):
        """
        Display the combined data in a new window.
        
        Preconditions:
            - self.__combined_data is a valid DataFrame with required columns.
        Postconditions:
            - Combined data is displayed in a new Toplevel window.
        """
        if self.__combined_data is None or self.__combined_data.empty:
            messagebox.showerror("Error", "No data available to display.")
            logging.error("No data available to display.")
            return

        # Display logic here for the combined data
        self.display_combined_names()


    def display_combined_names(self):
        """
        Display combined data in a new Toplevel window with options for searching and viewing details.
        
        Preconditions:
            - `self.__combined_data` is a valid DataFrame with data to display.
        Postconditions:
            - A new window is opened with the combined data displayed in a Treeview.
        """
        combined_names_window = tk.Toplevel(self.__root)
        combined_names_window.title("Combined Data")

        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to exit this view?\nFiles must be uploaded to view the data again."):
                # matched_file_path = 'combined_matched_data.xlsx'
                # if os.path.exists(matched_file_path):
                #     os.remove(matched_file_path)
                #     logging.info(f"Deleted {matched_file_path}")

                # unmatched_file_path = 'unmatched_data.xlsx'
                # if os.path.exists(unmatched_file_path):
                #     os.remove(unmatched_file_path)
                #     logging.info(f"Deleted {unmatched_file_path}")

                # self.__data_frames.clear()
                # combined_names_window.destroy()
                # logging.info("Combined data window closed and files deleted.")
                combined_names_window.destroy()
                logging.info("Combined data window closed.")

        combined_names_window.protocol("WM_DELETE_WINDOW", on_closing)

        combined_names_window.geometry("1000x600")
        combined_names_window.minsize(800, 400)
        combined_names_window.resizable(True, True)

        search_frame = tk.Frame(combined_names_window)
        search_frame.pack(fill=tk.X, pady=5)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)

        search_button = tk.Button(search_frame, text="Search", command=self.search_combined_names)
        search_button.pack(side=tk.RIGHT, padx=10)

        nurse_stats_button = tk.Button(combined_names_window, text="Nurse Statistics", command=self.show_nurse_statistics)
        nurse_stats_button.pack(pady=10)

        columns = ("Mother ID", "Child Name", "Child DOB", "Assigned Nurse")
        self.treeview = ttk.Treeview(combined_names_window, columns=columns, show='headings')

        tree_scroll = tk.Scrollbar(self.treeview, command=self.treeview.yview)
        tree_scroll.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=tree_scroll.set)

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, anchor="center", width=150)

        if 'Assigned Nurse' not in self.__combined_data.columns:
            self.__combined_data['Assigned Nurse'] = 'None'

        self.update_combined_names()
        self.__combined_data.to_excel('combined_matched_data.xlsx', index=False)

        self.treeview.pack(fill=tk.BOTH, expand=True)
        self.treeview.bind('<Double-1>', lambda event: self.show_child_profile(event))

        display_excel_button = tk.Button(combined_names_window, text="Display in Excel", command=self.display_in_excel)
        display_excel_button.pack(pady=10)

        unmatched_data_path = 'unmatched_data.xlsx'
        if os.path.exists(unmatched_data_path):
            unmatched_data = pd.read_excel(unmatched_data_path)
            unmatched_count = len(unmatched_data)
            if unmatched_count > 0:
                unmatched_button = tk.Button(
                    combined_names_window,
                    text="View Unmatched Data",
                    command=lambda: self.display_unmatched_data(unmatched_data)
                )
                unmatched_button.pack(pady=10)
                count_label = tk.Label(unmatched_button, text=str(unmatched_count), bg="red", fg="white", font=("Arial", 10, "bold"))
                count_label.place(relx=1.0, rely=0.0, anchor="ne")

        combined_names_window.mainloop()

    def encrypt_files(self):
        logging.info("Attempting to encrypt file.")

        if not os.path.exists("key.txt"):
            messagebox.showwarning("Error!", "Key does not exist")
        else:
            command = EncryptFileCommand(self) 
            result = command.execute()
            if result:
                messagebox.showinfo("Success", "Encryption Successfull.")
            else:
                messagebox.showerror("Error", "Encryption Unsuccessfull")

    def decrypt_file(self):
        logging.info("Attempting to decrypt file.")

        if not os.path.exists("key.txt"):
            messagebox.showwarning("Error!", "Key does not exist")
        else:
            command = DecryptFileCommand(self) 
            result = command.execute()
            if result:
                messagebox.showinfo("Success", "Decryption Successfull.")
            else:
                messagebox.showerror("Error", "Decryption Unsuccessfull")

    def generate_encryption_key(self):
        command = GenerateKeyCommand(self)
        logging.info("Attempting to generate key.")

        if not os.path.exists("key.txt") or os.stat("key.txt").st_size <= 0:
            command.execute()
            messagebox.showinfo("Success", "Key generated.")
        else:
            logging.warning("Key already exists")
            messagebox.showerror("Error", "To generate a new key, delete previous key.")

    def delete_encryption_key(self):
        logging.info("Attempting to delte key.")
        answer = messagebox.askquestion("WARNING!", "Are you sure you want to proceed? Any file encrypted with this key will become permanently unusable.")
        if answer == 'no':
            logging.info("Action aborted.")
            return
        command = DeleteFileCommand(self)
        if os.path.exists("key.txt"):
            command.execute("key.txt")
            logging.info("Key successfully deleted.")
            messagebox.showinfo("Success", "Key successfully deleted.")
        else:
            logging.warning("Key does not exist.")
            messagebox.showerror("Error", "No key exists.")

    def update_combined_names(self):
        """
        Update the Treeview with the combined data based on the current search term.
        
        Preconditions:
            - `self.__combined_data` contains data to display.
        Postconditions:
            - Treeview is populated with combined data entries that match the search term.
        """
        self.treeview.delete(*self.treeview.get_children())
        search_term = self.search_var.get().lower()
        for index, row in self.__combined_data.iterrows():
            child_name = f"{row['Child_First_Name']} {row['Child_Last_Name']}"
            assigned_nurse = row.get('Assigned Nurse', 'None')
            if search_term in f"{row['Mother_ID']} {child_name}".lower():
                self.treeview.insert("", "end", values=(row['Mother_ID'], child_name, row['Child_Date_of_Birth'], assigned_nurse))

        logging.info("Treeview updated with filtered names.")

    def show_nurse_statistics(self):
        """
        Display statistics on nurse assignments from the combined data.
        
        Preconditions:
            - 'combined_matched_data.xlsx' exists and contains valid nurse assignment data.
        Postconditions:
            - A new window is opened displaying statistics on most and least assigned nurses.
        """
        try:
            if os.path.exists('combined_matched_data.xlsx'):
                self._combined_data = pd.read_excel('combined_matched_data.xlsx')
                logging.info("Successfully reloaded the combined data for statistics.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload combined data: {e}")
            logging.error(f"Failed to reload combined data: {e}")
            return

        if self._combined_data is None or 'Assigned Nurse' not in self._combined_data.columns:
            messagebox.showwarning("No Data", "Nurse statistics could not be displayed because the data is not available or not combined.")
            logging.error("Nurse statistics could not be displayed because the data is not available or not combined.")
            return

        nurse_counts = self._combined_data['Assigned Nurse'].value_counts()
        nurse_counts = nurse_counts[nurse_counts.index != 'None']

        if nurse_counts.empty:
            messagebox.showinfo("No Nurse Data", "No nurse assignment data to display statistics.")
            logging.info("No nurse assignment data available for statistics.")
            return

        most_assigned_nurse = nurse_counts.idxmax()
        most_assigned_count = nurse_counts.max()
        least_assigned_nurse = nurse_counts.idxmin()
        least_assigned_count = nurse_counts.min()

        stats_window = tk.Toplevel(self.__root)
        stats_window.title("Nurse Statistics")
        stats_window.geometry("400x400")

        tk.Label(
            stats_window,
            text=f"Most Assigned Nurse: {most_assigned_nurse} ({most_assigned_count} assignments)",
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Label(
            stats_window,
            text=f"Least Assigned Nurse: {least_assigned_nurse} ({least_assigned_count} assignments)",
            font=("Arial", 12)
        ).pack(pady=5)

        tk.Label(stats_window, text="Assignments by Nurse Name:", font=("Arial", 12, "bold")).pack(pady=5)

        # Function to display children assigned to the selected nurse
        def show_children_for_nurse(nurse_name):
            assigned_children = self._combined_data[self._combined_data['Assigned Nurse'] == nurse_name]
            children_window = tk.Toplevel(stats_window)
            children_window.title(f"Children assigned to {nurse_name}")
            children_window.geometry("500x700")

            tk.Label(children_window, text=f"Children assigned to {nurse_name}:", font=("Arial", 12, "bold")).pack(pady=5)

            # Treeview to display child names and DOB
            tree = ttk.Treeview(children_window, columns=("Name", "DOB"), show="headings")
            tree.heading("Name", text="Child's Name")
            tree.heading("DOB", text="Date of Birth")
            tree.pack(fill=tk.BOTH, expand=True)

            # Populate tree with children data
            for _, row in assigned_children.iterrows():
                child_name = f"{row['Child_First_Name']} {row['Child_Last_Name']}"
                tree.insert("", "end", values=(child_name, row['Child_Date_of_Birth']))

             # Bind double-click to show profile
            def on_child_double_click(event):
                selected_item = tree.selection()
                if selected_item:
                    item_data = tree.item(selected_item)["values"]
                    child_name = item_data[0]
                    child_dob = item_data[1]

                    # Locate the child's data in the combined DataFrame
                    child_data = self._combined_data[
                        (self._combined_data['Child_First_Name'] + " " + self._combined_data['Child_Last_Name'] == child_name) &
                        (self._combined_data['Child_Date_of_Birth'] == child_dob)
                    ]

                    if not child_data.empty:
                        self.show_child_profile_from_data(child_data.iloc[0])

            tree.bind("<Double-1>", on_child_double_click)

        for nurse, count in nurse_counts.items():
            nurse_label = tk.Label(stats_window, text=f"{nurse}: {count} assignments", font=("Arial", 10), cursor="hand2")
            nurse_label.pack(anchor="w")
            nurse_label.bind("<Button-1>", lambda e, nurse=nurse: show_children_for_nurse(nurse))

        logging.info("Nurse statistics displayed successfully.")

    def show_child_profile_from_data(self, child_data):
        """
        Display detailed profile for a selected child from the data.
        
        Preconditions:
            - `child_data` contains a valid row of child information from `self._combined_data`.
        Postconditions:
            - A new window is opened displaying the child’s detailed profile.
        """
        profile_window = tk.Toplevel(self.__root)
        profile_window.title(f"Profile of {child_data['Child_First_Name']} {child_data['Child_Last_Name']}")

        profile_frame = tk.Frame(profile_window, padx=10, pady=10)
        profile_frame.pack(fill=tk.BOTH, expand=True)

        mother_info_label = tk.Label(profile_frame, text="Mother's Information", font=("Arial", 14, "bold"))
        mother_info_label.pack(anchor='w', pady=(10, 0))

        mother_info_text = f"Mother ID: {child_data['Mother_ID']}\n" \
                        f"First Name: {child_data['Mother_First_Name']}\n" \
                        f"Last Name: {child_data['Mother_Last_Name']}\n"

        tk.Label(profile_frame, text=mother_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12)).pack(anchor='w', pady=(5, 10))

        child_info_label = tk.Label(profile_frame, text="Child's Information", font=("Arial", 14, "bold"))
        child_info_label.pack(anchor='w', pady=(10, 0))

        child_info_text = f"First Name: {child_data['Child_First_Name']}\n" \
                        f"Last Name: {child_data['Child_Last_Name']}\n" \
                        f"Date of Birth: {child_data['Child_Date_of_Birth']}\n"

        tk.Label(profile_frame, text=child_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12)).pack(anchor='w', pady=(5, 10))

        if 'Street' in child_data and not pd.isnull(child_data['Street']):
            address_info_label = tk.Label(profile_frame, text="Address & Contact Information", font=("Arial", 14, "bold"))
            address_info_label.pack(anchor='w', pady=(10, 0))

            address_info_text = f"Street: {child_data['Street']}\n" \
                                f"City: {child_data['City']}\n" \
                                f"State: {child_data['State']}\n" \
                                f"ZIP: {child_data['ZIP']}\n" \
                                f"Phone #: {child_data['Phone_#']}\n" \
                                f"Mobile #: {child_data['Mobile_#']}\n"

            tk.Label(profile_frame, text=address_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12)).pack(anchor='w', pady=(5, 10))

        nurse_info_label = tk.Label(profile_frame, text="Assigned Nurse", font=("Arial", 14, "bold"))
        nurse_info_label.pack(anchor='w', pady=(10, 0))

        assigned_nurse = child_data['Assigned Nurse'] if pd.notna(child_data['Assigned Nurse']) else 'None'
        nurse_info_text = f"Name: {assigned_nurse}"

        tk.Label(profile_frame, text=nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12)).pack(anchor='w', pady=(5, 10))

        copy_button = tk.Button(profile_frame, text="Copy Profile Info", command=lambda: self.copy_to_clipboard(mother_info_text, child_info_text, address_info_text))
        copy_button.pack(pady=(10, 5))

        export_button = tk.Button(profile_frame, text="Export to PDF", command=lambda: self.export_profile_to_pdf(mother_info_text, child_info_text, address_info_text, nurse_info_text))
        export_button.pack(pady=(10, 5))

        logging.info(f"Profile for {child_data['Child_First_Name']} {child_data['Child_Last_Name']} displayed successfully.")

    def display_unmatched_data(self, unmatched_data):
        """
        Display a new window with the unmatched data in a Treeview.

        Preconditions:
            - `unmatched_data` is a DataFrame containing unmatched entries.
        Postconditions:
            - A new window is opened, displaying the unmatched data in a Treeview.
            - Each unmatched entry is displayed in the primary columns, with additional details expandable.
        """
        logging.info("Opening unmatched data window.")

        unmatched_data_window = tk.Toplevel(self.__root)
        unmatched_data_window.title("Unmatched Data")
        unmatched_data_window.geometry("800x400")

        # Define primary columns to show initially
        primary_columns = ["Source", "Child_ID", "Mother_First_Name", "Mother_Last_Name"]
        all_columns = list(unmatched_data.columns)

        # Create the Treeview widget with primary columns
        treeview = ttk.Treeview(unmatched_data_window, columns=primary_columns, show="headings")
        treeview.pack(fill=tk.BOTH, expand=True)

        # Configure the headings and column widths for primary columns
        for col in primary_columns:
            treeview.heading(col, text=col)
            treeview.column(col, anchor="center", width=150)

        # Dictionary to store whether a row is expanded or collapsed
        expanded_rows = {}

        # Insert the unmatched data into the Treeview with only primary columns initially
        for index, row in unmatched_data.iterrows():
            # Extract primary column values for the main row
            main_values = [row.get(col, "") for col in primary_columns]
            row_id = treeview.insert("", "end", values=main_values, open=False)
            logging.info(f"Inserted unmatched row with ID {row_id} and data: {main_values}")
            
            # Prepare additional information as separate rows under the main row
            additional_info_rows = []
            for col in all_columns:
                if col not in primary_columns:
                    additional_info_rows.append(f"{col}: {row.get(col, '')}")
            
            # Store the additional rows data in a hidden structure under each main row
            expanded_rows[row_id] = {
                "expanded": False,
                "details": additional_info_rows
            }

        def toggle_expand(event):
            """
            Toggle displaying additional information for the clicked row.

            Preconditions:
                - The Treeview item is selected.
            Postconditions:
                - Additional details for the selected row are displayed or hidden.
            """
            selected_items = treeview.selection()
            if not selected_items:
                logging.warning("No row selected for expansion/collapse.")
                return

            selected_item = selected_items[0]
            row_data = expanded_rows.get(selected_item, {})
            is_expanded = row_data.get("expanded", False)

            if not is_expanded:
                detail_items = []
                for detail in row_data["details"]:
                    detail_item = treeview.insert(selected_item, "end", values=[detail], tags=("additional",))
                    detail_items.append(detail_item)
                row_data["expanded"] = True
                row_data["detail_items"] = detail_items  # Store detail items for future collapse
                logging.info(f"Expanded row with ID {selected_item} to show details.")
            else:
                for child in row_data.get("detail_items", []):
                    treeview.delete(child)
                row_data["expanded"] = False
                row_data["detail_items"] = []
                logging.info(f"Collapsed row with ID {selected_item} to hide details.")

            expanded_rows[selected_item] = row_data  # Update the expanded_rows dictionary

        # Bind the double-click event to expand/collapse rows
        treeview.bind("<Double-1>", toggle_expand)

        # Style the additional information rows for readability
        treeview.tag_configure("additional", background="#962f2f", font=("Arial", 10, "italic"))

        # Button to view the unmatched data in Excel
        def view_in_excel():
            try:
                unmatched_file_path = 'unmatched_data.xlsx'
                if os.path.exists(unmatched_file_path):
                    os.system(f"open {unmatched_file_path}")
                    logging.info("Opened unmatched data in Excel.")
                else:
                    messagebox.showerror("Error", "The unmatched data file does not exist.")
                    logging.error("The unmatched data file does not exist.")
            except Exception as e:
                messagebox.showerror("Error", f"Error opening unmatched data Excel file: {e}")
                logging.error(f"Error opening unmatched data Excel file: {e}")

        view_excel_button = tk.Button(unmatched_data_window, text="View in Excel", command=view_in_excel)
        view_excel_button.pack(pady=10)

        logging.info("Unmatched data window initialized and ready for user interaction.")
        unmatched_data_window.mainloop()

    def search_combined_names(self):
        """
        Initiates a search operation for the combined data based on user input.

        Preconditions:
            - `self.search_var` is a valid StringVar that contains the search term entered by the user.
            - `self.update_combined_names` function is defined to filter and display the search results in the Treeview.
        Postconditions:
            - Logs the search term used.
            - Triggers an update in the Treeview to display filtered names based on the search term.
        """
        logging.info(f"Searching names with term: {self.search_var.get()}")
        self.update_combined_names()

    def show_child_profile(self, event):
        """
        Show child profile when a name is double-clicked from the Treeview.

        Preconditions:
            - A row in the Treeview is selected, containing valid child profile data.
        Postconditions:
            - Opens a new window displaying detailed profile information for the selected child.
        """
        selected_item = self.treeview.selection()
        if not selected_item:
            logging.warning("No profile selected for viewing.")
            return  # If no selection, return

        # Get selected entry values
        selected_values = self.treeview.item(selected_item, 'values')

        # Extract the Mother ID and the child's full name from the selection
        mother_id = selected_values[0]
        child_name_parts = selected_values[1].split()
        child_first_name = child_name_parts[0]
        child_last_name = child_name_parts[1]
        child_dob = selected_values[2]

        logging.info(f"Viewing profile for Mother ID: {mother_id}, Child: {child_first_name} {child_last_name}, DOB: {child_dob}")

        # Query the child's profile from the combined data
        try:
            child_data = self.__combined_data.loc[
                (self.__combined_data['Mother_ID'].astype(str) == str(mother_id)) &
                (self.__combined_data['Child_First_Name'].str.lower() == child_first_name.lower()) &
                (self.__combined_data['Child_Last_Name'].str.lower() == child_last_name.lower()) &
                (self.__combined_data['Child_Date_of_Birth'] == child_dob)
            ]

            if child_data.empty:
                messagebox.showerror("Error", f"No data found for {child_first_name} {child_last_name}.")
                logging.error(f"No data found for Mother ID: {mother_id}, Child: {child_first_name} {child_last_name}, DOB: {child_dob}")
                return

            # Get the first matching row
            child_data = child_data.iloc[0]

            # Show profile window
            profile_window = tk.Toplevel(self.__root)
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

            # Display assigned nurse as a separate section
            nurse_info_label = tk.Label(profile_frame, text="Assigned Nurse", font=("Arial", 14, "bold"))
            nurse_info_label.pack(anchor='w', pady=(10, 0))

            assigned_nurse = child_data['Assigned Nurse'] if pd.notna(child_data['Assigned Nurse']) else 'None'
            nurse_info_text = f"Name: {assigned_nurse}"

            nurse_info = tk.Label(profile_frame, text=nurse_info_text, anchor='w', justify=tk.LEFT, font=("Arial", 12))
            nurse_info.pack(anchor='w', pady=(5, 10))

            # Add "Assign Nurse" button with functionality
            assign_nurse_button = tk.Button(profile_frame, text="Assign Nurse", command=lambda: self.assign_nurse(child_data, profile_window, nurse_info))
            assign_nurse_button.pack(pady=(10, 5))

            # Option to copy text to clipboard
            copy_button = tk.Button(profile_frame, text="Copy Profile Info", command=lambda: self.copy_to_clipboard(mother_info_text, child_info_text, address_info_text))
            copy_button.pack(pady=(10, 5))

            # Button to export the profile information to PDF
            export_button = tk.Button(profile_frame, text="Export to PDF", command=lambda: self.export_profile_to_pdf(mother_info_text, child_info.cget("text"), address_info_text, nurse_info.cget("text")))
            export_button.pack(pady=(10, 5))

            logging.info(f"Profile for {child_first_name} {child_last_name} displayed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")
            logging.error(f"Error loading profile for {child_first_name} {child_last_name}: {e}")

    def assign_nurse(self, child_data, profile_window, nurse_info_label):
        """
        Open a window to assign a nurse to the selected child.

        Preconditions:
            - `child_data` contains valid data about the selected child.
            - `profile_window` is the window displaying the child’s profile.
            - `nurse_info_label` is a Label widget displaying the currently assigned nurse.
        Postconditions:
            - Opens a dialog to input a nurse’s name.
            - Updates the assigned nurse for the child in the combined data and reflects it in the profile display and Excel file.
        """
        assign_window = tk.Toplevel(profile_window)
        assign_window.title(f"Assign Nurse to {child_data['Child_First_Name']} {child_data['Child_Last_Name']}")
        assign_window.geometry("300x150")

        tk.Label(assign_window, text="Enter Nurse Name:").pack(pady=5)
        nurse_name_var = tk.StringVar()
        nurse_entry = tk.Entry(assign_window, textvariable=nurse_name_var)
        nurse_entry.pack(pady=5)

        def save_nurse():
            """
            Saves the assigned nurse to the child's profile.

            Preconditions:
                - `nurse_name_var` contains a non-empty string with the nurse’s name.
            Postconditions:
                - The nurse’s name is saved to `__combined_data` for the child.
                - The nurse name is updated in the profile display and saved to the Excel file.
            """
            nurse_name = nurse_name_var.get().strip()
            if nurse_name:
                # Update combined data DataFrame
                index = self.__combined_data[
                    (self.__combined_data['Mother_ID'].astype(str) == str(child_data['Mother_ID'])) &
                    (self.__combined_data['Child_First_Name'].str.lower() == child_data['Child_First_Name'].lower()) &
                    (self.__combined_data['Child_Last_Name'].str.lower() == child_data['Child_Last_Name'].lower()) &
                    (self.__combined_data['Child_Date_of_Birth'] == child_data['Child_Date_of_Birth'])
                ].index

                if not index.empty:
                    self.__combined_data.at[index[0], 'Assigned Nurse'] = nurse_name

                    # Update the Excel file
                    self.__combined_data.to_excel('combined_matched_data.xlsx', index=False)
                    logging.info(f"Assigned Nurse '{nurse_name}' to {child_data['Child_First_Name']} {child_data['Child_Last_Name']}.")

                    # Update the nurse section in the profile display
                    updated_nurse_text = f"Name: {nurse_name}"
                    nurse_info_label.config(text=updated_nurse_text)

                    # Update the Treeview display
                    self.update_combined_names()

                    messagebox.showinfo("Success", f"Nurse '{nurse_name}' assigned successfully.")
                    assign_window.destroy()
                else:
                    logging.error("Error finding the row to update nurse assignment.")
                    messagebox.showerror("Error", "Failed to assign nurse.")

        tk.Button(assign_window, text="Add", command=save_nurse).pack(pady=10)

    def copy_to_clipboard(self, mother_info_text, child_info_text, address_info_text=None):
        """
        Copies the provided profile information to the clipboard.

        Preconditions:
            - `mother_info_text` and `child_info_text` contain valid strings.
            - `address_info_text` may be None if address details are unavailable.
        Postconditions:
            - Profile information is copied to the clipboard and a confirmation message is shown.
        """
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

        self.__root.clipboard_clear()
        self.__root.clipboard_append(copied_text)
        messagebox.showinfo("Info", "Profile info copied to clipboard.")
        logging.info("Profile info successfully copied to clipboard.")

    def export_profile_to_pdf(self, mother_info_text, child_info_text, address_info_text=None, nurse_info_text=None):
        """
        Exports profile information to a structured PDF document.

        Preconditions:
            - `mother_info_text` and `child_info_text` contain valid profile details.
            - `address_info_text` and `nurse_info_text` are optional and may be None.
        Postconditions:
            - A PDF with profile information is generated and opened in the default viewer.
        """
        try:
            # Create a temporary file for the PDF
            pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            c = canvas.Canvas(pdf_file.name, pagesize=letter)

            # PDF Title and document layout settings
            c.setFont("Helvetica-Bold", 14)
            c.drawString(1 * inch, 10.5 * inch, "Profile Information")
            c.line(1 * inch, 10.45 * inch, 7.5 * inch, 10.45 * inch)
            c.setFont("Helvetica", 10)
            y = 10.2 * inch  # Start position

            # Function to draw a section header
            def draw_section_header(title, ypos):
                c.setFont("Helvetica-Bold", 12)
                c.setFillColor(colors.darkblue)
                c.drawString(1 * inch, ypos, title)
                c.setFillColor(colors.black)
                c.line(1 * inch, ypos - 2, 7.5 * inch, ypos - 2)
                return ypos - 14

            # Draw "Mother's Information" section
            y = draw_section_header("Mother's Information", y)
            c.setFont("Helvetica", 10)
            for line in mother_info_text.strip().split('\n'):
                c.drawString(1.2 * inch, y, line)
                y -= 12

            # Draw "Child's Information" section
            y = draw_section_header("Child's Information", y - 10)
            for line in child_info_text.strip().split('\n'):
                c.drawString(1.2 * inch, y, line)
                y -= 12

            # Draw "Address & Contact Information" section if available
            if address_info_text:
                y = draw_section_header("Address & Contact Information", y - 10)
                for line in address_info_text.strip().split('\n'):
                    c.drawString(1.2 * inch, y, line)
                    y -= 12

            # Draw "Assigned Nurse" section if available
            if nurse_info_text:
                y = draw_section_header("Assigned Nurse", y - 10)
                c.drawString(1.2 * inch, y, nurse_info_text)
                y -= 12

            # Save and close PDF
            c.save()

            # Open the generated PDF
            os.system(f"open {pdf_file.name}")
            logging.info(f"Profile exported to PDF: {pdf_file.name}")

        except Exception as e:
            messagebox.showerror("Error", f"Error exporting profile: {e}")
            logging.error(f"Error exporting profile to PDF: {e}")

    def display_in_excel(self):
        """
        Open the combined data Excel file in the default Excel application.

        Preconditions:
            - 'combined_matched_data.xlsx' exists in the current directory.
        Postconditions:
            - The Excel file opens in the default application if available.
        """
        try:
            if os.path.exists('combined_matched_data.xlsx'):
                # Check the OS and use the appropriate command
                if platform.system() == "Darwin":  # macOS
                    os.system("open combined_matched_data.xlsx")
                elif platform.system() == "Windows":
                    os.startfile("combined_matched_data.xlsx")
                else:  # For Linux or other OS
                    os.system("xdg-open combined_matched_data.xlsx")
                
                logging.info("Opened combined data in Excel.")
            else:
                messagebox.showerror("Error", "The combined data file does not exist.")
                logging.error("The combined data file does not exist.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening Excel file: {e}")
            logging.error(f"Error opening Excel file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

