import threading
from app.gamepadListener import GamepadListener
from app.remoteListener import RemoteListener


def main():

    controller = GamepadListener()
    remote = RemoteListener()

    thread_remote = threading.Thread(target=remote.listen, daemon=True)
    thread_controller = threading.Thread(target=controller.listen, daemon=True)
    try:
        thread_remote.start()
        thread_controller.start()

        thread_remote.join()
        thread_controller.join()

    except KeyboardInterrupt:
        print("\n[SYSTEM] CLOSING...")


if __name__ == "__main__":
    main()