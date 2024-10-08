import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from invoker import ReadExcelCommand, CombineDataCommand, Invoker


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Combiner")

        # Initialize variables
        self.invoker = Invoker()  # Create an Invoker to manage commands
        self.data_frames = []  # Store the two data frames to be combined
        self.combined_data = None  # Store the combined data

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        # Buttons for reading two Excel files
        self.read_button1 = tk.Button(self.root, text="Read Excel File 1", command=self.read_excel_file)
        self.read_button1.pack(pady=5)

        self.read_button2 = tk.Button(self.root, text="Read Excel File 2", command=self.read_excel_file)
        self.read_button2.pack(pady=5)

        # Button to combine the data
        self.combine_button = tk.Button(self.root, text="Combine Data", command=self.combine_data)
        self.combine_button.pack(pady=5)

    def read_excel_file(self):
        """Read an Excel file and append its data to the list"""
        command = ReadExcelCommand(self)
        self.invoker.add_command(command)
        data_frame = command.execute()
        if data_frame is not None:
            self.data_frames.append(data_frame)

    def combine_data(self):
        """Combine the two read Excel files and display the combined names"""
        if len(self.data_frames) >= 2:
            # Combine data
            command = CombineDataCommand(self, self.data_frames)
            self.invoker.add_command(command)
            combined_data = command.execute()

            if combined_data is not None:
                # Store combined data in app
                self.combined_data = combined_data
                # Display the combined names in the UI window
                self.display_combined_names()

        else:
            messagebox.showwarning("Warning", "Please read two Excel files first.")

    def display_combined_names(self):
        """Display a new window with the list of combined names (Mother ID, Child Name, DOB)"""
        combined_names_window = tk.Toplevel(self.root)
        combined_names_window.title("Combined Data")

        # Listbox to display combined names
        listbox = tk.Listbox(combined_names_window)
        listbox.pack(fill=tk.BOTH, expand=True)

        # Add the combined names to the listbox (Mother ID, Child Name, DOB)
        for index, row in self.combined_data.iterrows():
            display_text = f"{row['Mother_ID']} {row['Child_First_Name']} {row['Child_Last_Name']} (DOB: {row['Child_Date_of_Birth']})"
            listbox.insert(tk.END, display_text)

        # Bind double-click event to open child profile
        listbox.bind('<Double-1>', lambda event: self.show_child_profile(event, listbox))

    def show_child_profile(self, event, listbox):
        """Show child profile when a name is double-clicked"""
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
                print("No matching data found:")
                print(f"Mother ID: {mother_id}, Child Name: {child_first_name} {child_last_name}, DOB: {child_dob}")
                messagebox.showerror("Error", f"No data found for {child_first_name} {child_last_name}.")
                # print("Combined Data (First 5 Rows):")
                # print(self.combined_data.head())
                return

            # Get the first matching row
            child_data = child_data.iloc[0]

            # Show profile window
            profile_window = tk.Toplevel(self.root)
            profile_window.title(f"Profile of {child_first_name} {child_last_name}")

            # Display child's information in the profile window
            for col in child_data.index:
                label = tk.Label(profile_window, text=f"{col}: {child_data[col]}")
                label.pack(anchor='w')

        except Exception as e:
            messagebox.showerror("Error", f"Error loading profile: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
