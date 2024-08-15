from libs.screenshot import *
import pyautogui
import os
from loguru import logger
from config import config
from screenshots import *
from libs.window import *

def init():
    window = get_window_with_title("EVE - ")
    config.set_window(window)
    logger.info(f"找到窗口: {window.title}, 大小: {window.width}x{window.height}, 位置: ({window.left}, {window.top})")

init()