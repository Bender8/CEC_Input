#!/home/bender/Python/CEC_Input/.venv/bin/python3
import signal
import sys
import time

import cec
import uinput

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
        """Initializes the virtual keyboard with all required keys."""
        unique_keys = {k for val in KEY_MAP.values() for k in val["keys"]}
        unique_keys.update(CODE["keys"])
        return uinput.Device(list(unique_keys))

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
        # Always return to normal mode after a full attempt
        self.is_intercepting = False
        return

    def _emit_combo(self, keys):
        """Processes combo keys or single keys."""
        # Press all keys in the list (e.g., ALT then F4)
        for k in keys:
            self.device.emit(k, 1)
        time.sleep(KEY_DURATION)
        # Release all keys in reverse order (e.g., F4 then ALT)
        for k in reversed(keys):
            self.device.emit(k, 0)

    def _emit_sequence(self, keys):
        """Processes sequence keys or single keys."""
        for k in keys:
            self.device.emit_click(k)

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
        # Toggle Secret Mode
        if key == SEQUENCE_START:
            self._start_interception()
            return
        # Route keys based on current state
        if self.is_intercepting:
            self._process_secret_sequence(key)
        else:
            self._process_action(KEY_MAP.get(key))


def main():
    # Wait for hardware before starting the class
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
