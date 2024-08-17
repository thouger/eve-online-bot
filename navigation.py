import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *

def is_wrapping():
    """
    检查屏幕上是否存在 'wrapping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    loc = find_target(f'navigation/{client}/warpping1.png')
    if loc:
        return True
    else:
        loc = find_target(f'navigation/{client}/warpping2.png')
        if loc:
            return True
    return False


def find_stargate():
    """
    查找屏幕上的 'stargate.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = find_target(f'navigation/{client}/stargate.png')
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
            jump_stargate(position)
            # 点击完，移动到屏幕中心，避免鼠标遮挡
            pyautogui.moveTo(671,452)
            break
        except Exception as e:
            continue

def jump_stargate(positions):
    try:
        if positions:
            # 鼠标移动到目标位置
            # pyautogui.moveTo(x, y)

            # 先按住d
            # 再点击那个星门
            # 再松开d
            for _ in range(3):
                jump(positions[0])
            return True
    except Exception as e:
        assert Exception(f"Error in click_targate: {e}")

def is_jumping():
    """
    检查屏幕上是否存在 'jumping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    loc = find_target(f'navigation/{client}/jumping.png')
    if loc:
        print(f"Jumping detected at {loc}.")
        return True
    return False

def find_1_jump():
    """
    查找屏幕上的 '1_jump.png' 图像，连续三次找到图像才返回位置。

    :return: 如果连续三次都找到图像，返回位置 (left, top)，否则返回 None。
    """
    for i in range(3):
        loc = find_target(f'navigation/{client}/1_jump.png',color=False)
        if loc is None:
            logger.info(f"第 {i+1} 次查找失败。")
            return None
        logger.info(f"第 {i+1} 次找到 1_jump 图像：{loc}")
    
    # 如果连续三次都成功找到，返回位置
    return loc

def find_station():
    """
    查找屏幕上的 'station.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = find_target(f'navigation/{client}/station.png')
    if loc:
        return loc
    return None

def click_station():
    """
    尝试点击屏幕上的 station 位置。
    """
    for i in range(5):
        try:
            positions = find_station()
            if positions:
                # 鼠标移动到目标位置
                # pyautogui.moveTo(x, y)
                jump(positions[0])
                return True
        except Exception as e:
            continue

def find_0ms():
    """
    查找屏幕上的 '0ms.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = find_target(f'navigation/{client}/0ms.png',color=False)
    if loc:
        return loc
    return None

def find_not_found():
    """
    查找屏幕上的 'not_found.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = find_target(f'navigation/{client}/not_found.png',color=False)
    if loc:
        return loc
    return None

def run():
    """
    运行主循环以执行星门导航。
    """
    while True:
        # 开始先点击星门
        click_targate()
        logger.info('开始寻找下一个星门。')
        # 有几率找不到跃迁，所以需要设个计数器
        # 点击星门是一个死循环，所以点击完星门，一定是在等跃迁
        while True:
            logger.info('等待跃迁...')
            if is_wrapping():
                logger.info('开始跃迁。')
                # 趁着跃迁的时候，寻找是否还剩下一跳了
                exist_1_jump = find_1_jump()
                if exist_1_jump:
                    logger.info('只剩下一跳了。')
                while True:
                    logger.info('等待跃迁完成...准备跳跃')
                    # 当找不到星门，或者速度为 0 时，就认为是跃迁完成
                    # if not stargate_locations or find_0ms():
                    # if not find_stargate():
                    if find_not_found():
                        logger.info('跃迁完成。正在跳跃:')
                        # 跳跃中,点击星门或者点击空间站
                        while True:
                            if exist_1_jump and find_station():
                                logger.info('跳跃完成。准备点击空间站。')
                                click_station()
                                if is_wrapping():
                                    break
                            else:
                                stargate_locations = find_stargate()
                                if stargate_locations:
                                    logger.info('跳跃完成。准备点击下一个星门。')
                                    jump_stargate(stargate_locations)
                                    break
                
if __name__ == '__main__':
    # run()
    # print(find_1_jump())
    print(click_station())