import pyautogui
import time
from libs.config import *

"""
假隐跳，点击目标位置后按住 D 键，然后松开 D 键，最后按下 1 键。
"""
def jump_and_invisible(position):
    try:
        jump(position)
        # time.sleep(0.1)
        pyautogui.press('1')
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
def jump(position):
    try:
        if position is None:
            print("No position provided for action.")
            return False

        x, y = position

        # 移动鼠标到指定坐标
        pyautogui.moveTo(x, y)

        # 按下鼠标左键
        pyautogui.mouseDown(button='left')

        # 移动鼠标到正上方（y+100）
        pyautogui.moveTo(x, y - 500, duration=0.2)

        # 松开鼠标左键
        pyautogui.mouseUp(button='left')

        # 点击完，移动到屏幕中心，避免鼠标遮挡
        # todo: 需要根据屏幕分辨率调整
        # pyautogui.moveTo(671, 452)

        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# def jump(position):
#     try:
#         if position is None:
#             print("No position provided for action.")
#             return
#         x, y = position
#         pyautogui.moveTo(x, y)

#         # 按下 'd' 键
#         pyautogui.keyDown('d')

#         # 确保 'd' 键已经被按下，立即双击
#         pyautogui.mouseDown(button='left')  # 按下鼠标左键
#         pyautogui.mouseUp(button='left')    # 松开鼠标左键
#         pyautogui.mouseDown(button='left')  # 再次按下鼠标左键
#         pyautogui.mouseUp(button='left')    # 再次松开鼠标左键
#         pyautogui.mouseDown(button='left')  # 再次按下鼠标左键
#         pyautogui.mouseUp(button='left')    # 再次松开鼠标左键
#         pyautogui.mouseDown(button='left')  # 再次按下鼠标左键
#         pyautogui.mouseUp(button='left')    # 再次松开鼠标左键

#         # 松开 'd' 键
#         pyautogui.keyUp('d')

#         # 点击完，移动到屏幕中心，避免鼠标遮挡
#         # todo: 需要根据屏幕分辨率调整
#         pyautogui.moveTo(671,452)
#         return True
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return False
    
def show_mouse_position(interval=0.1):
    """
    显示当前鼠标的坐标。

    :param interval: 刷新间隔时间（秒），默认为0.1秒
    """
    print("按 Ctrl + C 停止显示鼠标坐标。\n")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"鼠标坐标: X={x}, Y={y}", end="\r")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n停止显示鼠标坐标。")

if __name__ == '__main__':
    show_mouse_position()