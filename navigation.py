import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from init import *

def is_wrapping():
    """
    检查屏幕上是否存在 'wrapping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    logger.info('Checking if wrapping...')
    loc = find_target('navigation/wrapping.png', threshold=0.8)
    if loc:
        logger.info('Wrapping detected.')
        return True
    return False

def find_stargate():
    """
    查找屏幕上的 'stargate.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    logger.info('Finding stargate...')
    loc = find_target('navigation/stargate.png', threshold=0.8)
    if loc:
        return loc
    return None

def click_targate():
    """
    尝试点击屏幕上的星门位置。
    """
    while True:
        try:
            position = find_stargate()
            if position:
                x, y = position
                # 鼠标移动到目标位置
                # pyautogui.moveTo(x, y)

                # 先按住d
                # 再点击那个星门
                # 再松开d
                pyautogui.click(x, y)
                pyautogui.keyDown('d')
                pyautogui.click(x, y)
                pyautogui.keyUp('d')
                logger.info('Passed through targate.')
                return
        except Exception as e:
            logger.error(f"Error in click_targate: {e}")
            continue

def is_jumping():
    """
    检查屏幕上是否存在 'jumping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    logger.info('Checking if jumping...')
    loc = find_target('navigation/jumping.png', threshold=0.8)
    if loc:
        print(f"Jumping detected at {loc}.")
        logger.info('Jumping detected.')
        return True
    return False

def run():
    """
    运行主循环以执行星门导航。
    """
    while True:
        # 开始先点击星门
        click_targate()
        if is_wrapping():
            while True:
                if is_jumping():
                    while True:
                        if find_stargate():
                            click_targate()
                            break
                    break
                
if __name__ == '__main__':
    init()
    run()