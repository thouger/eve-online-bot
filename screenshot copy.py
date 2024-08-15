import os
import mss
import pygetwindow as gw
import cv2
import numpy as np
from loguru import logger
from config import config
from PIL import Image
from libs.times import *

def get_eve_window():
    """
    获取标题中包含'EVE - '的窗口。

    :return: 返回找到的第一个窗口对象
    """
    windows = gw.getWindowsWithTitle('EVE - ')
    logger.info(windows[0].title)
    if not windows:
        raise Exception("没有找到标题中包含'Cealym'的窗口。")
    return windows[0]

def get_window_with_title(title_keyword):
    """
    根据标题关键字获取窗口。

    :param title_keyword: 窗口标题中的关键字
    :return: 找到的第一个窗口对象
    """
    windows = gw.getWindowsWithTitle(title_keyword)
    if not windows:
        raise Exception(f"没有找到标题中包含'{title_keyword}'的窗口。")
    return windows[0]

def match_template_color(screenshot_img, target_img, threshold=0.8):
    """
    在彩色截图中匹配模板图像。

    :param screenshot_img: 截图图像
    :param target_img: 模板图像
    :param threshold: 匹配阈值
    :return: 匹配到的位置列表
    """
    # 在彩色图像上进行模板匹配
    result = cv2.matchTemplate(screenshot_img, target_img, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return locations


def find_and_mark_images(target_image_path, screenshots_dir, threshold=0.8):
    """
    在截图中查找目标图像的位置并标记所有匹配的位置。

    :param target_image_path: 目标图像路径
    :param screenshots_dir: 截图目录
    :param threshold: 匹配阈值
    """
    target_img = cv2.imread(target_image_path, cv2.IMREAD_COLOR)
    target_height, target_width = target_img.shape[:2]

    for root, _, files in os.walk(screenshots_dir):
        for file in files:
            file_path = os.path.join(root, file)

            # 检查文件名是否已经被标记过
            if file.startswith("marked_"):
                continue  # 如果文件已经被标记过，则跳过

            screenshot_img = cv2.imread(file_path, cv2.IMREAD_COLOR)

            # 使用抽象出的函数进行匹配
            locations = match_template_color(screenshot_img, target_img, threshold)

            if len(locations[0]) > 0:
                logger.info(f"Found target in {file_path} at positions with confidence > {threshold}")

                # 在所有匹配的位置上标记
                for pt in zip(*locations[::-1]):
                    bottom_right = (pt[0] + target_width, pt[1] + target_height)
                    cv2.rectangle(screenshot_img, pt, bottom_right, (0, 255, 0), 2)

                # 保存标记后的图像
                marked_file_path = os.path.join(root, f"marked_{file}")
                cv2.imwrite(marked_file_path, screenshot_img)
                # logger.info(f"Saved marked image at {marked_file_path}")



def find_image_in_screenshots(target_image_path, screenshots_dir, threshold=0.8):
    """
    在截图中查找目标图像的第一个匹配位置并对其进行标记保存。

    :param target_image_path: 目标图像路径
    :param screenshots_dir: 截图目录
    :param threshold: 匹配阈值
    :return: 目标图像的第一个匹配位置 (left, top) 或 None 如果未找到
    """
    capture("screenshots")
    target_img = cv2.imread(target_image_path, cv2.IMREAD_COLOR)
    target_height, target_width = target_img.shape[:2]

    for root, _, files in os.walk(screenshots_dir):
        for file in files:
            if("marked_" in file):
                continue
            file_path = os.path.join(root, file)
            screenshot_img = cv2.imread(file_path, cv2.IMREAD_COLOR)

            # 使用匹配模板进行查找
            locations = match_template_color(screenshot_img, target_img, threshold)

            if len(locations[0]) > 0:
                # 获取第一个匹配点的位置
                max_loc = (locations[1][0], locations[0][0])
                logger.info(f"Found target in {target_image_path} at {file_path} with confidence > {threshold}")

                # 在图像上绘制矩形框进行标记
                top_left = max_loc
                bottom_right = (top_left[0] + target_width, top_left[1] + target_height)
                cv2.rectangle(screenshot_img, top_left, bottom_right, (0, 255, 0), 2)

                # 保存标记后的图像
                marked_file_path = os.path.join(root, f"marked_{file}")
                cv2.imwrite(marked_file_path, screenshot_img)
                logger.info(f"Saved marked image at {marked_file_path}")

                return max_loc

    # logger.info(f"{target_image_path} image not found in screenshots.")
    return None
            
def test_image_matching_and_marking(target_image_path, screenshots_dir, threshold=0.8):
    """
    测试目标图像在截图中的匹配和标记功能。

    :param target_image_path: 目标图像路径
    :param screenshots_dir: 截图目录
    :param threshold: 匹配阈值
    """
    # 获取窗口并进行截图
    # try:
    #     window = get_window_with_title('EVE - ')  # 根据需要修改窗口标题关键字
    #     capture_window(window, screenshots_dir)
    #     logger.info("Captured window screenshot.")
    # except Exception as e:
    #     logger.info(f"Error capturing window: {e}")
    #     return

    # 查找目标图像
    logger.info("Testing find_image_in_screenshots...")
    match_position = find_image_in_screenshots(target_image_path, screenshots_dir, threshold)
    if match_position:
        logger.info(f"Match found at position: {match_position}")
    else:
        logger.info("No match found.")

    # 标记目标图像
    logger.info("Testing find_and_mark_images...")
    find_and_mark_images(target_image_path, screenshots_dir, threshold)

def capture(save_dir="screenshots", save=True, region=None):
    """
    获取带有特定标题的窗口，截取该窗口的截图，并计算窗口的分割区域坐标。
    :param save_dir: 保存截图的目录
    :param save: 是否保存截图分割后的图像
    :param region: 要截取的特定区域（如 '0_3'）
    :return: 截图的图像数据和分割区域的坐标列表
    """

    # 获取窗口信息
    window = config.get_window()

    # 截图
    img = capture_window(window, save_dir)

    # 计算分割坐标
    coords = calculate_grid_coordinates(window)

    if save:
        for coord in coords:
            if region and coord["name"] != f"region_{region}":
                continue  # 跳过不需要的区域

            # 裁剪并保存图像
            region_img = img.crop((coord["left"], coord["top"], coord["left"] + coord["width"], coord["top"] + coord["height"]))
            region_filename = os.path.join(save_dir, f"{coord['name']}.png")
            region_img.save(region_filename)

    return img

def calculate_grid_coordinates(window, rows=2, cols=4):
    """
    计算将窗口分割成指定行列的区域的坐标。

    :param window: 窗口对象。
    :param rows: 分割行数。
    :param cols: 分割列数。
    :return: 包含每个区域坐标的列表。
    """

    region_width = window.width // cols
    region_height = window.height // rows

    coords = []
    for row in range(rows):
        for col in range(cols):
            left = col * region_width
            top = row * region_height
            coords.append({
                "name": f"region_{row}_{col}",
                "left": left,
                "top": top,
                "width": region_width,
                "height": region_height
            })
    return coords

def capture_window(window, save_dir="screenshots"):
    """
    对指定窗口进行截图。

    :param window: 窗口对象。
    :param save_dir: 保存截图的目录。
    :return: 返回截图的PIL.Image对象。
    """

    with mss.mss() as sct:
        monitor = {
            "top": window.top,
            "left": window.left,
            "width": window.width,
            "height": window.height
        }
        img = sct.grab(monitor)


        # 速度慢，可切割
        # pil_img = Image.frombytes("RGB", img.size, img.rgb)
        # os.makedirs(save_dir, exist_ok=True)
        # file_path = os.path.join(save_dir, "full_window.png")
        # pil_img.save(file_path)
        # return pil_img

        # 速度快，不可切割
        os.makedirs(save_dir, exist_ok=True)
        file_path = os.path.join(save_dir, "full_window.png")
        mss.tools.to_png(img.rgb, img.size, output=file_path)
        # logger.info(f"完整窗口截图已保存至 {file_path}")
        return img