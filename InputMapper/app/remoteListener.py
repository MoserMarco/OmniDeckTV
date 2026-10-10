import socket
from .command import *
PC_PORT = 5000
PC_IP = "0.0.0.0"
class RemoteListener():
    def listen(self):

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((PC_IP, PC_PORT))

        print(f"Listening on port {PC_PORT}...")


        while True:

            data, addr = sock.recvfrom(1024)

            command = data.decode("utf-8")
            if command[:5] == "MOUSE":
                coordinates = command.split(":")[1].split(",")
                x, y = int(coordinates[0]), int(coordinates[1])
                MoveMouseCommand(x,y).execute()

            else:
                REMOTE_COMMAND_MAP[command]().execute()

