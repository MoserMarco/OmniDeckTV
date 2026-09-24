from app.commandExecutor import CommandExecutor
from app.gamepadListener import GamepadListener


def main():
    executor = CommandExecutor()
    controller = GamepadListener(executor)

    try:
        controller.listen()
    except KeyboardInterrupt:
        print("\n[SYSTEM] Chiusura...")


if __name__ == "__main__":
    main()