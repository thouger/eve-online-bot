from libs.screenshot import *
import time

class Init:
    # 定义类变量用于存储点位信息
    center_point = None
    approaching_point = None
    jump_point = None
    
    def __init__(self):
        # 初始化类变量
        Init.center_point = (image.window_size['width'] // 2, image.window_size['height'] // 2)
        Init.approaching_point = Init.find_approaching()
        Init.jump_point = Init.find_jump()

    @staticmethod
    def find_approaching():
        """
        查找屏幕上的 'approaching.png' 图像。
        """
        while True:
            try:
                loc = image.find_target('approaching', color=False)
                if loc:
                    print("初始化接近按钮成功，坐标是：", loc[0])
                    return loc[0]
            except Exception as e:
                logger.error(f"Error in find_approaching: {e}")
            logger.info('未找到approaching.png')
            time.sleep(1)

    @staticmethod
    def find_jump():
        """
        查找屏幕上的 'jump.png' 图像。

        :return: 如果找到返回位置 (left, top)，否则返回 None。
        """
        try:
            loc = image.find_target('jump', color=False)
            if loc:
                print("初始化跳按钮成功，坐标是：", loc[0])
                return loc[0]
        except Exception as e:
            logger.error(f"Error in find_jump: {e}")
        logger.info('未找到jump.png')
        time.sleep(1)

# 初始化类变量
init = Init()