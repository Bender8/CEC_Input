import sys
import time

import cec
import uinput

# --- CONFIGURATION LOADING ---
try:
    from local_settings import CODE, CODE_SEQUENCE, KEY_MAP, SEQUENCE_START
except ImportError:
    print("local_settings.py not found!")
    sys.exit(1)


# Create the virtual keyboard
def uinput_setup(key_map, code_buttons):
    unique_keys = {k for key_list in key_map.values() for k in key_list}
    # Add the code keys to the set
    unique_keys.update(code_buttons)
    # Convert the set to a list and initialize the device
    return uinput.Device(list(unique_keys))


def on_keypress(event, key, duration):
    action = None
    # check record passcode
    global entered_sequence
    # Only process on initial press
    if duration != 0:
        return

    # 1. Check for the "Trigger" key (Yellow / 116) to reset/start sequence
    if key == SEQUENCE_START:
        entered_sequence = []
        print("Sequence reset. Enter code...")
        return

    # 2. If we are in the middle of entering a code
    if len(entered_sequence) < len(CODE_SEQUENCE):
        entered_sequence.append(key)
        # Check if the code is complete
        if len(entered_sequence) < len(CODE_SEQUENCE):
            return

        if entered_sequence == CODE_SEQUENCE:
            print("Code Correct! Sending keys...")
            for k in CODE:
                device.emit_click(k)
        else:
            print("Wrong code.")

        entered_sequence = list(range(len(CODE_SEQUENCE) + 1))  # Reset after attempt
        return  # Skip normal key mapping while entering code

    # 3. Normal Key Map Logic
    action = KEY_MAP.get(key)
    if not action:
        return
    # Handle single keys or combos
    if len(action) > 1:
        for k in action:
            device.emit(k, 1)
        for k in reversed(action):
            device.emit(k, 0)
    else:
        device.emit_click(action[0])


def main():
    global device
    device = uinput_setup(KEY_MAP, CODE)
    global entered_sequence
    entered_sequence = list(range(len(CODE_SEQUENCE) + 1))

    # Wait for CEC adapter to be available (useful for slow boots)
    while not cec.list_adapters():
        print("Waiting for CEC adapter...")
        time.sleep(5)

    # Initialize CEC and register the callback
    cec.init()
    cec.add_callback(on_keypress, cec.EVENT_KEYPRESS)
    print("CEC Input Bridge started.")

    # Keep the script alive
    try:
        while True:
            time.sleep(100)  # Long sleep to save CPU; events happen in background
    except KeyboardInterrupt:
        print("Shutting down...")


if __name__ == "__main__":
    main()
