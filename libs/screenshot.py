import os
import cv2
import mss
import numpy as np
import pygetwindow as gw
from loguru import logger
from libs.config import *
import pyautogui
from collections import Counter


def capture_screen(window=None, save_dir="screenshots", file_name="full_screen.png"):
    """
    捕获指定窗口的屏幕截图并保存。如果无法获取指定窗口的尺寸，则捕获当前屏幕的截图。
    
    :param window: 要捕获的窗口对象。如果为 None，则捕获整个屏幕。
    :param save_dir: 保存截图的目录
    :param file_name: 截图文件的名称
    :return: 截图文件的完整路径
    """
    os.makedirs(save_dir, exist_ok=True)

    with mss.mss() as sct:
        try:
            # 如果窗口对象存在，获取窗口的尺寸
            if window is not None:
                monitor = {
                    "top": window.top,
                    "left": window.left,
                    "width": window.width,
                    "height": window.height
                }
            else:
                # 如果窗口对象为 None，则捕获整个屏幕
                monitor = sct.monitors[1]  # 获取第一个显示器的尺寸
        except Exception as e:
            logger.error(f"Error in accessing window dimensions: {e}. Using full screen instead.")
            # 获取整个屏幕的尺寸
            monitor = sct.monitors[1]

        try:
            img = sct.grab(monitor)
            file_path = os.path.join(save_dir, file_name)
            mss.tools.to_png(img.rgb, img.size, output=file_path)
            # logger.info(f"截图已保存至 {file_path}")
            return file_path
        except Exception as e:
            logger.error(f"Error in capture_screen: {e}")
            return None
        
def match_template_with_color_mask(img_path, template_path, lower_color,upper_color, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)

    # 转换颜色范围为 HSV
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)
    
    # 创建颜色蒙版
    mask_img = cv2.inRange(img_hsv, lower_color, upper_color)
    mask_template = cv2.inRange(template_hsv, lower_color, upper_color)
    
    # 只保留与模板颜色相匹配的区域
    img_masked = cv2.bitwise_and(img, img, mask=mask_img)
    template_masked = cv2.bitwise_and(template, template, mask=mask_template)
    
    # 执行模板匹配
    result = cv2.matchTemplate(img_masked, template_masked, method)
    locations = np.where(result >= threshold)
    
    if locations[0].size == 0:
        # print(f"未找到 {template_path} 的匹配项。")
        return None
    
    matched_locations = list(zip(locations[1], locations[0]))

    if client == "mac":
        matched_locations = [(int(x // 2), int(y // 2)) for (x, y) in matched_locations]
    # logger.info(f"找到 {template_path} 的匹配项：{matched_locations}")
    return matched_locations

def match_template(img_path, template_path, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
    """
    对指定图像进行模板匹配。
    
    :param img_path: 需要搜索的图像文件路径
    :param template_path: 作为模板的图像文件路径
    :param method: OpenCV提供的模板匹配方法
    :param threshold: 匹配的阈值，只有高于此阈值的结果会被返回
    :param client: 指定客户端（例如 mac 时坐标需要缩小两倍）
    :return: 匹配到的位置坐标，如果没有找到合适的匹配则返回None
    """
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(img, template, method)
    locations = np.where(result >= threshold)
    if locations[0].size == 0:
        # logger.info(f"未找到{template_path}匹配项。")
        return None
    
    # 获取匹配的坐标对 (x, y)
    matched_locations = list(zip(locations[1], locations[0]))
    # 如果是 macOS，缩小坐标
    if client == "mac":
        matched_locations = [(int(x // 2), int(y // 2)) for (x, y) in matched_locations]
    # logger.info(f"找到{template_path}匹配项：{matched_locations}")
    return matched_locations


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
    for point in locations:
        top_left = point
        bottom_right = (top_left[0] + template_size[1], top_left[1] + template_size[0])
        cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    marked_path = os.path.join(output_dir, f"marked_{file_suffix}.png")
    cv2.imwrite(marked_path, img)
    # logger.info(f"标记图像已保存至 {marked_path}")

def find_target(template_path,color=True,threshold=0.8):
    """
    查找目标图像。
    
    :param template_path: 目标图像的路径
    :return: 匹配到的位置列表
    """
    window = config.get_window()
    screenshot_path = capture_screen(window)
    
    if color:
        lower_color,upper_color= get_dominant_hsv_range(template_path)
        locations = match_template_with_color_mask(img_path = screenshot_path, lower_color=lower_color, upper_color=upper_color, template_path =  template_path, threshold=threshold)
    else:
        locations = match_template(img_path = screenshot_path,template_path =  template_path, threshold=threshold)

    if locations:
        return locations
    else:
        # logger.info("未找到目标图像。")
        return False

def get_dominant_hsv_range(image_path, bins=30):
    # 读取图像
    image = cv2.imread(image_path)
    
    # 将图像从 BGR 转换为 HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 将 HSV 图像展平为一维数组
    h_values = hsv_image[:, :, 0].flatten()
    s_values = hsv_image[:, :, 1].flatten()
    v_values = hsv_image[:, :, 2].flatten()

    # 统计出现频率最高的HSV值
    hsv_counter = Counter(zip(h_values, s_values, v_values))
    dominant_hsv = hsv_counter.most_common(1)[0][0]  # 获取出现次数最多的HSV值
    
    # 根据最常见的颜色生成一个合理的范围
    lower_bound = np.array([max(dominant_hsv[0] - 10, 0), max(dominant_hsv[1] - 50, 0), max(dominant_hsv[2] - 50, 0)])
    upper_bound = np.array([min(dominant_hsv[0] + 10, 180), min(dominant_hsv[1] + 50, 255), min(dominant_hsv[2] + 50, 255)])
    
    # logger.info(f"np.array({lower_bound}), np.array({upper_bound})")
    
    return lower_bound, upper_bound