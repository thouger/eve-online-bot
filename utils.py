import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication
import win32gui
from PyQt5.QtGui import *
import sys

debug= True
def screenshot(window_name='eve - thouger'):


    hwnd = win32gui.FindWindow(None, window_name)
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    return img

def qtpixmap_to_cvimg(qimg):

    temp_shape = (qimg.height(), qimg.bytesPerLine() * 8 // qimg.depth())
    temp_shape += (4,)
    ptr = qimg.bits()
    ptr.setsize(qimg.byteCount())
    result = np.array(ptr, dtype=np.uint8).reshape(temp_shape)
    result = result[..., :3]

    return result

def all_windows_by_qt():
    import win32gui
    hwnd_title = dict()

    def get_all_hwnd(hwnd, mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})

    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
        if t != "":
            print(h, t)

def find_window(keyword):
    """
    Find window by keyword
    :param keyword: keyword
    :return: window
    """
    windows = find_all_windows()
    for window in windows:
        if keyword in win32gui.GetWindowText(window):
            return window
    return None

def find_all_windows():
    import win32gui
    """
    Find all windows
    :return: windows
    """
    windows = []
    def callback(hwnd, extra):
        windows.append(hwnd)
    win32gui.EnumWindows(callback, None)
    return windows

def match(template:str,window_name='eve - cealym',threshold=0.8):
    img_rgb = qtpixmap_to_cvimg(screenshot(window_name))
    img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)
    template = cv2.imread(template)
    w, h = template.shape[:-1]

    res = cv2.matchTemplate(img_rgb, template, cv2.TM_CCOEFF_NORMED)
    threshold = threshold
    loc = np.where(res >= threshold)

    matchs = []
    for pt in zip(*loc[::-1]):  # Switch collumns and rows
        matchs.append((pt[0]+w, pt[1]+h))
    if debug:
        for pt in zip(*loc[::-1]):  # Switch collumns and rows
            matchs.append((pt[0], pt[1], w, h))
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
        cv2.imwrite('match.png', img_rgb)
        # cv2.imshow('output',img_rgb)
        # cv2.waitKey(0)
    return matchs


if __name__ == '__main__':
    all_windows_by_qt()