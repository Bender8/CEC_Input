import uinput

# Blue = 113 Red = 114 Green = 115 Yellow = 116
# Ok = 0 Back = 13
# up = 1 down = 2 left = 3 right = 4

KEY_DURATION = 0.02
KEY_MAP = {
    0: {"type": "combo", "keys": [uinput.KEY_ENTER]},
    1: {"type": "combo", "keys": [uinput.KEY_UP]},
    2: {"type": "combo", "keys": [uinput.KEY_DOWN]},
    3: {"type": "combo", "keys": [uinput.KEY_LEFT]},
    4: {"type": "combo", "keys": [uinput.KEY_RIGHT]},
    13: {"type": "combo", "keys": [uinput.KEY_ESC]},
    113: {"type": "combo", "keys": [uinput.KEY_LEFTMETA]},
    114: {"type": "combo", "keys": [uinput.KEY_LEFTALT, uinput.KEY_F4]},
    115: {"type": "combo", "keys": [uinput.KEY_LEFTSHIFT, uinput.KEY_ENTER]},
}

SEQUENCE_START = 116
CODE_SEQUENCE = [1, 2, 3, 4]
CODE = {
    "type": "sequence",
    "keys": [uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4],
}
