import win32gui, win32con
from random import choice
from time import sleep

key_map = {
    "0": 49,
    "1": 50,
    "2": 51,
    "3": 52,
    "4": 53,
    "5": 54,
    "6": 55,
    "7": 56,
    "8": 57,
    "9": 58,
    "F1": 112,
    "F2": 113,
    "F3": 114,
    "F4": 115,
    "F5": 116,
    "F6": 117,
    "F7": 118,
    "F8": 119,
    "F9": 120,
    "F10": 121,
    "F11": 122,
    "F12": 123,
    "F13": 124,
    "F14": 125,
    "F15": 126,
    "F16": 127,
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
    "BACKSPACE": 8,
    "TAB": 9,
    "TABLE": 9,
    "CLEAR": 12,
    "ENTER": 13,
    "SHIFT": 16,
    "CTRL": 17,
    "CONTROL": 17,
    "ALT": 18,
    "ALTER": 18,
    "PAUSE": 19,
    "BREAK": 19,
    "CAPSLK": 20,
    "CAPSLOCK": 20,
    "ESC": 27,
    "SPACE": 32,
    "SPACEBAR": 32,
    "PGUP": 33,
    "PAGEUP": 33,
    "PGDN": 34,
    "PAGEDOWN": 34,
    "END": 35,
    "HOME": 36,
    "LEFT": 37,
    "UP": 38,
    "RIGHT": 39,
    "DOWN": 40,
    "SELECT": 41,
    "PRTSC": 42,
    "PRINTSCREEN": 42,
    "SYSRQ": 42,
    "SYSTEMREQUEST": 42,
    "EXECUTE": 43,
    "SNAPSHOT": 44,
    "INSERT": 45,
    "DELETE": 46,
    "HELP": 47,
    "WIN": 91,
    "WINDOWS": 91,
    "NMLK": 144,
    "NUMLK": 144,
    "NUMLOCK": 144,
    "SCRLK": 145,
}


class PressController(object):
    def __init__(self, hander) -> None:
        self.hander = hander
        pass

    def key_up(self, key):
        win32gui.SendMessage(self.hander, win32con.WM_KEYUP, key_map[key], 0)
        win32gui.SendMessage(self.hander, win32con.WM_KEYUP, key_map[key], 0)

    def key_down(self, key):
        win32gui.SendMessage(self.hander, win32con.WM_KEYDOWN, key_map[key], 0)
        win32gui.SendMessage(self.hander, win32con.WM_KEYDOWN, key_map[key], 0)

    def hit_key(self, key, time=0.3):
        self.key_down(key)
        sleep(time)
        self.key_up(key)
        # print("hit key: ", key)

    def random_hit_key(self, key_list, time=0.3):
        self.hit_key(choice(key_list), time)

    def release_all_keys(self, key_list):
        for key in key_list:
            self.key_up(key)
