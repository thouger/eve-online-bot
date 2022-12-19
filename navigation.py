import time

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
                if is_jumping():
                    while True:
                        if find_targate():
                            click_targate()
                            break
                    break
        else:
            pass


if __name__ == '__main__':
    run()
