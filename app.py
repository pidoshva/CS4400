import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from invoker import (Command, ReadExcelCommand, CombineDataCommand,
                     SaveDataCommand, Invoker, CommandHistory)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel Combiner")

        # Initialize components
        self.invoker = Invoker(self)
        self.history = CommandHistory()
        self.data_frames = [] #??? is this needed?
        self.combined_data = None

        # Set up the GUI
        self.create_widgets()

    def create_widgets(self):
        self.read_button1 = tk.Button(
            self.root, text="Read Excel File 1",command=self.read_excel_file1) 
        self.read_button1.pack(pady=5)

        self.read_button2 = tk.Button(
            self.root, text="Read Excel File 2",command=self.read_excel_file2)
        self.read_button2.pack(pady=5)

        # combine
        self.combine_button = tk.Button(
            self.root, text="Combine Data",command=self.combine_data)
        self.combine_button.pack(pady=5)

        # Button to save the combined data
        self.save_button = tk.Button(
            self.root, text="Save Combined Data",command=self.save_combined_data)
        self.save_button.pack(pady=5)

        # Button to undo the last action
        self.undo_button = tk.Button(
            self.root, text="Undo",)
        self.undo_button.pack(pady=5)

    def read_excel_file1(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:
            command = ReadExcelCommand(filepath, self)
            self.invoker.add_command(command) #???
            messagebox.showinfo(
                "Success", f"File '{filepath}' read successfully.")

    def read_excel_file2(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")])
        if filepath:
            command = ReadExcelCommand(filepath, self)
            self.invoker.add_command(command) #???
            messagebox.showinfo(
                "Success", f"File '{filepath}' read successfully.")

    def combine_data(self):
        if len(self.data_frames) >= 2:
            command = CombineDataCommand(self)
            self.invoker.add_command(command)
            messagebox.showinfo("Success", "Data combined successfully.")
        else:
            messagebox.showwarning(
                "Warning", "Please read two Excel files first.")

    def save_combined_data(self):
        if self.combined_data is not None:
            filepath = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx *.xls")])
            if filepath:
                command = SaveDataCommand(filepath, self)
                self.invoker.add_command(command)
                messagebox.showinfo(
                    "Success", f"Combined data saved to '{filepath}'.")
        else:
            messagebox.showwarning(
                "Warning", "No combined data to save.")

    def undo(self):
        self.history.undo()
        messagebox.showinfo("Undo", "Previous action has been undone.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

