import time

import cec


def on_keypress(event, key, duration):
    print(f"CEC button: {key} Duration: {duration}")


def main():
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
