import time

import pyautogui

def displayMousePosition():
    try:
        while True:
            x, y = pyautogui.position()
            positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
            print(positionStr)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print('\n')

if __name__ == '__main__':
    # displayMousePosition()
    import pyautogui

    # 寻找窗口的位置和大小

    # 计算窗口占用的屏幕空间
    window_area = width * height
    pyautogui.click(x, y)
    print(x, y,)
