import os
import cv2
import mss
import numpy as np
import pygetwindow as gw
from loguru import logger
from config import config

def get_window(title="EVE - "):
    """
    获取指定标题的窗口对象。
    
    :param title: 窗口的标题关键词
    :return: 返回找到的第一个窗口对象
    """
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"未找到标题中包含'{title}'的窗口。")
    logger.info(f"找到窗口：{windows[0].title}")
    return windows[0]

def capture_screen(window, save_dir="screenshots", file_name="full_screen.png"):
    """
    捕获指定窗口的屏幕截图并保存。
    
    :param window: 要捕获的窗口对象
    :param save_dir: 保存截图的目录
    :param file_name: 截图文件的名称
    :return: 截图文件的完整路径
    """
    os.makedirs(save_dir, exist_ok=True)
    with mss.mss() as sct:
        monitor = {"top": window.top, "left": window.left, "width": window.width, "height": window.height}
        img = sct.grab(monitor)
        file_path = os.path.join(save_dir, file_name)
        while True:
            try:
                mss.tools.to_png(img.rgb, img.size, output=file_path)
                break
            except Exception as e:
                logger.error(f"Error in capture_screen: {e}")
                continue
        # logger.info(f"截图已保存至 {file_path}")
        return file_path

def match_template(img_path, template_path, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
    """
    对指定图像进行模板匹配。
    
    :param img_path: 需要搜索的图像文件路径
    :param template_path: 作为模板的图像文件路径
    :param method: OpenCV提供的模板匹配方法
    :param threshold: 匹配的阈值，只有高于此阈值的结果会被返回
    :return: 匹配到的位置坐标，如果没有找到合适的匹配则返回None
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(img, template, method)
    locations = np.where(result >= threshold)
    if locations[0].size == 0:
        logger.info("未找到匹配项。")
        return None
    return locations

def mark_matches(img_path, locations, template_size, output_dir="screenshots", file_suffix=""):
    """
    在图像中标记匹配的位置并保存。
    
    :param img_path: 被搜索的原始图像路径
    :param locations: 匹配到的坐标位置列表
    :param template_size: 模板图像的尺寸（高度，宽度）
    :param output_dir: 标记后的图像保存目录
    :param file_suffix: 保存的文件后缀名，用于标识文件
    """
    img = cv2.imread(img_path)
    for point in zip(*locations[::-1]):  # 反转 x, y 坐标位置
        top_left = point
        bottom_right = (top_left[0] + template_size[1], top_left[1] + template_size[0])
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    marked_path = os.path.join(output_dir, f"marked_{file_suffix}.png")
    cv2.imwrite(marked_path, img)
    logger.info(f"标记图像已保存至 {marked_path}")

def find_target(target,threshold=0.8):
    """
    查找目标图像。
    
    :param target: 目标图像的路径
    :return: 匹配到的位置列表
    """
    window = get_window()
    screenshot_path = capture_screen(window)
    locations = match_template(img_path = screenshot_path, template_path = target,threshold=threshold)
    if locations:
        # logger.info("找到目标图像。")
        # 注意: OpenCV的坐标是 (y, x) 而不是 (x, y)
        max_loc = (locations[1][0], locations[0][0])
        return max_loc
    else:
        # logger.info("未找到目标图像。")
        return False

def test_template_matching(target_path,threshold=0.8):
    """
    测试模板匹配功能。
    
    执行全屏截图并对指定模板进行匹配测试，验证匹配的正确性并标记匹配位置。
    """
    window = get_window()
    screenshot_path = capture_screen(window)
    locations = match_template(img_path = screenshot_path,template_path =  target_path, threshold=threshold)
    if locations:
        template_img = cv2.imread(target_path, cv2.IMREAD_COLOR)
        mark_matches(screenshot_path, locations, (template_img.shape[0], template_img.shape[1]), file_suffix="test")
        logger.info("匹配成功并标记。")
    else:
        logger.info("测试中未找到匹配项。")

if __name__ == "__main__":
    test_template_matching()
