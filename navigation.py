import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *
import traceback

def find_wrapping():
    """
    检查屏幕上是否存在 'wrapping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    loc = image.find_target('wrapping1')
    if loc:
        return True
    else:
        loc = image.find_target('wrapping2')
        if loc:
            return True
    return False



def find_stargate():
    """
    查找屏幕上的 'stargate.png' 图像，并判断是否在屏幕的右半部分。

    :return: 如果找到并且位置在右半部分，返回位置 (left, top)，否则返回 None。
    """
    locations = image.find_target('stargate',False)
    if locations:
        for location in locations:
            if location[0] > config.screen_size[0] / 2:  # 判断 x 坐标是否在屏幕右半部分
                return location
    return None

def click_targate():
    """
    尝试点击屏幕上的星门位置。
    """
    while True:
        try:
            logger.info('正在点击星门。')
            position = find_stargate()
            print(position)
            jump_stargate(position)
            time.sleep(2)
            # 确保点击星门是成功的
            _find_wrapping = find_wrapping()
            if _find_wrapping:
                logger.info('点击星门成功。')
                break
        except Exception as e:
            traceback.print_exc()
            continue

def jump_stargate(location):
    try:
        if location:
            # 有时候还没跳转完就已经找到下一个星门了，所以这里先等一下
            time.sleep(0.5)
            # 鼠标移动到目标位置
            # pyautogui.moveTo(x, y)
            jump_and_invisible(location)
            time.sleep(3)
            return True
    except Exception as e:
        assert Exception(f"Error in click_targate: {e}")

def find_jumping():
    """
    检查屏幕上是否存在 'jumping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    loc = image.find_target('jumping')
    if loc:
        return True
    return False

def find_0_jump():
    """
    查找屏幕上的 '0_jump.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('0_jump',color=False,threshold=0.95)
    if loc:
        return loc
    return None

def find_1_jump():
    """
    查找屏幕上的 '1_jump.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('1_jump',color=False,threshold=0.95)
    if loc:
        return loc
    return None

def find_station():
    """
    查找屏幕上的 'station.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('station')
    if loc:
        return loc
    return None

def click_station():
    """
    尝试点击屏幕上的 station 位置。
    """
    try:
        positions = find_station()
        if positions:
            # 鼠标移动到目标位置
            # pyautogui.moveTo(x, y)
            jump_and_invisible(positions[0])
            time.sleep(3)
            return True
    except Exception as e:
        return False

def find_0ms():
    """
    查找屏幕上的 '0ms.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('0ms',color=False)
    if loc:
        return loc
    return None

def find_not_found():
    """
    查找屏幕上的 'not_found.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('not_found',color=False)
    if loc:
        return loc
    return None

# 判断过门是否成功
# 1. 首先判断跃迁不在了
# 2. 然后判断是否出现正在跳跃
def finish_wrapping():
    while not find_wrapping():
        time.sleep(1)
        if find_jumping() or find_not_found():
            return True
        else:
            click_targate()

def run():
    """
    运行主循环以执行星门导航。
    """
    while True:
        found_next_stargate = False  # 引入一个标志变量，控制click_targate的执行

        if not found_next_stargate:  # 只有在没有找到星门时，才执行click_targate
            click_targate()
            logger.info('开始寻找下一个星门。')

        while True:
            logger.info('等待跃迁...')
            if find_wrapping():
                logger.info('开始跃迁。')
                while True:
                    logger.info('等待跃迁完成...准备跳跃')
                    if finish_wrapping():
                        logger.info('跃迁完成。正在跳跃:')
                        time.sleep(0.5)
                        while True:
                            if find_0_jump() or find_station():
                                logger.info('跳跃完成。准备点击空间站。')
                                click_station()
                                if find_wrapping():
                                    break
                            if find_stargate():
                                found_next_stargate = True  # 设置标志，准备跳出所有循环
                                break
                        if found_next_stargate:  # 检查标志位并跳出上一层循环
                            break
                    elif find_0ms():
                        click_station()
                    if found_next_stargate:  # 检查标志位并跳出再上一层循环
                        break
            if found_next_stargate:  # 检查标志位并跳出再上一层循环
                break
        if found_next_stargate:  # 检查标志位并重新开始最外层循环
            continue
        
if __name__ == '__main__':
    time.sleep(3)
    run()
    # print(find_0_jump() and find_station())
    # locations = find_1_jump()
    # if locations:
    #     print(locations)
    #     pyautogui.moveTo(locations[0][0],locations[0][1])
    # pyautogui.moveTo(locations[0],locations[1])