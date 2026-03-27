from evdev import ecodes as e

# Blue = 113 Red = 114 Green = 115 Yellow = 116
# Ok = 0 Back = 13
# up = 1 down = 2 left = 3 right = 4

KEY_DURATION = 0.02

# Updated to use evdev ecodes (e.KEY_XXX)
KEY_MAP = {
    0: {"type": "combo", "keys": [e.KEY_ENTER]},
    1: {"type": "combo", "keys": [e.KEY_UP]},
    2: {"type": "combo", "keys": [e.KEY_DOWN]},
    3: {"type": "combo", "keys": [e.KEY_LEFT]},
    4: {"type": "combo", "keys": [e.KEY_RIGHT]},
    13: {"type": "combo", "keys": [e.KEY_ESC]},
    113: {"type": "combo", "keys": [e.KEY_LEFTMETA]},
    114: {"type": "combo", "keys": [e.KEY_LEFTALT, e.KEY_F4]},
    115: {"type": "combo", "keys": [e.KEY_LEFTSHIFT, e.KEY_ENTER]},
}

SEQUENCE_START = 116
CODE_SEQUENCE = [1, 2, 3, 4]
CODE = {
    "type": "sequence",
    "keys": [e.KEY_1, e.KEY_2, e.KEY_2, e.KEY_4],
}
