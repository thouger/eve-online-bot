import pyautogui
import time

"""
假隐跳，点击目标位置后按住 D 键，然后松开 D 键，最后按下 1 键。
"""
def jump(position):
    try:
        if position is None:
            print("No position provided for action.")
            return
        
        x, y = position
        pyautogui.click(x, y)
        pyautogui.keyDown('d')
        pyautogui.click(x, y)
        pyautogui.keyUp('d')
        # time.sleep(0.2)
        pyautogui.press('1')
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    
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