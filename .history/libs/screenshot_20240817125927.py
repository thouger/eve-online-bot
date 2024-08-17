import os
import cv2
import mss
import numpy as np
import pygetwindow as gw
from loguru import logger
import pyautogui

def get_window(title="EVE - "):
    """
    获取指定标题的窗口对象。
    
    :param title: 窗口的标题关键词
    :return: 返回找到的第一个窗口对象
    """
    windows = gw.getWindowsWithTitle(title)
    if not windows:
        raise Exception(f"未找到标题中包含'{title}'的窗口。")
    # logger.info(f"找到窗口：{windows[0].title}")
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

def match_template(img_path, template_path, method=cv2.TM_CCOEFF_NORMED, threshold=0.8, scale_range=(0.5, 1.5), scale_step=0.1):
    """
    在多个尺度下对指定图像进行模板匹配并返回匹配区域的中心坐标。
    
    :param img_path: 需要搜索的图像文件路径
    :param template_path: 作为模板的图像文件路径
    :param method: OpenCV提供的模板匹配方法
    :param threshold: 匹配的阈值，只有高于此阈值的结果会被返回
    :param scale_range: 要搜索的尺度范围（最小值, 最大值）
    :param scale_step: 每次缩放的步长
    :return: 匹配到的中心位置坐标，如果没有找到合适的匹配则返回None
    """
    # 读取图像和模板
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    original_template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    template_height, template_width = original_template.shape[:2]
    
    best_match = None
    best_val = -1

    # 在多个尺度下进行匹配
    for scale in np.arange(scale_range[0], scale_range[1], scale_step):
        # 调整模板尺寸
        scaled_template = cv2.resize(original_template, (int(template_width * scale), int(template_height * scale)))
        scaled_height, scaled_width = scaled_template.shape[:2]

        # 执行模板匹配
        result = cv2.matchTemplate(img, scaled_template, method)
        
        # 获取匹配结果大于阈值的坐标
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        
        if max_val > best_val and max_val >= threshold:
            best_val = max_val
            best_match = max_loc
            best_scale = scale

    # 如果找到了匹配项，计算中心位置
    if best_match is not None:
        center_x = best_match[0] + int((scaled_width) / 2)
        center_y = best_match[1] + int((scaled_height) / 2)
        # logger.info(f"找到匹配项：{center_x}, {center_y}")
        # pyautogui.moveTo(best_match[0], best_match[1])
        return (best_match[0], best_match[1])
        # return (center_x, center_y)
    
    return None

def match_features(img_path, template_path, threshold=0.75):
    """
    使用 ORB 特征匹配方法匹配图像并返回最佳匹配区域的中心坐标。
    
    :param img_path: 需要搜索的图像文件路径
    :param template_path: 作为模板的图像文件路径
    :param threshold: 匹配的阈值，越高越严格
    :return: 匹配到的中心位置坐标，如果没有找到合适的匹配则返回None
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # ORB 特征检测器
    orb = cv2.ORB_create()

    # 检测特征点并计算描述符
    kp1, des1 = orb.detectAndCompute(template, None)
    kp2, des2 = orb.detectAndCompute(img, None)

    # 使用 BFMatcher 进行特征点匹配
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    if len(matches) > 0:
        # 获取匹配点
        pt = kp2[matches[0].trainIdx].pt
        return int(pt[0]), int(pt[1])
    
    return None

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
    top_left = (locations[0] - template_size[1] // 2, locations[1] - template_size[0] // 2)
    bottom_right = (locations[0] + template_size[1] // 2, locations[1] + template_size[0] // 2)
    logger.info(f"标记位置：{top_left} - {bottom_right}")
    # 绘制矩形
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    marked_path = os.path.join(output_dir, f"marked_{file_suffix}.png")
    cv2.imwrite(marked_path, img)
    # logger.info(f"标记图像已保存至 {marked_path}")

def find_target(target,threshold=0.8,activation=False):
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
        if activation:
            window.activate()
        return locations
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

def match_features_with_sift(img_path, template_path, threshold=0.75):
    """
    使用 SIFT 特征匹配和仿射变换来更准确地匹配图像并返回最佳匹配区域的中心坐标。
    
    :param img_path: 需要搜索的图像文件路径
    :param template_path: 作为模板的图像文件路径
    :param threshold: 匹配的阈值，越高越严格
    :return: 匹配到的中心位置坐标，如果没有找到合适的匹配则返回None
    """
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # SIFT 特征检测器
    sift = cv2.SIFT_create()

    # 检测特征点并计算描述符
    kp1, des1 = sift.detectAndCompute(template, None)
    kp2, des2 = sift.detectAndCompute(img, None)

    # 使用 FLANN 匹配器进行特征点匹配
    index_params = dict(algorithm=1, trees=5)
    search_params = dict(checks=50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(des1, des2, k=2)

    # 只保留距离足够近的匹配项
    good_matches = []
    for m, n in matches:
        if m.distance < threshold * n.distance:
            good_matches.append(m)

    if len(good_matches) > 4:  # 至少需要4个点来计算仿射变换
        src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 计算仿射变换矩阵
        M, mask = cv2.estimateAffinePartial2D(src_pts, dst_pts)

        # 使用仿射变换矩阵来计算模板的中心点
        h, w = template.shape
        template_corners = np.float32([[0, 0], [0, h], [w, h], [w, 0]]).reshape(-1, 1, 2)
        transformed_corners = cv2.transform(template_corners, M)

        center_x = np.mean(transformed_corners[:, 0, 0])
        center_y = np.mean(transformed_corners[:, 0, 1])

        return int(center_x), int(center_y)
    
    return None
if __name__ == "__main__":
    # test_template_matching('Factional_warfare/5_degrees.png', threshold=0.8)
    match_features_with_sift('screenshots/full_screen.png', 'navigation/stargate.png', threshold=0.8)
