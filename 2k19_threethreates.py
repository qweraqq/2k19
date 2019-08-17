#!/usr/bin/python3
# -*- coding: utf-8 -*-
import win32gui
import win32api
import pyscreenshot as ImageGrab
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import logging
import re
import time
import pyautogui
import win32con
import ctypes
logging.basicConfig(level=logging.DEBUG)
SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


# https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# key code: https://gist.github.com/tracend/912308
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actual Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



def get_resolution():
    """
    获取屏幕分辨率
    :return:
    """
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


class WindowMgr:
    """Encapsulates some calls to the winapi for window management"""

    def __init__(self):
        """Constructor"""
        self._handle = None

    def find_window(self, class_name, window_name=None):
        """find a window by its class_name"""
        self._handle = win32gui.FindWindow(class_name, window_name)

    def _window_enum_callback(self, hwnd, wildcard):
        """Pass to win32gui.EnumWindows() to check all the opened windows"""
        if re.match(wildcard, str(win32gui.GetWindowText(hwnd))) is not None:
            self._handle = hwnd

    def find_window_wildcard(self, wildcard):
        """find a window whose title matches the wildcard regex"""
        self._handle = None
        win32gui.EnumWindows(self._window_enum_callback, wildcard)

    def set_foreground(self):
        """put the window in the foreground"""
        win32gui.SetForegroundWindow(self._handle)

    def get_handle(self):
        return self._handle


def get_window_info(wdname='.*2k19.*'):
    """
    get_window_info()函数返回2k19窗口信息(x1, y1, x2, y2)，
    (x1, y1)是窗口左上角的坐标，(x2, y2)是窗口右下角的坐标
    :return:
    """
    w = WindowMgr()
    w.find_window_wildcard(wdname)
    if w.get_handle() is None:
        return None
    else:
        w.set_foreground()
        return win32gui.GetWindowRect(w.get_handle())


def pass_and_shot():
    for _ in range(4):  # 传3次球
        win32api.keybd_event(98, 3, 0, 0)  # press 2
        time.sleep(0.1)
        win32api.keybd_event(98, 3, win32con.KEYEVENTF_KEYUP, 0)

        win32api.keybd_event(65, 30, 0, 0)  # press a
        time.sleep(0.5)
        win32api.keybd_event(65, 30, win32con.KEYEVENTF_KEYUP, 0)

        time.sleep(1)

    win32api.keybd_event(83, 31, 0, 0)  # press s
    time.sleep(0.58)
    win32api.keybd_event(83, 31, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.1)
    PressKey(0xC8)  # up arrow
    time.sleep(0.05)
    ReleaseKey(0xC8)


if __name__ == '__main__':
    logging.info(get_resolution())
    logging.info(get_window_info('NBA 2K19'))
    while True:
        pass_and_shot()
    # im = ImageGrab.grab(bbox=get_window_info('.*Sublime.*'))  # X1,Y1,X2,Y2
    # im.show()
