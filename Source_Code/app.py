import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import logging
from invoker import ReadExcelCommand, CombineDataCommand, GenerateKeyCommand, DeleteFileCommand, Invoker
import tkinter.ttk as ttk  # for treeview
import os
import subprocess
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
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
        Initialize the main application, setup the UI, and initialize variables.
        """
        if root is not None:  # Only setup UI if root is provided
            self.__root = root
            self.__root.title("Excel Combiner")
            # Create UI elements
            self.create_widgets()
        else:
            self.__root = None

        self._combined_data = None
        self.__data_frames = []

    def create_widgets(self):
        """
        Create the UI elements including buttons to read Excel files, combine data, and display profiles.
        """
        # Set the initial size of the root window
        self.__root.geometry("500x500")  # Set the window size to 500x500
        self.__root.minsize(500, 500)  # Ensure the window does not resize smaller than this

        # Frame to hold the buttons and center them
        button_frame = tk.Frame(self.__root, padx=20, pady=20)
        button_frame.pack(expand=True)  # Add padding to make the UI more spacious

        # Buttons for reading two Excel files
        self.read_button1 = tk.Button(button_frame, text="Read Excel File 1", command=self.read_excel_file, width=30, height=2)
        self.read_button1.pack(pady=10)  # Add padding between buttons

        self.read_button2 = tk.Button(button_frame, text="Read Excel File 2", command=self.read_excel_file, width=30, height=2)
        self.read_button2.pack(pady=10)

        # Button to combine the data
        self.combine_button = tk.Button(button_frame, text="Combine Data", command=self.combine_data, width=30, height=2)
        self.combine_button.pack(pady=10)

        # Button to encrypt files
        self.combine_button = tk.Button(button_frame, text="Encrypt File", command=self.encrypt_files, width=30, height=2)
        self.combine_button.pack(pady=10)

        # Button to create encryption key
        self.combine_button = tk.Button(button_frame, text="Generate Encryption Key", command=self.generate_encryption_key, width=30, height=2)
        self.combine_button.pack(pady=10)

        # Button to delete encryption key
        self.combine_button = tk.Button(button_frame, text="Delete Encryption Key", command=self.delete_encryption_key, width=30, height=2)
        self.combine_button.pack(pady=10)

        logging.info("UI widgets created.")

    def read_excel_file(self):
        """
        Read an Excel file and append its data to the list of data frames.
        """
        command = ReadExcelCommand(self)
        data_frame = command.execute()
        if data_frame is not None:
            self.__data_frames.append(data_frame)
            logging.info(f"Data from {command.filepath} successfully read and added to data frames.")
        else:
            logging.warning("No data frame returned from the file read.")

    def combine_data(self):
        """
        Combine the two read Excel files and display the combined names.
        """
        if len(self.__data_frames) >= 2:
            logging.info("Attempting to combine data from two Excel files.")
            command = CombineDataCommand(self, self.__data_frames)
            combined_data = command.execute()

            if combined_data is not None:
                # Store combined data in app
                self.__combined_data = combined_data
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
        combined_names_window = tk.Toplevel(self.__root)
        combined_names_window.title("Combined Data")

        """
        Inner function that describes the event of closing the combined_names_window
        """
        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to exit this view?\nFiles must be uploaded to view the data again."):
                combined_names_window.destroy()
                self.__data_frames.clear()
                print(self.__data_frames)

        combined_names_window.protocol("WM_DELETE_WINDOW", on_closing)

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

        # Create a scrollbar widget
        tree_scroll = tk.Scrollbar(self.treeview, command=self.treeview.yview)
        tree_scroll.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=tree_scroll.set)

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

        # Button to display combined data in Excel
        display_excel_button = tk.Button(combined_names_window, text="Display in Excel", command=self.display_in_excel)
        display_excel_button.pack(pady=10)

        combined_names_window.mainloop()

    def encrypt_files(self):
        pass

    def generate_encryption_key(self):
        command = GenerateKeyCommand(self)
        logging.info("Attempting to generate key.")

        if not os.path.exists("key.key") or os.stat("key.key").st_size <= 0:
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
        if os.path.exists("key.key"):
            command.execute("key.key")
            logging.info("Key successfully deleted.")
            messagebox.showinfo("Success", "Key successfully deleted.")
        else:
            logging.warning("Key does not exist.")
            messagebox.showerror("Error", "No key exists.")

    def encrypt_file(self):
        pass

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
        for index, row in self.__combined_data.iterrows():
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

            # Option to copy text to clipboard
            copy_button = tk.Button(profile_frame, text="Copy Profile Info", command=lambda: self.copy_to_clipboard(mother_info_text, child_info_text, address_info_text))
            copy_button.pack(pady=(10, 5))

            # Button to export the profile information to PDF
            export_button = tk.Button(profile_frame, text="Export to PDF", command=lambda: self.export_profile_to_pdf(mother_info_text, child_info_text, address_info_text))
            export_button.pack(pady=(10, 5))

            logging.info(f"Profile for {child_first_name} {child_last_name} displayed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")
            logging.error(f"Error loading profile for {child_first_name} {child_last_name}: {e}")

    def copy_to_clipboard(self, mother_info_text, child_info_text, address_info_text=None):
        """
        Copies the given text to the clipboard, formatted for better readability.
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

    def export_profile_to_pdf(self, mother_info_text, child_info_text, address_info_text=None):
        """
        Function to export the profile to a structured PDF document.
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
        """
        try:
            if os.path.exists('combined_matched_data.xlsx'):
                os.system(f"open combined_matched_data.xlsx")
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

