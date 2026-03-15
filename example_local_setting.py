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

SEQUENCE_START = 116
CODE_SEQUENCE = [1, 2, 3, 4]
CODE = [uinput.KEY_1, uinput.KEY_2, uinput.KEY_3, uinput.KEY_4, uinput.KEY_ENTER]
KEY_DURATION = 0.02
