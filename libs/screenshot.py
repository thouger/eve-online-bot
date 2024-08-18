import os
import cv2
import mss
import numpy as np
import pygetwindow as gw
from loguru import logger
import pyautogui
from collections import Counter
from libs.config import *

class ImageProcessor:
    def __init__(self, config):
        self.config = config
        self.window_size = self.config.window_size

    def capture_screen(self, category_key):
        """
        捕获指定屏幕区域的截图并保存。区域由Config类的get_target_area方法决定。

        :param category_key: 区域的键值，用于获取Config中的区域范围。
        :return: 截图文件的完整路径和相对于全屏幕的偏移量 (start_x, start_y)
        """
        save_dir = "screenshots"
        file_name = f"screenshot.png"
        os.makedirs(save_dir, exist_ok=True)

        # 获取指定区域的坐标
        start_x, start_y, end_x, end_y = self.get_target_area(category_key)
        
        # 输出截图区域信息
        # logger.info(f"capture_screen_func - {category_key}: start_x={start_x}, start_y={start_y}, end_x={end_x}, end_y={end_y}")

        with mss.mss() as sct:
            monitor = {
                "top": start_y,
                "left": start_x,
                "width": end_x - start_x,
                "height": end_y - start_y
            }

            img = sct.grab(monitor)
            file_path = os.path.join(save_dir, file_name)
            mss.tools.to_png(img.rgb, img.size, output=file_path)

        # 返回截图的路径和区域的偏移量
        return file_path, (start_x, start_y)
    
    def get_target_area(self, category_key):
        """
        获取给定分类对应的屏幕区域范围。

        :param category_key: 区域的键值，如 'station'
        :return: 屏幕区域范围的坐标 (start_x, start_y, end_x, end_y)
        """
        screen_width, screen_height = self.config.window_size['width'], self.config.window_size['height']

        if category_key in self.config.region:
            # 直接获取该键对应的区域坐标
            _, area = self.config.region[category_key]
            start_x = int(area[0] * screen_width)
            start_y = int(area[1] * screen_height)
            end_x = int(area[2] * screen_width)
            end_y = int(area[3] * screen_height)
            # logger.info(f"get_target_area - {category_key}: start_x={start_x}, start_y={start_y}, end_x={end_x}, end_y={end_y}")
            return (start_x, start_y, end_x, end_y)
        
        # 如果没有找到，默认返回全屏范围
        return (0, 0, screen_width, screen_height)

    def match_template_with_color_mask(self, img_path, template_path, lower_color, upper_color, region_offset, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)

        img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        template_hsv = cv2.cvtColor(template, cv2.COLOR_BGR2HSV)

        mask_img = cv2.inRange(img_hsv, lower_color, upper_color)
        mask_template = cv2.inRange(template_hsv, lower_color, upper_color)

        img_masked = cv2.bitwise_and(img, img, mask=mask_img)
        template_masked = cv2.bitwise_and(template, template, mask=mask_template)

        result = cv2.matchTemplate(img_masked, template_masked, method)
        locations = np.where(result >= threshold)

        if locations[0].size == 0:
            return None

        matched_locations = list(zip(locations[1], locations[0]))

        # 如果在 macOS 上，需要先缩放匹配位置
        if self.config.client == "mac":
            matched_locations = [(int(x // 2), int(y // 2)) for (x, y) in matched_locations]

        # 调整匹配位置以适应全屏幕坐标
        adjusted_locations = [(x + region_offset[0], y + region_offset[1]) for (x, y) in matched_locations]

        # # 输出匹配的原始位置
        # logger.info(f"match_template_with_color_mask - Matched Locations: {matched_locations}")
        # # 输出调整后的位置
        # logger.info(f"match_template_with_color_mask - Adjusted Locations: {adjusted_locations}")

        return adjusted_locations


    def match_template(self, img_path, template_path, region_offset, method=cv2.TM_CCOEFF_NORMED, threshold=0.8):
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        result = cv2.matchTemplate(img, template, method)
        locations = np.where(result >= threshold)
        
        if locations[0].size == 0:
            return None

        matched_locations = list(zip(locations[1], locations[0]))

        if self.config.client == "mac":
            adjusted_locations = [(int(x // 2), int(y // 2)) for (x, y) in matched_locations]

        # 调整匹配位置以适应全屏幕坐标
        adjusted_locations = [(x + region_offset[0], y + region_offset[1]) for (x, y) in adjusted_locations]

        # # 输出匹配的原始位置
        # logger.info(f"match_template - Matched Locations: {matched_locations}")
        # # 输出调整后的位置
        # logger.info(f"match_template - Adjusted Locations: {adjusted_locations}")

        return adjusted_locations


    def mark_matches(self, img_path, locations, template_size, output_dir="screenshots", file_suffix=""):
        img = cv2.imread(img_path)
        for point in locations:
            top_left = point
            bottom_right = (top_left[0] + template_size[1], top_left[1] + template_size[0])
            cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
        marked_path = os.path.join(output_dir, f"marked_{file_suffix}.png")
        cv2.imwrite(marked_path, img)

    def find_target(self, category_key, color=True, threshold=0.8):
        """
        在屏幕的指定区域查找目标图像。
        
        :param category_key: 区域的键值，用于获取Config中的区域范围。
        :param color: 是否使用颜色匹配。
        :param threshold: 匹配阈值。
        :return: 匹配到的位置列表，坐标相对于全屏幕。
        """
        # 获取截图和区域的偏移量
        screenshot_path, (start_x, start_y) = self.capture_screen(category_key)

        template_path = self.config.region[category_key][0]
        if color:
            lower_color, upper_color = self.get_dominant_hsv_range(template_path)
            locations = self.match_template_with_color_mask(
                img_path=screenshot_path, 
                template_path=template_path, 
                lower_color=lower_color, 
                upper_color=upper_color, 
                region_offset=(start_x, start_y),  # 传递 region_offset 参数
                threshold=threshold
            )
        else:
            locations = self.match_template(
                img_path=screenshot_path, 
                template_path=template_path, 
                region_offset=(start_x, start_y),  # 传递 region_offset 参数
                threshold=threshold
            )

        if locations:
            return locations
        else:
            return False

    def get_dominant_hsv_range(self, image_path, bins=30):
        image = cv2.imread(image_path)

        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        h_values = hsv_image[:, :, 0].flatten()
        s_values = hsv_image[:, :, 1].flatten()
        v_values = hsv_image[:, :, 2].flatten()

        hsv_counter = Counter(zip(h_values, s_values, v_values))
        dominant_hsv = hsv_counter.most_common(1)[0][0]

        lower_bound = np.array([max(dominant_hsv[0] - 10, 0), max(dominant_hsv[1] - 50, 0), max(dominant_hsv[2] - 50, 0)])
        upper_bound = np.array([min(dominant_hsv[0] + 10, 180), min(dominant_hsv[1] + 50, 255), min(dominant_hsv[2] + 50, 255)])

        return lower_bound, upper_bound

image = ImageProcessor(config)