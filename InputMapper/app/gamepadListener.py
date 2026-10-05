import evdev
from evdev import InputDevice, ecodes
from pathlib import Path
import json
from typing import Optional, Tuple, Dict
from evdev import ecodes, InputEvent, InputDevice
from .command import *
import threading
import time
SENSITIVITY = 0.08 #calculated for value of the stics in [-128,127]
REFRESH_RATE = 1 / 60
class GamepadListener:
    """
    Handles input events from a connected gamepad and translates them
    into system commands. Supports custom JSON mappings as well as
    automatic fallback to Linux kernel ecodes constants.
    """



    def __init__(self,  config_file: str = "config.json") -> None:

        self.config_file = Path(__file__).resolve().parent.parent / config_file
        self.config_selected, self.offset, self.deadzone, self.custom_keys, self.custom_axes = self._load_config()
        self.device: Optional[InputDevice] = self._find_gamepad()

        #Variables used of mouse moving
        self.rx = 0
        self.ry = 0
        self.running = False
        self.mouse_thread: Optional[threading.Thread] = None

        #To disable auto fire on CloseSoftwareCommand and EnterCommand (I DONT KNOW WHY IT IS ENABLED)
        self.last_command_time: dict[str, float] = {}
        self.cooldown_seconds: float = 2

    def _find_gamepad(self):
        for path in evdev.list_devices():
            try:
                dev = InputDevice(path)


                dev_name = dev.name.lower()
                if "uinput" in dev_name or "py-evdev" in dev_name:
                    continue

                caps = dev.capabilities().get(ecodes.EV_KEY, [])
                if ecodes.BTN_GAMEPAD in caps or ecodes.BTN_SOUTH in caps:
                    print(f"[GAMEPAD] Connected to: {dev.name}")
                    return dev
            except Exception:
                continue

        print("[GAMEPAD] No GamePad Found.")
        return None

    def _load_config(self) -> Tuple[bool, Dict[int, str], Dict[int, str]]:
        """
        Reads the JSON configuration file. If 'ConfigurationSelected' is True,
        it parses and returns custom button and axis mappings. Otherwise,
        it falls back to automatic ecodes translation.
        """
        try:

            with open(self.config_file, "r") as f:
                data = json.load(f)

            is_selected = data.get("ConfigurationSelected", False)

            if is_selected:
                offset = data.get("Offset", 0)
                deadzone = data.get("DeadZone", 12000)
                custom_axes = {}
                raw_axes = data.get("axes", {})

                for axis_code_str, axis_name in raw_axes.items():

                    axis_code_int = int(axis_code_str)
                    custom_axes[axis_code_int] = axis_name



                custom_keys = {}

                for key_code_str, button_name in data.items():

                    if key_code_str in ("axes", "ConfigurationSelected", "Offset", "DeadZone"):
                        continue


                    key_code_int = int(key_code_str)
                    custom_keys[key_code_int] = button_name

                return True, offset, deadzone, custom_keys, custom_axes

        except Exception as e:
            print(f"[WARN] Failed to load '{self.config_file}': {e}")

        print("[CONFIG] No custom configuration selected. Falling back to AUTOMATIC ECODES translation.")
        return False, 0, 12000, {}, {}

    def _resolve_name(self, event: InputEvent) -> Optional[str]:
        """
        Determines the symbolic string name for an event code.
        Uses the custom JSON mappings if ConfigurationSelected is True;
        otherwise queries Linux ecodes definitions directly.
        """
        # 1. USE CUSTOM MAPPINGS IF ENABLED

        if self.config_selected:

            if event.type == ecodes.EV_KEY:
                return self.custom_keys.get(event.code)
            elif event.type == ecodes.EV_ABS:
                event.value = event.value
                return self.custom_axes.get(event.code)
            return None

        # 2. AUTOMATIC FALLBACK USING ECODES
        name = None
        if event.type == ecodes.EV_KEY:
            name = ecodes.BTN.get(event.code) or ecodes.KEY.get(event.code)
        elif event.type == ecodes.EV_ABS:
            name = ecodes.ABS.get(event.code)

        # Handle aliased tuples returned by evdev (e.g., ('BTN_A', 'BTN_SOUTH'))
        if isinstance(name, (tuple, list)):
            name = name[0]

        return name

    def _mouse_loop(self) -> None:
        """
        Background loop running at 60 FPS.
        Calculates and sends continuous relative mouse movement as long as the stick is tilted.
        """
        while self.running:
            dx = 0
            dy = 0

            # X Axis calculation with deadzone
            if abs(self.rx) > self.deadzone:
                raw_x = self.rx - (self.deadzone if self.rx > 0 else -self.deadzone)
                dx = int(raw_x * SENSITIVITY)

            # Y Axis calculation with deadzone
            if abs(self.ry) > self.deadzone:
                raw_y = self.ry - (self.deadzone if self.ry > 0 else -self.deadzone)
                dy = int(raw_y * SENSITIVITY)

            # Execute relative mouse movement continuously while held
            if dx != 0 or dy != 0:
                MoveMouseCommand(dx, dy).execute()

            # Maintain smooth ~60 FPS rate
            time.sleep(REFRESH_RATE)

    def translate_event_to_command(self, event: InputEvent) -> Optional[Command]:
        """
        Translates a raw evdev InputEvent into an application-level Command object.
        """
        cmd_name = self._resolve_name(event)
        if not cmd_name:
            return None

        # -------------------------------------------------------------
        # 1. PHYSICAL BUTTONS (EV_KEY)
        # -------------------------------------------------------------
        if event.type == ecodes.EV_KEY and event.value == 1:
            if cmd_name in PAD_COMMAND_MAP:
                return PAD_COMMAND_MAP[cmd_name]()
            if cmd_name in ["BTN_SELECT","BTN_START"]:
                time.sleep(1)

        # -------------------------------------------------------------
        # 2. And DIRECTION PAD ANALOG STICKS (EV_ABS)
        # -------------------------------------------------------------
        elif event.type == ecodes.EV_ABS:

            # --- A. D-PAD / DIRECTIONAL PAD ---
            if cmd_name == "ABS_HAT0Y":  # D-Pad Vertical Axis
                if event.value < 0:
                    return KeyUpCommand()
                elif event.value > 0:
                    return KeyDownCommand()
            elif cmd_name == "ABS_HAT0X":
                if event.value < 0:
                    return KeyLeftCommand()
                elif event.value > 0:
                    return KeyRightCommand()


            # --- B.  STICKS ---
            # 1. Update current axis state
            if cmd_name in ["ABS_RX","ABS_X"]:
                self.rx = event.value + self.offset
            elif cmd_name in  ["ABS_RY","ABS_Y"] :
                self.ry = event.value + self.offset



        return None

    def listen(self) -> None:
        """
        Main loop listening to hardware events from the gamepad device.
        Filter out system noise (EV_SYN/EV_MSC) and forward commands.
        """
        if not self.device:
            print("[ERROR] Gamepad device not initialized.")
            return

        self.running = True
        self.mouse_thread = threading.Thread(target=self._mouse_loop, daemon=True)
        self.mouse_thread.start()
        ignore = False
        print(f"[LISTENING] Gamepad loop started on device: {self.device.name}")
        try:
            for event in self.device.read_loop():
                # Skip synchronization and misc events
                if event.type in (ecodes.EV_SYN, ecodes.EV_MSC):
                    continue

                command = self.translate_event_to_command(event)

                if command is not None:
                    current_time = time.time()
                    command_name = command.type

                    if command_name in ("ENTER", "CLOSE_SOFTWARE"):

                        last_time = self.last_command_time.get(command_name, 0.0)
                        if current_time - last_time < self.cooldown_seconds:
                            continue
                        self.last_command_time[command_name] = current_time

                    command.execute()
        finally:
            # Stop the mouse thread safely when exiting the loop
            self.stop()

    def stop(self) -> None:
        """Safely terminates the listener thread."""
        self.running = False
        if self.mouse_thread and self.mouse_thread.is_alive():
            self.mouse_thread.join()