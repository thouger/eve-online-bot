import time
import pyautogui
from loguru import logger
from libs.screenshot import *
from libs.config import *
from libs.action import *
import traceback
from typing import Optional, Tuple, Union

# 1. 配置参数的抽取
WAIT_TIME = {
    'JUMP_DELAY': 0.5,
    'ACTION_DELAY': 3,
    'RETRY_DELAY': 1,
    'WRAP_CHECK_DELAY': 1,
}

# 2. 参数验证
def validate_position(position: Optional[Tuple[int, int]]) -> bool:
    """
    验证位置参数是否有效
    """
    if not position or not isinstance(position, (list, tuple)) or len(position) < 2:
        return False
    return all(isinstance(coord, (int, float)) for coord in position)

# 3. 重复代码的抽象
def find_target(target_name: str, color: bool = True, threshold: float = 0.8) -> Optional[Tuple[int, int]]:
    """
    通用的目标查找函数
    """
    loc = image.find_target(target_name, color=color, threshold=threshold)
    return loc if loc else None

def click_structure(find_func, structure_name: str, positions: Optional[Tuple[int, int]] = None) -> bool:
    """
    通用的建筑点击函数
    """
    try:
        if positions is None:
            positions = find_func()
        
        if positions and validate_position(positions[0]):
            logger.info(f'正在点击{structure_name}')
            jump_and_invisible(positions[0])
            time.sleep(WAIT_TIME['ACTION_DELAY'])
            return True
        logger.warning(f'未找到有效的{structure_name}位置')
        return False
    except Exception as e:
        logger.error(f"点击{structure_name}时发生错误: {e}")
        return False

def find_wrapping() -> bool:
    """
    检查屏幕上是否存在 'wrapping.png' 图像。
    """
    return any(image.find_target(f'wrapping{i}') for i in (1, 2))

def find_stargate() -> Optional[Tuple[int, int]]:
    """
    查找屏幕上的星门并验证位置
    """
    locations = image.find_target('stargate', False)
    if locations:
        for location in locations:
            if location[0] > config.screen_size[0] / 2:
                return location
    return None

def click_targate(max_attempts: int = 3) -> bool:
    """
    尝试点击屏幕上的星门位置
    """
    attempt = 0
    while attempt < max_attempts:
        attempt += 1
        try:
            logger.info(f'正在尝试第{attempt}次点击星门')
            position = find_stargate()
            if position and validate_position(position):
                logger.info(f'找到星门位置：{position}')
                return jump_stargate(position)
            logger.warning('未找到有效的星门位置')
        except Exception as e:
            logger.error(f'点击星门时发生错误: {str(e)}')
            logger.debug(traceback.format_exc())
        time.sleep(WAIT_TIME['RETRY_DELAY'])
    return False

def jump_stargate(location: Tuple[int, int]) -> bool:
    """
    执行星门跳跃
    """
    if not validate_position(location):
        logger.error("无效的星门位置参数")
        return False
    
    try:
        time.sleep(WAIT_TIME['JUMP_DELAY'])
        jump_and_invisible(location)
        time.sleep(WAIT_TIME['ACTION_DELAY'])
        return True
    except Exception as e:
        logger.error(f"星门跳跃时发生错误: {e}")
        return False

# 简化的查找函数
find_jumping = lambda: bool(find_target('jumping'))
find_0_jump = lambda: find_target('0_jump', color=False, threshold=0.95)
find_1_jump = lambda: find_target('1_jump', color=False, threshold=0.95)
find_station = lambda: find_target('station')
find_keepstar = lambda: find_target('keepstar')
find_0ms = lambda: find_target('0ms', color=False)
find_not_found = lambda: find_target('not_found', color=False)
find_align = lambda: find_target('align', color=False)

# 使用通用click_structure函数的包装
def click_station(positions=None):
    return click_structure(find_station, "空间站", positions)

def click_keepstar(positions=None):
    return click_structure(find_keepstar, "星城", positions)

def finish_wrapping() -> bool:
    """
    检查跃迁完成状态
    """
    while not find_wrapping():
        time.sleep(WAIT_TIME['WRAP_CHECK_DELAY'])
        
        # 分别检查两个条件
        is_jumping = find_jumping()
        is_not_found = find_not_found()
        
        logger.info(f'跳跃状态详情 - jumping: {is_jumping}, not_found: {is_not_found}')
        
        # 如果任一条件为 True
        if is_jumping or is_not_found:
            if is_jumping:
                logger.info('检测到正在跳跃状态')
            if is_not_found:
                logger.info('检测到目标丢失状态')
            return True
            
        logger.info('等待跃迁完成...')
        click_targate()
    return False

def navigate_to_next_target() -> bool:
    """
    4. 循环控制的优化：将主要导航逻辑抽取为独立函数
    """
    try:
        if find_wrapping():
            logger.info('开始跃迁')
            if finish_wrapping():
                logger.info('跃迁完成，准备跳跃')
                time.sleep(WAIT_TIME['JUMP_DELAY'])
                
                found_station = find_station()
                found_keepstar = find_keepstar()
                
                if find_0_jump() or found_station or found_keepstar:
                    logger.info('跳跃完成，检查目标建筑')
                    if found_station:
                        return click_station(found_station)
                    elif found_keepstar:
                        return click_keepstar(found_keepstar)
                
                if find_stargate():
                    logger.info('找到下一个星门')
                    return True
            
            elif find_0ms():
                logger.info('找到0ms，准备点击空间站')
                return click_station()
    except Exception as e:
        logger.error(f"导航过程发生错误: {e}")
    return False

def run():
    """
    主循环函数
    """
    while True:
        try:
            logger.info('开始新的导航循环')
            if not click_targate():
                logger.error("无法点击星门，重试中...")
                continue
                
            if not navigate_to_next_target():
                logger.warning("导航到下一个目标失败，重试中...")
                time.sleep(WAIT_TIME['RETRY_DELAY'])
                
        except Exception as e:
            logger.error(f"主循环发生错误: {e}")
            logger.debug(traceback.format_exc())
            time.sleep(WAIT_TIME['RETRY_DELAY'])

if __name__ == '__main__':
    logger.info("启动游戏自动化脚本")
    run()