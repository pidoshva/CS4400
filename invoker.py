import pandas as pd #for excel manipulationsss
import tkinter as tk
from tkinter import filedialog

class Command:
    """Command Interface"""
    def execute(self):
        pass

#should this open a file explorer to find a file to read?
class ReadExcelCommand(Command):
    """Concrete Commands"""

    def execute(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        if not file_path:
            #throw an error
            pass
        
        data = pd.read_excel(file_path)

        # replacing blank spaces with '_' 
        data.columns = [column.replace(" ", "_") for column in data.columns] 

        #test query
        result = data.query('Child_Name == "Jennifer Miller"')
        print(result)

class CombineDataCommand(Command):
    def __init__(self):
        pass

    def execute(self):
        pass

class SaveDataCommand(Command):
    def __init__(self):
        pass

    def execute(self):
        pass

class Invoker:
    """Invoker class"""
    def __init__(self):
        pass

    def add_command(self, command):
        pass

    def execute_commands(self):
        pass
        
class CommandHistory:
    """CommandHistory class"""
    #list of commands
    history = []
    
    def __init__(self):
        pass

    def push(cmd):
        history.append(cmd)

    def pop():
        pass
    
