import socket

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Configurazione PC da accendere (dummy dati per ora)
PC_MAC = "f4:4e:e3:0e:05:92"
#PC_IP= "host.docker.internal"
PC_IP= "127.0.0.1"
PC_PORT = 5000
REMOTE_PORT = 5001
@app.route("/")
def index():
    return render_template("remote.html")
@app.route("/mouse")
def mouse():
    return render_template("mouse.html")

def send_key_to_pc(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (PC_IP, PC_PORT))

@app.route("/key/<name>", methods=["POST"])
def press_key(name):
    allowed_keys = ["UPARROW","DOWNARROW","LEFTARROW","RIGHTARROW","LEFTCLICK","RIGHTCLICK","PAUSE","BACK","SCROLLUP","SCROLLDOWN","VOLUMEDOWN","VOLUMEUP","CLOSESOFTWARE","ENTER", "HOME", "POWEROFF"]
    if name in allowed_keys:
        send_key_to_pc(name)
        return jsonify({"status": "ok", "message": f"Button {name} sent"})
    else:
        return jsonify({"status": "error", "message": "Button non valido"})

@app.route("/mouse_move", methods=["POST"])
def mouse_move():
    data = request.get_json()
    dx = data.get("dx", 0)
    dy = data.get("dy", 0)


    command = f"MOUSE:{dx},{dy}"
    send_key_to_pc(command)
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=REMOTE_PORT, debug=False)
