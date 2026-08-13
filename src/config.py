# config.py
import os
from commands import LaunchAppCommand, ExitCommand, PowerOffCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Configurazione griglia CustomTkinter
COLUMN_WEIGHTS = [1, 5, 1, 5, 1, 5, 1]
ROW_WEIGHTS = [30, 10, 40, 10, 40, 10, 40, 10]

COMMAND_REGISTRY = {
    "Kodi": LaunchAppCommand("kodi"),
    "DVD": LaunchAppCommand("dvd"),
    "Bluetooth": LaunchAppCommand("bluetooth"),
    "RetroArch": LaunchAppCommand("retroarch"),
    "Mame": LaunchAppCommand("mame"),
    "Exit": ExitCommand(),
    "PowerOff": PowerOffCommand()
}

# Definizione dei programmi nella griglia (3x3)
PROGRAMS_DATA = [
    {"name": "Kodi",      "image": os.path.join(IMAGES_DIR, "Kodi.png")},
    {"name": "DVD",       "image": os.path.join(IMAGES_DIR, "DVD.png")},
    {"name": "Bluetooth", "image": os.path.join(IMAGES_DIR, "Bluetooth.png")},
    {"name": "RetroArch", "image": os.path.join(IMAGES_DIR, "RetroArch.png")},
    {"name": "Mame",      "image": os.path.join(IMAGES_DIR, "Mame.jpeg")},
    {"name": "Extra1",    "image": os.path.join(IMAGES_DIR, "Extra.jpeg")},
    {"name": "Extra2",    "image": os.path.join(IMAGES_DIR, "Extra.jpeg")},
    {"name": "Exit",       "image": os.path.join(IMAGES_DIR, "Exit.png")},
    {"name": "PowerOff",   "image": os.path.join(IMAGES_DIR, "Poweroff.png")},
]