import pyautogui
import time
from libs.config import *
from pynput.mouse import Button, Controller
from libs.screenshot import *
from libs.init import *

def jump():
    while True:
        try:
            logger.info('正在点击跳跃。')
            
            # 处理不同的跳跃类型
            if jump_type == "covert":
                logger.info('执行隐跳。')
                if not covert_jump():
                    continue
            elif jump_type == "fake_covert":
                logger.info('执行假隐跳。')
                if not fake_covert_jump():
                    continue
            else:
                logger.warning(f"未知的跳跃类型: {jump_type}")
                time.sleep(1)
                continue
                
            pyautogui.moveTo(init.center_point)
            break
            
        except Exception as e:
            logger.critical(f"未预期的错误: {str(e)}")
            traceback.print_exc()
            time.sleep(1)
            continue

def triple_click(position):
    """执行三次点击操作"""
    x, y = position
    for _ in range(3):
        pyautogui.click(x, y)

"""
隐跳，点击jump位置后按下1键
"""
def covert_jump():
    try:
        if not init.jump_point:
            logger.error("未找到跳跃点坐标")
            return False
            
        triple_click(init.jump_point)
        time.sleep(0.7)
        pyautogui.press('1')
        return True
    except Exception as e:
        logger.error(f"隐跳过程中发生错误: {e}")
        return False
    
def fake_covert_jump():
    try:
        if not init.approaching_point:
            logger.error("未找到approaching坐标")
            return False
        if not init.jump_point:
            logger.error("未找到jump坐标")
            return False
            
        # 点击approaching按钮
        triple_click(init.approaching_point)
        # 移动到中心点避免鼠标遮挡
        pyautogui.moveTo(init.center_point)
        time.sleep(0.7)
        pyautogui.press('1')
        pyautogui.press('2')
        time.sleep(9)
        pyautogui.press('1')
        # 点击jump按钮
        triple_click(init.jump_point)
        return True
    except Exception as e:
        logger.error(f"假隐跳过程中发生错误: {e}")
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
    # show_mouse_position()
    pass