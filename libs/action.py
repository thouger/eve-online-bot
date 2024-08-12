import pyautogui

"""
在指定位置执行按住 'd' 键并点击的操作。

:param position: 要点击的坐标 (left, top)
"""
def jump(position):
    try:
        if position is None:
            print("No position provided for action.")
            return

        # 移动鼠标到指定位置
        pyautogui.moveTo(position[0], position[1])

        # 按住 'd' 键
        pyautogui.keyDown('d')

        # 单击鼠标
        pyautogui.click()

        # 松开 'd' 键
        pyautogui.keyUp('d')

        print(f"Performed action on position: {position}")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False