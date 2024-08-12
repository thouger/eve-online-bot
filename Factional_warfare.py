import pyautogui
from loguru import logger


def find_NVY():
    logger.info('is_NVY')

    loc = pyautogui.locateOnScreen('Factional_warfare/Medium NVY.png', confidence=.8)
    if loc:
        logger.info('find Medium NVY')
        return loc
    else:
        logger.info('not find Medium NVY')

    loc = pyautogui.locateOnScreen('Factional_warfare/Small NVY.png', confidence=.8)
    if loc:
        logger.info('find Small NVY')
        return loc
    else:
        logger.info('not find Small NVY')

    return False

def wrap_NVY(loc):
    logger.info('wrap_NVY')
    x, y, w, h = loc
    #右键点击
    pyautogui.click(x, y, button='left')
    pyautogui.click(x, y, button='right')
    loc = pyautogui.locateOnScreen('Factional_warfare/wrap_0.png', confidence=.8)
    x, y, w, h = loc
    #左键点击
    pyautogui.click(x, y, button='left')


    #进入轨道
    loc = pyautogui.locateOnScreen('Factional_warfare/加速轨道.png', confidence=.8)
    x, y, w, h = loc
    #按住d再按x,y坐标
    pyautogui.keyDown('d')
    pyautogui.click(x, y, button='left')
    pyautogui.keyUp('d')


def main():
    find_nvy = find_NVY()
    if find_nvy:
        wrap_NVY(find_nvy)

if __name__ == '__main__':
    main()