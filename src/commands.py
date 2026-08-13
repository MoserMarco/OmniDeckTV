#commands.py
import os
from abc import ABC, abstractmethod
import sys
import subprocess

command_to_launch_program = {
    "kodi": ['flatpak', 'run', 'tv.kodi.Kodi'],
    "dvd": ['/bin/bash','../scripts/dvd_Kodi.sh'],
    "bluetooth": ['gnome-control-center', 'bluetooth'],
    "retroarch": ['flatpak', 'run', 'org.libretro.RetroArch'],
    "mame": ['ls', '-l'],


}


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
        try:
            subprocess.Popen(command_to_launch_program.get(self.process_name))
        except Exception as e:
            print(f"[Command] Error: {e}")



class ExitCommand(Command):
    def execute(self):
        print("[Command] Close application...")
        sys.exit(0)



class PowerOffCommand(Command):
    def execute(self):
        print("[Command] Power Off...")
        subprocess.run(['systemctl', 'poweroff'])


class NoOpCommand(Command):
    def execute(self):
        print("[Command] No action selected")

