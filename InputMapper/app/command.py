import time
from dataclasses import dataclass
from evdev import UInput, ecodes as e
import os
events = {
    e.EV_KEY: [
        # Keyboard keys
        e.KEY_SPACE, e.KEY_ESC, e.KEY_ENTER,
        e.KEY_UP, e.KEY_DOWN, e.KEY_LEFT, e.KEY_RIGHT,
        e.KEY_VOLUMEUP, e.KEY_VOLUMEDOWN, e.KEY_LEFTALT, e.KEY_F4,
        # Mouse buttons
        e.BTN_LEFT, e.BTN_RIGHT, e.BTN_MIDDLE
    ],
    e.EV_REL: [
        e.REL_X, e.REL_Y,  # Cursor movement (X = Horizontal, Y = Vertical)
        e.REL_WHEEL,       # Mouse scroll
        e.REL_HWHEEL
    ]
}

ui = UInput(events=events, name="VirtualInputDevice")


@dataclass
class Command:
    type: str

    def execute(self):
        pass





# ==========================================
# INPUT HELPER FUNCTIONS (EVDEV)
# ==========================================

def press_key(key_code: int):
    """Simulates a single key press and release."""
    ui.write(e.EV_KEY, key_code, 1)  # Key Down
    ui.syn()
    time.sleep(0.02)
    ui.write(e.EV_KEY, key_code, 0)  # Key Up
    ui.syn()


def press_hotkey(key1: int, key2: int):
    """Simulates a two-key combination (e.g., Alt + F4)."""
    ui.write(e.EV_KEY, key1, 1)
    ui.write(e.EV_KEY, key2, 1)
    ui.syn()
    time.sleep(0.02)
    ui.write(e.EV_KEY, key2, 0)
    ui.write(e.EV_KEY, key1, 0)
    ui.syn()


def click_mouse(btn_code: int):
    """Simulates a mouse button click (Left or Right)."""
    ui.write(e.EV_KEY, btn_code, 1)
    ui.syn()
    time.sleep(0.02)
    ui.write(e.EV_KEY, btn_code, 0)
    ui.syn()


def scroll_mouse(amount: int):
    """Simulates mouse wheel scrolling."""
    ui.write(e.EV_REL, e.REL_WHEEL, amount)
    ui.syn()

# ==========================================
# KEYBOARD COMMANDS
# ==========================================

class PauseCommand(Command):
    def __init__(self):
        super().__init__(type="PAUSE")

    def execute(self):
        press_key(e.KEY_SPACE)
class BackCommand(Command):
    def __init__(self):
        super().__init__(type="BACK")

    def execute(self):
        press_key(e.KEY_ESC)
class EnterCommand(Command):
    def __init__(self):
        super().__init__(type="ENTER")

    def execute(self):
        press_key(e.KEY_ENTER)
class KeyUpCommand(Command):
    def __init__(self):
        super().__init__(type="KEY_UP")

    def execute(self):
        press_key(e.KEY_UP)
class KeyDownCommand(Command):
    def __init__(self):
        super().__init__(type="KEY_DOWN")

    def execute(self):
        press_key(e.KEY_DOWN)
class KeyLeftCommand(Command):
    def __init__(self):
        super().__init__(type="KEY_LEFT")

    def execute(self):

        press_key(e.KEY_LEFT)
class KeyRightCommand(Command):
    def __init__(self):
        super().__init__(type="KEY_RIGHT")

    def execute(self):
        press_key(e.KEY_RIGHT)

# ==========================================
# VOLUME COMMANDS
# ==========================================

class VolumeUpCommand(Command):
    def __init__(self):
        super().__init__(type="VOLUME_UP")

    def execute(self):
        press_key(e.KEY_VOLUMEUP)
class VolumeDownCommand(Command):
    def __init__(self):
        super().__init__(type="VOLUME_DOWN")

    def execute(self):
        press_key(e.KEY_VOLUMEDOWN)

# ==========================================
# MOUSE COMMANDS
# ==========================================

