import os
import sys
from PIL import Image
from init import *

# 获取当前脚本的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 获取上一级目录
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# 将上一级目录添加到 sys.path
sys.path.append(parent_dir)
from libs.screenshot import *
from libs.action import jump
from libs.times import *

def split_and_save_image(image, coords):
    """
    分割截图并保存每个区域。

    :param image: 原始截图的图像数据
    :param coords: 每个区域的坐标列表
    """
    img = Image.frombytes("RGB", image.size, image.rgb)

    save_dir = "screenshots"
    os.makedirs(save_dir, exist_ok=True)

    for region in coords:
        cropped_img = img.crop((
            region['left'],
            region['top'],
            region['left'] + region['width'],
            region['top'] + region['height']
        ))
        file_path = os.path.join(save_dir, f"{region['name']}.png")
        cropped_img.save(file_path)
        print(f"{region['name']} 区域截图已保存至 {file_path}")

def main():

    # """
    # 主函数：执行获取窗口、截图并分割保存的流程。
    # """
    # window = get_eve_window()
    
    # print(f"找到窗口: {window.title}, 大小: {window.width}x{window.height}, 位置: ({window.left}, {window.top})")

    # img = capture_window(window)

    # coords = calculate_grid_coordinates(window.width, window.height)

    # split_and_save_image(img, coords)

    target_image_path = "./navigation/jumping.png"
    screenshots_dir = "screenshots"

    test_image_matching_and_marking(target_image_path, screenshots_dir)

    # 查找目标图像位置
    # while True:
    #     position = find_image_in_screenshots(target_image_path, screenshots_dir,0.95)
    #     jump(position)

    # find_and_mark_images(target_image_path, screenshots_dir,0.95)

@timing_decorator
def test():
    # location = find_target("navigation\stargate.png", threshold=0.8)
    # print(f"location:{location}")
    test_template_matching("navigation\stargate.png", threshold=0.8)

if __name__ == "__main__":
    import time
    # time.sleep(2)
    # main()
    # capture(save=True)
    test()
