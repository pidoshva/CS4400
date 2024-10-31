import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import logging
from invoker import ReadExcelCommand, CombineDataCommand, Invoker
import tkinter.ttk as ttk  # for treeview
import os
import tempfile
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App:
    """
    The main application class for combining two Excel files.
    It handles user interactions for reading files, combining data, and displaying profiles.
    """
    def __init__(self, root):
        if root is not None:
            self.__root = root
            self.__root.title("Excel Combiner")
            self.create_widgets()
        else:
            self.__root = None

        self._combined_data = None
        self.__data_frames = []

    def create_widgets(self):
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

        logging.info("UI widgets created.")

    def read_excel_file(self):
        command = ReadExcelCommand(self)
        data_frame = command.execute()
        if data_frame is not None:
            self.__data_frames.append(data_frame)
            logging.info(f"Data from {command.filepath} successfully read and added to data frames.")
        else:
            logging.warning("No data frame returned from the file read.")

    def combine_data(self):
        if len(self.__data_frames) >= 2:
            logging.info("Attempting to combine data from two Excel files.")
            command = CombineDataCommand(self, self.__data_frames)
            combined_data = command.execute()

            if combined_data is not None:
                self.__combined_data = combined_data
                self.display_combined_names()
                logging.info("Data combined and displayed successfully.")
        else:
            messagebox.showwarning("Warning", "Please read two Excel files first.")
            logging.warning("Attempted to combine data with less than two files.")

    def display_combined_names(self):
        combined_names_window = tk.Toplevel(self.__root)
        combined_names_window.title("Combined Data")

        def on_closing():
            if tk.messagebox.askokcancel("Quit", "Do you want to exit this view?\nFiles must be uploaded to view the data again."):
                combined_names_window.destroy()
                self.__data_frames.clear()

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

        columns = ("Mother ID", "Child Name", "Child DOB")
        self.treeview = ttk.Treeview(combined_names_window, columns=columns, show='headings')

        tree_scroll = tk.Scrollbar(self.treeview, command=self.treeview.yview)
        tree_scroll.pack(side="right", fill="y")
        self.treeview.configure(yscrollcommand=tree_scroll.set)

        self.treeview.heading("Mother ID", text="Mother ID")
        self.treeview.heading("Child Name", text="Child Name")
        self.treeview.heading("Child DOB", text="Child DOB")
        
        self.treeview.column("Mother ID", width=150, anchor="center")
        self.treeview.column("Child Name", width=250, anchor="center")
        self.treeview.column("Child DOB", width=150, anchor="center")

        self.update_combined_names()
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

    def update_combined_names(self):
        self.treeview.delete(*self.treeview.get_children())
        search_term = self.search_var.get().lower()
        for index, row in self.__combined_data.iterrows():
            child_name = f"{row['Child_First_Name']} {row['Child_Last_Name']}"
            display_text = f"{row['Mother_ID']} {child_name} (DOB: {row['Child_Date_of_Birth']})"
            if search_term in display_text.lower():
                self.treeview.insert("", "end", values=(row['Mother_ID'], child_name, row['Child_Date_of_Birth']))

        logging.info("Treeview updated with filtered names.")

    def display_unmatched_data(self, unmatched_data):
        """
        Display a new window with the unmatched data in a Treeview.
        """
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

        # Function to toggle displaying additional information for the clicked row
        def toggle_expand(event):
            # Ensure there is a selected item before proceeding
            selected_items = treeview.selection()
            if not selected_items:
                return  # Exit if no item is selected

            selected_item = selected_items[0]
            row_data = expanded_rows.get(selected_item, {})
            is_expanded = row_data.get("expanded", False)

            if not is_expanded:
                # Add additional information rows for expansion
                detail_items = []
                for detail in row_data["details"]:
                    detail_item = treeview.insert(selected_item, "end", values=[detail], tags=("additional",))
                    detail_items.append(detail_item)
                row_data["expanded"] = True
                row_data["detail_items"] = detail_items  # Store detail items for future collapse
            else:
                # Collapse by removing detail items
                for child in row_data.get("detail_items", []):
                    treeview.delete(child)
                row_data["expanded"] = False
                row_data["detail_items"] = []  # Reset detail items

            # Update the expanded_rows dictionary to reflect changes
            expanded_rows[selected_item] = row_data

        # Attach this function to a double-click event
        treeview.bind("<Double-1>", toggle_expand)



        # Style the additional information rows for readability and background color
        treeview.tag_configure("additional", background="#8f6a6a", font=("Arial", 10, "italic"))

        unmatched_data_window.mainloop()



    def search_combined_names(self):
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

