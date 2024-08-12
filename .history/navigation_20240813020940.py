import time
<<<<<<< HEAD
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
    loc = find_image_in_screenshots('navigation/wrapping.png', 'screenshots', threshold=0.8)
    if loc:
        logger.info('Wrapping detected.')
        return True
    return False

def find_targate():
    """
    查找屏幕上的 'stargate.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    logger.info('Finding targate...')
    loc = find_image_in_screenshots('navigation/stargate.png', 'screenshots', threshold=0.8)
    if loc:
        return loc
    return None

def click_targate():
    """
    尝试点击屏幕上的星门位置。
    """
    while True:
        try:
            position = find_targate()
            if position:
                x, y = position
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
    loc = find_image_in_screenshots('navigation/jumping.png', 'screenshots', threshold=0.8)
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
=======

import pyautogui
from loguru import logger


def is_wrapping():
    logger.info('is_wrapping')
    loc = pyautogui.locateOnScreen('navigation/wrapping.png', confidence=.8)
    if loc:
        logger.info('is_wrapping')
        return True


def find_targate():
    logger.info('find_targate')
    loc = pyautogui.locateOnScreen('navigation/stargate.png', confidence=.8)
    if loc:
        return loc

def click_targate():
    while True:
        try:
            x, y, w, h = find_targate()
            # 先按住d
            # 再点击那个星门
            # 再松开d
            pyautogui.click(x, y)
            pyautogui.keyDown('d')
            pyautogui.click(x, y, )
            pyautogui.keyUp('d')
            logger.info('pass_targate after')
            return
        except:
            continue


def is_jumping():
    logger.info('is_jumping')
    loc = pyautogui.locateOnScreen('navigation/jumping.png', confidence=.8)
    if loc:
        logger.info('is_jumping')
        return True


def run():
    while True:
        if not is_wrapping():
            click_targate()
            while True:
                # if not find_targate():
>>>>>>> 7b86bfbf847aeb1d29330f49612e575fedd3ae7d
                if is_jumping():
                    while True:
                        if find_targate():
                            click_targate()
                            break
                    break
<<<<<<< HEAD
                
if __name__ == '__main__':
    init()
    run()
=======
        else:
            pass


if __name__ == '__main__':
    run()
>>>>>>> 7b86bfbf847aeb1d29330f49612e575fedd3ae7d
