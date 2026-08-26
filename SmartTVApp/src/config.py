# config.py
import os
from .commands import LaunchAppCommand, ExitCommand, PowerOffCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Configurazione griglia CustomTkinter
COLUMN_WEIGHTS = [1, 5, 1, 5, 1, 5, 1, 5, 1]
ROW_WEIGHTS = [30, 10, 40, 10, 40, 10, 40, 10]
NUMBER_OF_COLUMNS = 4
NUMBER_OF_ROWS= 3
COMMAND_REGISTRY = {

    "Bluetooth": LaunchAppCommand("bluetooth"),
    "DVD": LaunchAppCommand("dvd"),
    "PowerOff": PowerOffCommand(),
    "Kodi": LaunchAppCommand("kodi"),
    "PrimeVideo": LaunchAppCommand("primevideo"),

    "RaiPlay": LaunchAppCommand("raiplay"),
    "YouTube": LaunchAppCommand("youtube"),
    "RetroArch": LaunchAppCommand("retroarch"),
    "Exit": ExitCommand(),

}

# Definizione dei programmi nella griglia (3x3)
PROGRAMS_DATA = [
    {"name": "Remote",    "image": os.path.join(IMAGES_DIR, "Remote.png")},
    {"name": "Bluetooth", "image": os.path.join(IMAGES_DIR, "Bluetooth.png")},
    {"name": "DVD",       "image": os.path.join(IMAGES_DIR, "DVD.png")},
    {"name": "PowerOff",   "image": os.path.join(IMAGES_DIR, "Poweroff.png")},
    {"name": "Kodi",      "image": os.path.join(IMAGES_DIR, "Kodi.png")},
    {"name": "PrimeVideo",    "image": os.path.join(IMAGES_DIR, "Primevideo.jpeg")},
    {"name": "RaiPlay",    "image": os.path.join(IMAGES_DIR, "Raiplay.png")},
    {"name": "YouTube",    "image": os.path.join(IMAGES_DIR, "Youtube.jpg")},
    {"name": "RetroArch", "image": os.path.join(IMAGES_DIR, "RetroArch.png")},
    {"name": "Extra1",    "image": os.path.join(IMAGES_DIR, "Extra.jpeg")},
    {"name": "Extra2",    "image": os.path.join(IMAGES_DIR, "Extra.jpeg")},
    {"name": "Exit",       "image": os.path.join(IMAGES_DIR, "Exit.png")},

]