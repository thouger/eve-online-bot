import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *
import traceback

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
            jump_and_invisible(positions[0])
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
            jump_and_invisible(location)
            time.sleep(3)
            return True
        return False
    except Exception as e:
        logger.error(f"Error in jump_stargate: {e}")  # 使用logger而不是assert
        return False

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

def find_keepstar():
    """
    查找屏幕上的 'keepstar.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('keepstar')
    if loc:
        return loc
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
            jump_and_invisible(positions[0])
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
            jump_and_invisible(positions[0])
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

def find_align():
    """
    查找屏幕上的 'align.png' 图像。

    :return: 如果找到返回位置 (left, top)，否则返回 None。
    """
    loc = image.find_target('align',color=False)
    if loc:
        return loc
    return None

# 判断跃迁完毕后，过门是否成功，不完成继续点击星门
# 1. 首先判断跃迁不在了
# 2. 然后判断是否出现正在跳跃
def finish_wrapping():
    while not find_wrapping():
        time.sleep(1)
        is_jump = find_jumping() or find_not_found()
        logger.info(f'is_jump: {is_jump}')
        if is_jump:
            return True
        else:
            logger.info('等待跃迁完成...')
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
                            # 先调用 find_xxx 函数并将结果存储在变量中
                            found_station = find_station()
                            found_keepstar = find_keepstar()

                            if find_0_jump() or found_station or found_keepstar:
                                logger.info('跳跃完成。准备点击空间站。')
                                
                                # 根据 find_station 和 find_keepstar 的结果决定调用哪个函数
                                if found_station:
                                    # 将 found_station 作为参数传递给 click_station，避免重复调用 find_station
                                    click_station(found_station)
                                elif found_keepstar:
                                    click_keepstar(found_keepstar)
                                
                                if find_wrapping():
                                    logger.info('正在跃迁到下一个目标...')
                                    break
                            if find_stargate():
                                logger.info('找到下一个星门。')
                                found_next_stargate = True  # 设置标志，准备跳出所有循环
                                break
                        if found_next_stargate:  # 检查标志位并跳出上一层循环
                            logger.info('跳出内部循环，重新开始外层循环。')
                            break
                    elif find_0ms():
                        logger.info('找到0ms，准备点击空间站。')
                        click_station()
                    if found_next_stargate:  # 检查标志位并跳出再上一层循环
                        break
            # 还有一种是只朝向不跳跃
            # if find_align():
            #     found_next_stargate = True
            if found_next_stargate:  # 检查标志位并跳出再上一层循环
                break
        if found_next_stargate:  # 检查标志位并重新开始最外层循环
            logger.info('准备重新开始主循环。')
            continue
        
if __name__ == '__main__':
    # time.sleep(3)
    run()
    # print(find_0_jump() and find_station())
    # locations = find_1_jump()
    # if locations:
    #     print(locations)
    #     pyautogui.moveTo(locations[0][0],locations[0][1])
    # pyautogui.moveTo(locations[0],locations[1])