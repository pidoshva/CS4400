import pandas as pd #for excel manipulationsss

class Command:
    """Command Interface"""
    def execute(self):
        pass

class ReadExcelCommand(Command):
    """Concrete Commands"""
    pass

    def execute(self):
        pass

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
    
    def push(cmd Command):
        history.append(cmd)

    def pop():
        pass
    
