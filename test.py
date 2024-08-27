import os
import sys
from PIL import Image
import numpy as np

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# 将上一级目录添加到 sys.path
sys.path.append(parent_dir)
from libs.screenshot import *
from libs.action import jump_and_invisible
from libs.times import *
from libs.config import *
from navigation import *

@timing_decorator
def test():
    threshold = 0.8
    capture = False
    target = f"not_found"
    target_path = config.region[target][0]
    locations = image.find_target(target, color=False, threshold=threshold)
    if locations:
        template_img = cv2.imread(target_path, cv2.IMREAD_COLOR)
        image.mark_matches('screenshots/screenshot.png', locations, (template_img.shape[0], template_img.shape[1]), file_suffix="test")

    # locations = test_template_matching(f"navigation/mac/wrapping.png",False,threshold=0.8)
    if locations:
        logger.info(f"找到目标位置：{locations}")
        pyautogui.click(locations[0])

if __name__ == "__main__":
    import time
    # 如果输入参数第一个是xy
    if len(sys.argv) == 2:
        xy = sys.argv[1]
        show_mouse_position()
    # time.sleep(2)
    test()
    # find_0_jump()
