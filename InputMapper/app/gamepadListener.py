import evdev
from evdev import InputDevice, ecodes
from pathlib import Path
import json
from typing import Optional, Tuple, Dict
from evdev import ecodes, InputEvent, InputDevice
from app.command import Command
from app.commandExecutor import CommandExecutor


class GamepadListener:
    """
    Handles input events from a connected gamepad and translates them
    into system commands. Supports custom JSON mappings as well as
    automatic fallback to Linux kernel ecodes constants.
    """
    DEADZONE: int = 40

    def __init__(self, executor: CommandExecutor, config_file: str = "config.json") -> None:
        self.executor = executor
        self.config_file = Path(__file__).resolve().parent.parent / config_file
        self.config_selected, self.offset, self.deadzone, self.custom_keys, self.custom_axes = self._load_config()
        self.device: Optional[InputDevice] = self._find_gamepad()

    def _find_gamepad(self):
        for path in evdev.list_devices():
            try:
                dev = InputDevice(path)
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
            if cmd_name in ("BTN_SOUTH", "BTN_A"):
                print(cmd_name)
                return Command(type="LEFT_CLIK", value="KEY_SPACE")
            elif cmd_name in ("BTN_EAST", "BTN_B"):
                print(cmd_name)
                return Command(type="RIGHT_CLIK", value="KEY_ESC")
            elif cmd_name in ("BTN_NORTH", "BTN_X"):
                print(cmd_name)
                return Command(type="PAUSE", value="TOGGLE_FULLSCREEN")
            elif cmd_name in ("BTN_WEST", "BTN_Y"):
                print(cmd_name)
                return Command(type="BACK", value="MUTE")
            elif cmd_name == "BTN_TL":
                print(cmd_name)
                return Command(type="SCROLL_UP", value="PREVIOUS_TRACK")
            elif cmd_name == "BTN_TR":
                #print(cmd_name)
                return Command(type="SCROLL_DOWN", value="NEXT_TRACK")
            elif cmd_name == "BTN_TL2":
                print(cmd_name)
                return Command(type="VOLUME_DOWN", value="PREVIOUS_TRACK")
            elif cmd_name == "BTN_TR2":
                print(cmd_name)
                return Command(type="VOLUME_UP", value="NEXT_TRACK")
            elif cmd_name == "BTN_SELECT":
                print(cmd_name)
                return Command(type="CLOSE_SOFTWARE", value="KEY_ENTER")
            elif cmd_name == "BTN_START":
                print(cmd_name)
                return Command(type="ENTER", value="KEY_ENTER")
            elif cmd_name == "BTN_HOME":
                print(cmd_name)
                return Command(type="NONE", value="KEY_ENTER")
            elif cmd_name == "BTN_THUMBL":
                print(cmd_name)
                return Command(type="NONE", value="PREVIOUS_TRACK")
            elif cmd_name == "BTN_THUMBR":
                print(cmd_name)
                return Command(type="NONE", value="NEXT_TRACK")

        # -------------------------------------------------------------
        # 2. D-PAD AND ANALOG STICKS (EV_ABS)
        # -------------------------------------------------------------
        elif event.type == ecodes.EV_ABS:

            # --- A. D-PAD / DIRECTIONAL PAD ---
            if cmd_name == "ABS_HAT0Y":  # D-Pad Vertical Axis

                if event.value < 0:
                    print(cmd_name + "   |    NORTH")
                    return Command(type="KEY_UP", value="VOLUME_UP")
                elif event.value > 0:
                    print(cmd_name + "    |    SUD")
                    return Command(type="KEY_DOWN", value="VOLUME_DOWN")

            elif cmd_name == "ABS_HAT0X":  # D-Pad Horizontal Axis
                if event.value < 0:
                    print(cmd_name + "     |    WEST")
                    return Command(type="KEY_LEFT", value="SEEK_BACKWARD")
                elif event.value > 0:
                    print(cmd_name + "      |      ESTH")
                    return Command(type="KEY_RIGHT", value="SEEK_FORWARD")

            # --- B. LEFT ANALOG STICK ---
            elif cmd_name == "ABS_Y":  # Left Stick Vertical
                if (event.value + self.offset) < -self.deadzone:
                    print(cmd_name + "   |   NORTH")
                    return Command(type="NAVIGATE", value="UP")
                elif (event.value + self.offset) > self.deadzone:
                    print(cmd_name + "  |  SUD")
                    return Command(type="NAVIGATE", value="DOWN")

            elif cmd_name == "ABS_X":  # Left Stick Horizontal
                if (event.value + self.offset) < -self.deadzone:
                    print(cmd_name + "    |    WEST")
                    return Command(type="NAVIGATE", value="LEFT")
                elif (event.value + self.offset) > self.deadzone:
                    print(cmd_name + "    |    ESTH")
                    return Command(type="NAVIGATE", value="RIGHT")

            # --- C. RIGHT ANALOG STICK ---
            elif cmd_name == "ABS_RY":  # Right Stick Vertical
                if (event.value + self.offset) < -self.deadzone:
                    print(cmd_name + "      |      NORTH")
                    return Command(type="SYSTEM_ACTION", value="BRIGHTNESS_UP")
                elif (event.value + self.offset) > self.deadzone:
                    print(cmd_name + "    |     SUD")
                    return Command(type="SYSTEM_ACTION", value="BRIGHTNESS_DOWN")

            elif cmd_name == "ABS_RX":  # Right Stick Vertical
                if (event.value + self.offset) < -self.deadzone:
                    print(cmd_name + "       |     WEST")
                    return Command(type="SYSTEM_ACTION", value="BRIGHTNESS_UP")
                elif (event.value + self.offset) > self.deadzone:
                    print(cmd_name + "    |    ESTH")
                    return Command(type="SYSTEM_ACTION", value="BRIGHTNESS_DOWN")

        return None

    def listen(self) -> None:
        """
        Main loop listening to hardware events from the gamepad device.
        Filter out system noise (EV_SYN/EV_MSC) and forward commands.
        """
        if not self.device:
            print("[ERROR] Gamepad device not initialized.")
            return

        print(f"[LISTENING] Gamepad loop started on device: {self.device.name}")
        for event in self.device.read_loop():
            # Skip synchronization and misc events
            if event.type in (ecodes.EV_SYN, ecodes.EV_MSC):
                continue

            command = self.translate_event_to_command(event)

            if command is not None:
                self.executor.execute(command)

