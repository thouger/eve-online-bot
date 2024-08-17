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
from libs.action import jump
from libs.times import *

@timing_decorator
def test():
    threshold = 0.8
    capture = False
    target_path = f"navigation/mac/stargate.png"


    # locations = test_template_matching(f"navigation/{client}/stargate.png", captrue=False,threshold=0.8)
    lower_color,upper_color = get_dominant_hsv_range(target_path)
    window = config.get_window()
    screenshot_path = "screenshots/full_screen.png"
    if capture:
        screenshot_path = capture_screen(window)

    # color
    locations = match_template_with_color_mask(img_path = screenshot_path, lower_color=lower_color, upper_color=upper_color,template_path =  target_path, threshold=threshold)
    # no colo
    # locations = match_template(img_path = screenshot_path,template_path =  target_path, threshold=threshold)
    if locations:
        locations = [(x * 2, y * 2) for (x, y) in locations]
        template_img = cv2.imread(target_path, cv2.IMREAD_COLOR)
        mark_matches(screenshot_path, locations, (template_img.shape[0], template_img.shape[1]), file_suffix="test")

    # locations = test_template_matching(f"navigation/mac/wrapping.png",False,threshold=0.8)
    if locations:
        logger.info(f"找到目标位置：{locations}")
        pyautogui.click(locations[0])

if __name__ == "__main__":
    import time
    # time.sleep(2)
    # main()
    # capture(save=True)
    test()
