#commands.py
import os
from abc import ABC, abstractmethod
import sys
import subprocess
import os
from pathlib import Path

# os.path.expanduser("~") converte automaticamente "~" nel percorso reale (es. /home/tuoutente)
user_data = os.path.expanduser("~/.config/google-chrome")
CURRENT_DIR = Path(__file__).resolve().parent
SCRIPT_DVD_PATH = CURRENT_DIR.parent / "scripts" / "playDVD.sh"
SCRIPT_RETROARCH_PATH = CURRENT_DIR.parent / "scripts" / "retroarch.sh"
command_to_launch_program = {

    "bluetooth": ['gnome-control-center', 'bluetooth'],
    "dvd": ['/bin/bash',str(SCRIPT_DVD_PATH)],
    "kodi": ['flatpak', 'run', 'tv.kodi.Kodi'],
    "wifi": ['gnome-control-center', 'wifi'],
    "primevideo": [
        'google-chrome',
        f'--user-data-dir={user_data}',
        '--profile-directory=Default',
        '--start-fullscreen',
        'https://www.primevideo.com'
    ],
    "raiplay": [
        'google-chrome',
        f'--user-data-dir={user_data}',
        '--profile-directory=Default',
        '--start-fullscreen',
        'https://www.raiplay.it'
    ],
    "youtube": [
        'google-chrome',
        f'--user-data-dir={user_data}',
        '--profile-directory=Default',
        '--start-fullscreen',
        'https://www.youtube.com'
    ],


    "retroarch": ['/bin/bash',str(SCRIPT_RETROARCH_PATH)],



}


class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    def __call__(self):

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

