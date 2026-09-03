# config.py
import os
import socket

import qrcode

from .commands import LaunchAppCommand, ExitCommand, PowerOffCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

# Configurazione griglia CustomTkinter
REMOTE_PORT = 5001
COLUMN_WEIGHTS = [1, 5, 1, 5, 1, 5, 1, 5, 1]
ROW_WEIGHTS = [30, 10, 40, 10, 40, 10, 40, 10]
NUMBER_OF_COLUMNS = 4
NUMBER_OF_ROWS= 3

COMMAND_REGISTRY = {

    "Bluetooth": LaunchAppCommand("bluetooth"),
    "DVD": LaunchAppCommand("dvd"),
    "Wifi": LaunchAppCommand("wifi"),
    "Kodi": LaunchAppCommand("kodi"),
    "PrimeVideo": LaunchAppCommand("primevideo"),

    "RaiPlay": LaunchAppCommand("raiplay"),
    "YouTube": LaunchAppCommand("youtube"),
    "RetroArch": LaunchAppCommand("retroarch"),
    "PowerOff": PowerOffCommand(),
    "Exit": ExitCommand(),

}


def get_local_ip():
    """Rileva l'IP locale attivo sulla scheda di rete (es. Wi-Fi/Hotspot)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Non invia realmente dati, serve solo per capire quale IP usa il PC verso l'esterno
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Fallback in caso di errore di rete
    finally:
        s.close()
    return local_ip

def get_local_ip():
    """Rileva l'IP locale attivo sulla scheda di rete (es. Wi-Fi/Hotspot)"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Non invia realmente dati, serve solo per capire quale IP usa il PC verso l'esterno
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Fallback in caso di errore di rete
    finally:
        s.close()
    return local_ip
def createRemoteQR(local_ip):
    url_telecomando = f"http://{local_ip}:{REMOTE_PORT}"


    qr_image_path = os.path.join(IMAGES_DIR, "RemoteQR.png")


    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=2
    )
    qr.add_data(url_telecomando)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="white", back_color="black")
    img_qr.save(qr_image_path)

createRemoteQR(get_local_ip())


PROGRAMS_DATA = [
    {"name": "Remote",    "image": os.path.join(IMAGES_DIR, "RemoteQR.png")},
    {"name": "Bluetooth", "image": os.path.join(IMAGES_DIR, "Bluetooth.png")},
    {"name": "DVD",       "image": os.path.join(IMAGES_DIR, "DVD.png")},
    {"name": "Wifi",   "image": os.path.join(IMAGES_DIR, "Wifi.jpg")},
    {"name": "Kodi",      "image": os.path.join(IMAGES_DIR, "Kodi.png")},
    {"name": "PrimeVideo",    "image": os.path.join(IMAGES_DIR, "Primevideo.jpeg")},
    {"name": "RaiPlay",    "image": os.path.join(IMAGES_DIR, "Raiplay.png")},
    {"name": "YouTube",    "image": os.path.join(IMAGES_DIR, "Youtube.jpg")},
    {"name": "RetroArch", "image": os.path.join(IMAGES_DIR, "RetroArch.png")},
    {"name": "Extra1",    "image": os.path.join(IMAGES_DIR, "Extra.jpeg")},
    {"name": "Exit",       "image": os.path.join(IMAGES_DIR, "Exit.png")},
    {"name": "PowerOff",   "image": os.path.join(IMAGES_DIR, "Poweroff.png")},


]