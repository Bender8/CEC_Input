import signal
import sys
import time

import cec
from evdev import UInput
from evdev import ecodes as e

try:
    from local_settings import (
        CODE,
        CODE_SEQUENCE,
        KEY_DURATION,
        KEY_MAP,
        SEQUENCE_START,
    )
except ImportError:
    print("local_settings.py not found!")
    sys.exit(1)


class CECInputBridge:
    def __init__(self):
        # 1. Internal State
        self.is_intercepting = False
        self.entered_sequence = []
        # 2. Virtual Device Setup
        self.device = self._uinput_setup()
        # 3. CEC Hardware Initialization
        self._cec_setup()

    def _uinput_setup(self):
        """Initializes the virtual keyboard using evdev."""
        unique_keys = {k for val in KEY_MAP.values() for k in val["keys"]}
        unique_keys.update(CODE["keys"])
        # Filter for integers to prevent Python 3.13 TypeErrors
        clean_keys = [k for k in unique_keys if isinstance(k, int)]
        capabilities = {e.EV_KEY: clean_keys}
        return UInput(capabilities, name="CEC-Input-Bridge")

    def _cec_setup(self):
        """Registers the class method as the CEC callback."""
        cec.init()
        cec.add_callback(self.handle_keypress, cec.EVENT_KEYPRESS)
        print("CEC Input Bridge initialized and listening.")

    def _start_interception(self):
        """Resets the buffer and enters Intercept Mode."""
        self.is_intercepting = True
        self.entered_sequence = []
        print("Intercept Mode: ON (Enter Code)")

    def _process_secret_sequence(self, key):
        """Handles key buffering for the passcode."""
        self.entered_sequence.append(key)
        if len(self.entered_sequence) != len(CODE_SEQUENCE):
            return

        if self.entered_sequence == CODE_SEQUENCE:
            print("Code Correct! Sending keys...")
            self._process_action(CODE)
        else:
            print("Code Incorrect.")

        self.is_intercepting = False

    def _emit_combo(self, keys):
        """Processes combo keys or single keys with duration control."""
        # Press all keys
        for k in keys:
            self.device.write(e.EV_KEY, k, 1)
        self.device.syn()

        time.sleep(KEY_DURATION)

        # Release all keys
        for k in reversed(keys):
            self.device.write(e.EV_KEY, k, 0)
        self.device.syn()

    def _emit_sequence(self, keys):
        """Processes sequence keys by reusing combo logic for each key."""
        for k in keys:
            self._emit_combo([k])
            time.sleep(KEY_DURATION)

    def _process_action(self, action):
        """The Router: Decides whether to 'Combo' or 'Sequence' the keys."""
        if not action:
            return

        action_type = action.get("type")
        keys = action.get("keys")

        if action_type == "combo":
            self._emit_combo(keys)
        elif action_type == "sequence":
            self._emit_sequence(keys)

    def handle_keypress(self, event, key, duration):
        """The main entry point for every CEC event."""
        if duration != 0:
            return

        if key == SEQUENCE_START:
            self._start_interception()
            return

        if self.is_intercepting:
            self._process_secret_sequence(key)
        else:
            self._process_action(KEY_MAP.get(key))


def main():
    while not cec.list_adapters():
        print("Waiting for CEC adapter...")
        time.sleep(5)

    CECInputBridge()

    try:
        signal.pause()
    except KeyboardInterrupt:
        print("\nShutting down...")


if __name__ == "__main__":
    main()
