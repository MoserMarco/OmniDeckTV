from app.commandExecutor import CommandExecutor
from app.gamepadListener import GamepadListener


def main():

    controller = GamepadListener()

    try:
        controller.listen()
    except KeyboardInterrupt:
        print("\n[SYSTEM] CLOSING...")


if __name__ == "__main__":
    main()