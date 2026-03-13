import time

import cec
import uinput

# Blue = 113 Red = 114 Green = 115 Yellow = 116
# Ok = 0 Back = 13
# up = 1 down = 2 left = 3 right = 4
KEY_MAP = {
    0: [uinput.KEY_ENTER],
    1: [uinput.KEY_UP],
    2: [uinput.KEY_DOWN],
    3: [uinput.KEY_LEFT],
    4: [uinput.KEY_RIGHT],
    13: [uinput.KEY_ESC],
    113: [uinput.KEY_LEFTMETA],
    114: [uinput.KEY_LEFTALT, uinput.KEY_F4],
}

device = None


# Create the virtual keyboard
def uinput_setup(key_map):
    unique_keys = {k for key_list in key_map.values() for k in key_list}
    # Convert the set to a list and initialize the device
    return uinput.Device(list(unique_keys))


def on_keypress(event, key, duration):
    action = None
    # ignore key release events
    if duration == 0:
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
    device = uinput_setup(KEY_MAP)

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
