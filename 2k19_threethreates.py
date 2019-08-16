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

logging.basicConfig(level=logging.DEBUG)


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


def pass_and_shot(m, k):
    for _ in range(4):  # 传四次球
        k.tap_key('2')
        k.press_key('A')
        time.sleep(0.5)
        k.release_key('A')
        k.press_key(k.right_key)
        time.sleep(0.8)
        k.release_key(k.right_key)
    k.press_key('S')
    time.sleep(0.5)
    k.release_key('S')


if __name__ == '__main__':
    m = PyMouse()
    k = PyKeyboard()
    logging.info(get_resolution())
    logging.info(get_window_info('.*Sublime.*'))
    pass_and_shot(m, k)
    # im = ImageGrab.grab(bbox=get_window_info('.*Sublime.*'))  # X1,Y1,X2,Y2
    # im.show()