class LeftClickCommand(Command):
    def __init__(self):
        super().__init__(type="LEFT_CLIK")

    def execute(self):
        click_mouse(e.BTN_LEFT)
class RightClickCommand(Command):
    def __init__(self):
        super().__init__(type="RIGHT_CLIK")

    def execute(self):
        click_mouse(e.BTN_RIGHT)
class ScrollUpCommand(Command):
    def __init__(self):
        super().__init__(type="SCROLL_UP")

    def execute(self):
        scroll_mouse(1)  # Scroll up (+1 tick)
class ScrollDownCommand(Command):
    def __init__(self):
        super().__init__(type="SCROLL_DOWN")

    def execute(self):
        scroll_mouse(-1)  # Scroll down (-1 tick)
class MoveMouseCommand(Command):
    def __init__(self, x: int, y: int):
        super().__init__(type="MOVE_MOUSE")
        self.x = x
        self.y = y

    def execute(self):
        # Invia entrambi i delta relativi nello stesso sync
        if self.x != 0:
            ui.write(e.EV_REL, e.REL_X, self.x)
        if self.y != 0:
            ui.write(e.EV_REL, e.REL_Y, self.y)
        ui.syn()

# ==========================================
# SYSTEM COMMANDS
# ==========================================

class CloseSoftwareCommand(Command):
    def __init__(self):
        super().__init__(type="CLOSE_SOFTWARE")

    def execute(self):
        press_hotkey(e.KEY_LEFTALT, e.KEY_F4)

class PowerOffCommand(Command):
    def __init__(self):
        super().__init__(type="CLOSE_SOFTWARE")

    def execute(self):
        os.system("shutdown -h now")
class NoneCommand(Command):
    def __init__(self):
        super().__init__(type="NONE")

    def execute(self):
        print("no command selected")


# ==========================================
# KEY COMMAND MAPPING
# ==========================================

PAD_COMMAND_MAP = {
    # Buttons A, B, X, Y
    "BTN_SOUTH": lambda: LeftClickCommand(),
    "BTN_A": lambda: LeftClickCommand(),
    "BTN_EAST": lambda: RightClickCommand(),
    "BTN_B": lambda: RightClickCommand(),
    "BTN_NORTH": lambda: PauseCommand(),
    "BTN_X": lambda: PauseCommand(),
    "BTN_WEST": lambda: BackCommand(),
    "BTN_Y": lambda: BackCommand(),

    # Bumpers and Triggers
    "BTN_TL": lambda: ScrollUpCommand(),
    "BTN_TR": lambda: ScrollDownCommand(),
    "BTN_TL2": lambda: VolumeDownCommand(),
    "BTN_TR2": lambda: VolumeUpCommand(),

    # System Buttons and Thumbsticks
    "BTN_SELECT": lambda: CloseSoftwareCommand(),
    "BTN_START": lambda: EnterCommand(),
    "BTN_HOME": lambda: NoneCommand(),
    "BTN_THUMBL": lambda: NoneCommand(),
    "BTN_THUMBR": lambda: NoneCommand(),
}

REMOTE_COMMAND_MAP = {
    # Mouse
    "LEFTCLICK": lambda: LeftClickCommand(),
    "RIGHTCLICK": lambda: RightClickCommand(),
    "SCROLLUP": lambda: ScrollUpCommand(),
    "SCROLLDOWN": lambda: ScrollDownCommand(),

    # Key
    "PAUSE": lambda: PauseCommand(),
    "BACK": lambda: BackCommand(),
    "ENTER": lambda: EnterCommand(),
    "VOLUMEDOWN": lambda: VolumeDownCommand(),
    "VOLUMEUP": lambda: VolumeUpCommand(),

    "UPARROW": lambda: KeyUpCommand(),
    "LEFTARROW": lambda: KeyLeftCommand(),
    "RIGHTARROW": lambda: KeyRightCommand(),
    "DOWNARROW": lambda: KeyDownCommand(),

    # Syste
    "CLOSESOFTWARE": lambda: CloseSoftwareCommand(),
    "POWEROFF": lambda: PowerOffCommand(),
    "HOME": lambda: NoneCommand(),


}

