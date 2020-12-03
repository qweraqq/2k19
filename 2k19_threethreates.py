#!/usr/bin/python3
# -*- coding: utf-8 -*-
import win32gui
import win32api
import pyscreenshot as ImageGrab
from PIL import Image
import logging
import re
import time
import win32con
import imagehash
logging.basicConfig(level=logging.INFO)


# https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# key code: https://gist.github.com/tracend/912308
# https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
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


def get_window_info(wdname='.*2k21.*'):
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

def is_quit():
    time.sleep(0.2)
    im = ImageGrab.grab(bbox=get_window_info('.*2K.*'))  # X1,Y1,X2,Y2
    im.save("tmp_quit.jpg")
    hash_tmp = imagehash.dhash(Image.open("tmp_quit.jpg"), hash_size=6)
    similarities = []
    for _ in range(9):
        hash_value = imagehash.dhash(Image.open(f"quit{_}.jpg"), hash_size=6)
        similary = 1 - (hash_value - hash_tmp)/len(hash_value.hash)**2
        similarities.append(similary)
    similary = max(similarities)
    logging.info(f"Quiting game similary = {similary}")
    return similary>=0.72

def is_triplethreat():
    time.sleep(0.2)
    im = ImageGrab.grab(bbox=get_window_info('.*2K.*'))  # X1,Y1,X2,Y2
    im.save("tmp_triplethreat.jpg")
    similarities = []
    hash_tmp = imagehash.dhash(Image.open("tmp_triplethreat.jpg"), hash_size=6)
    for _ in range(2):
        hash_value = imagehash.dhash(Image.open(f"triplethreat{_}.jpg"), hash_size=6)
        similary = 1 - (hash_value - hash_tmp)/len(hash_value.hash)**2
        similarities.append(similary)
    similary = max(similarities)
    logging.info(f"Triple Threat similary = {similary}")
    return similary > 0.8

def press_two():
    win32api.keybd_event(98, 3, 0, 0)  # press 2in32api.keybd_event(98, 3, 0, 0)  # press 2
    time.sleep(0.1)
    win32api.keybd_event(98, 3, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.1)


def press_up():
    win32api.keybd_event(0x26, 0xC8, 0, 0)  # press up
    time.sleep(0.05)
    win32api.keybd_event(0x26, 0xC8, win32con.KEYEVENTF_KEYUP, 0)

def pass_and_shot():
    for _ in range(3):  # 传3次球
        if is_triplethreat():
            logging.info("Triple threat")
            time.sleep(1)
            win32api.keybd_event(83, 31, 0, 0)  # press s
            time.sleep(0.68)
            win32api.keybd_event(83, 31, win32con.KEYEVENTF_KEYUP, 0)
            time.sleep(1)
        
        if is_quit():
            logging.info("Quiting game")
            time.sleep(0.5)
            press_up()

        press_two()
        win32api.keybd_event(65, 30, 0, 0)  # press a
        time.sleep(0.2)
        win32api.keybd_event(65, 30, win32con.KEYEVENTF_KEYUP, 0)

    time.sleep(1)
    win32api.keybd_event(83, 31, 0, 0)  # press s
    time.sleep(0.7)
    win32api.keybd_event(83, 31, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(0.5)
    press_up()


if __name__ == '__main__':
    logging.info(get_resolution())
    logging.info(get_window_info('NBA 2K21'))

    while True:
        pass_and_shot()
    is_quit()
    is_triplethreat()

