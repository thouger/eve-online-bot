import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *
import traceback
from libs.init import *


WAIT_TIME = {
    'JUMP_DELAY': 0.5,
    'ACTION_DELAY': 3,
    'RETRY_DELAY': 1,
}


def click_structure(find_func, structure_name):
    """
    通用的建筑点击函数
    :param find_func: 查找函数 (find_station 或 find_keepstar)
    :param structure_name: 建筑名称，用于日志
    :return: 是否成功点击
    """
    try:
        positions = find_func()
        if positions:
            # jump(positions[0])
            jump(positions[0])
            time.sleep(3)
            return True
        return False
    except Exception as e:
        logger.error(f"Error clicking {structure_name}: {e}")
        return False

def find_wrapping():
    """
    检查屏幕上是否存在 'wrapping.png' 图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    return any(image.find_target(f'wrapping{i}') for i in (1, 2))


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
            if not position:
                continue
            print(position)
            jump_stargate(position)
            break
            # time.sleep(2)
            # # 确保点击星门是成功的
            # _find_wrapping = find_wrapping()
            # if _find_wrapping:
            #     logger.info('点击星门成功。')
            #     break
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
            jump(location)
            time.sleep(3)
            return True
        return False
    except Exception as e:
        logger.error(f"Error in jump_stargate: {e}")  # 使用logger而不是assert
        return False

def click_jumping():
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

def find_keepstar():
    """
    查找屏幕上的 'keepstar.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    # loc = image.find_target('keepstar')
    # if loc:
    #     return loc
    return None

def click_station(positions=None):
    """
    尝试点击屏幕上的 station 位置。
    :param positions: 可选的坐标值，如果传入则不再调用 find_station。
    :return: 是否成功点击。
    """
    try:
        # 如果没有传入 positions，则调用 find_station 获取坐标
        if positions is None:
            positions = find_station()
        
        if positions:
            # 鼠标移动到目标位置
            # pyautogui.moveTo(x, y)
            # jump(positions[0])
            jump(positions[0])
            time.sleep(3)
            return True
        return False
    except Exception as e:
        return False
    
def click_keepstar(positions=None):
    """
    尝试点击屏幕上的 星城 位置。
    :param positions: 可选的坐标值，如果传入则不再调用 find_station。
    :return: 是否成功点击。
    """
    try:
        # 如果没有传入 positions，则调用 find_station 获取坐标
        if positions is None:
            positions = find_keepstar()
        
        if positions:
            # 鼠标移动到目标位置
            # pyautogui.moveTo(x, y)
            # jump(positions[0])
            jump(positions[0])
            time.sleep(3)
            return True
        return False
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

# 判断跃迁完毕后，过门是否成功，不完成继续点击星门
# 1. 首先判断跃迁不在了
# 2. 然后判断是否出现正在跳跃
def finish_wrapping():
    while not find_wrapping():
        time.sleep(1)
        # is_jump = find_approaching() or find_not_found()
        is_jump = Init.find_approaching()
        logger.info(f'is_jump: {is_jump}')
        if is_jump:
            return True
        else:
            logger.info('等待跃迁完成...')
            # click_targate()
            # jump()
            time.sleep(0.5)

def run():
    """
    运行主循环以执行星门导航。
    """
    while True:
        # 开始新的循环
        jump()
        logger.info('开始寻找下一个星门。')

        # 标记是否需要继续中层循环
        found_next_stargate = True
        
        # 等待跃迁并处理
        while found_next_stargate:
            logger.info('等待跃迁...')
            if find_wrapping():
                logger.info('开始跃迁。')
                
                # 等待跃迁完成
                while True:
                    logger.info('等待跃迁完成...准备跳跃')
                    if finish_wrapping():
                        logger.info('跃迁完成。正在跳跃:')
                        time.sleep(0.5)
                        
                        # 检查是否k可以准备跃迁
                        if Init.find_approaching():
                            logger.info('找到下一个星门，准备开始新循环。')
                            found_next_stargate = False  # 设置标志位以跳出中层循环
                            break  # 跳出内层循环
                        
                # 内层循环结束，检查是否需要跳出中层循环
                if not found_next_stargate:
                    break
                    
            # 检查0ms情况
            elif find_0ms():
                time.sleep(5)
                if find_0ms():
                    logger.info('找到0ms，准备开始新循环。')
                    break
                
        # 重新开始外层循环
        logger.info('准备重新开始主循环。')
        
if __name__ == '__main__':
    if config.client == 'mac':
        time.sleep(3)
    run()
    # jump()
    # Init()
