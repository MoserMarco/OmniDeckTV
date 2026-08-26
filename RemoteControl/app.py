import socket

from flask import Flask, render_template, jsonify, request
from wakeonlan import send_magic_packet

app = Flask(__name__)

# Configurazione PC da accendere (dummy dati per ora)
PC_MAC = "f4:4e:e3:0e:05:92"
PC_IP= "127.0.0.1"
PC_PORT = 5000
@app.route("/")
def index():
    return render_template("remote.html")
@app.route("/mouse")
def mouse():
    return render_template("mouse.html")

@app.route("/wake", methods=["POST"])
def wake_pc():
    try:
        send_magic_packet(PC_MAC)
        return jsonify({"status": "ok", "message": "Wake-on-LAN sent!"})
    except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

def send_key_to_pc(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(command.encode(), (PC_IP, PC_PORT))
@app.route("/key/<name>", methods=["POST"])
def press_key(name):
    allowed_keys = ["up", "down", "left", "right", "enter", "back", "home", "esc", "space","mouseLeft", "mouseRight"]
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
    print(command)
    send_key_to_pc(command)
    return jsonify(success=True)




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=False)
