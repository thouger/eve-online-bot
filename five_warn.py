import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *

def find_no_scan_result():
    """
    检查屏幕上是否存在无扫描结果图像。
    当找不到图像时返回True并发出警告。

    :return: 如果找不到返回 True，找到返回 False。
    """
    loc = image.find_target('no_scan_result')
    if not loc:
        logger.warning('警告：未检测到扫描结果！')
        return True
    return False

def find_not_found():
    """
    检查屏幕上是否存在not_found图像。

    :return: 如果找到返回 True，否则返回 False。
    """
    loc = image.find_target('not_found')
    if not loc:
        logger.warning('警告：检测到not found！')
        return True
    return False

def click_and_press_v(x, y):
    """
    在指定坐标点击并按下v键
    
    参数:
    x (int): 目标x坐标
    y (int): 目标y坐标
    """
    try:
        logger.info(f'准备在坐标 ({x}, {y}) 执行操作')
        pyautogui.click(x, y)
        time.sleep(0.5)  # 等待点击动作完成
        pyautogui.press('v')
        logger.info('操作完成')
        
    except Exception as e:
        logger.error(f'操作失败: {str(e)}')
        raise

if __name__ == '__main__':
    # 测试函数
    # 给定坐标
    test_x, test_y = 1338, 735
    logger.info('程序将在3秒后开始运行...')
    time.sleep(3)
    
    while True:
        # 检查是否无扫描结果（找不到图片时警告）
        if find_no_scan_result():
            logger.warning('未检测到扫描结果，请注意检查！')
            time.sleep(1)  # 避免警告信息刷屏
            
        # 检查是否出现not found
        if find_not_found():
            logger.warning('检测到not found，请注意检查！')
            time.sleep(1)  # 避免警告信息刷屏
        
        click_and_press_v(test_x, test_y)
        time.sleep(5)