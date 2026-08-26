#commands.py
import os
from abc import ABC, abstractmethod
import sys
import subprocess
import os

# os.path.expanduser("~") converte automaticamente "~" nel percorso reale (es. /home/tuoutente)
user_data = os.path.expanduser("~/.config/google-chrome")
command_to_launch_program = {

    "bluetooth": ['gnome-control-center', 'bluetooth'],
    "dvd": ['/bin/bash','../scripts/playDVD.sh'],
    "kodi": ['flatpak', 'run', 'tv.kodi.Kodi'],
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

    "retroarch": ['flatpak', 'run', 'org.libretro.RetroArch'],



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

