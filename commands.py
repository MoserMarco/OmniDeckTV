#commands.py
import os
from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def __call__(self):
        """Rende l'oggetto 'Callable', consentendo a CustomTkinter di invocarlo come una funzione."""
        return self.execute()

# 2. Comandi Concreti
class LaunchAppCommand(Command):
    def __init__(self, process_name):
        self.process_name = process_name

    def execute(self):
        print(f"[Command] Start software: {self.process_name}")


class ExitCommand(Command):
    def __init__(self, root_window):
        self.root_window = root_window
    def execute(self):
        print("[Command] Close application...")



class PowerOffCommand(Command):
    def execute(self):
        print("[Command] Power Off...")


class NoOpCommand(Command):
    def execute(self):
        print("[Command] No action selected")

