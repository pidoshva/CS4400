import pandas as pd #for excel manipulationsss
import tkinter as tk
from tkinter import filedialog, messagebox

class Command:
    """Command Interface"""
    def execute(self):
        pass

class ReadExcelCommand(Command):
    def __init__(self, filepath, app):
        self.filepath = filepath
        self.app = app
        self.data = None

    """Concrete Commands"""
    def execute(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("Excel files", "*.xlsx *.xls")])
        if not filepath:
            pass #throw an error

        command = ReadExcelCommand(filepath, self)
        self.invoker.add_command(command) #???
        messagebox.showinfo(
                "Success", f"File '{filepath}' read successfully.")
        data_frame = pd.read_excel(filepath)
        data_frame.columns = [column.replace(" ", "_") for column in data_frame.columns]
        return data_frame

class CombineDataCommand(Command):
    def execute(self, data_frames):
        combined_data_frames = pd.concat(data_frames)
        combined_data_frames.to_excel('output.xlsx')

class SaveDataCommand(Command):
    def __init__(self):
        pass

    def execute(self):
        pass

class Invoker:
    """Invoker class"""
    def __init__(self,app):
        pass

    def add_command(self, command):
        pass

    def execute_commands(self):
        pass
        
class CommandHistory:
    """CommandHistory class"""
    #list of commands
    history = []
    
    def __init__(self,):
        pass
    
    def push(self, cmd: Command):
        pass
        # history.append(cmd)

    def pop():
        pass
    
