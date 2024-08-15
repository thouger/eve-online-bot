import win32api
import win32con
import pyautogui
from loguru import logger
from libs.screenshot import *
import time

def find_not_found():
    """
    查找屏幕上的 'not_found.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    logger.info('Finding not found...')
    loc = find_target('Factional_warfare/not_found.png', threshold=0.8)
    if loc:
        return loc
    return None

def find_five_degrees():
    """
    查找屏幕上的 '5_degrees.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    logger.info('Finding 5 degrees...')
    loc = find_target('Factional_warfare/5_degrees.png', threshold=0.8, activation=True)
    if loc:
        return loc
    return None

def click_five_degrees():
    """
    点击屏幕上的 '5_degrees.png' 图像，同时按住 'v' 键。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = find_five_degrees()
    if loc:
        x, y = loc
        # 移动到目标位置
        pyautogui.moveTo(x, y+80)

        # 按下 'v' 键
        win32api.keybd_event(0x56, 0, 0, 0)  # 0x56 是 'v' 键的虚拟键码
        time.sleep(0.1)  # 添加短暂延迟，确保按键按下被识别

        # 点击鼠标左键
        pyautogui.click()

        # 松开 'v' 键
        win32api.keybd_event(0x56, 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)  # 添加短暂延迟，确保按键释放被识别

        return loc
    return None

def main():
    while True:
        try:
            loc = click_five_degrees()
            if not find_not_found():
                logger.info('Not found, waiting...')
            else:
                logger.info('Found, waiting...')
        except Exception as e:
            logger.error(f"Error in main: {e}")
            continue

if __name__ == '__main__':
    main()
