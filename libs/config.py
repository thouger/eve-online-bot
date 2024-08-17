import pygetwindow as gw
from loguru import logger

def get_window_by_title(title_keyword = "EVE - "):
    """
    获取指定标题的窗口对象。
    
    :param title: 窗口的标题关键词
    :return: 返回找到的第一个窗口对象
    """
    try:
        windows = gw.getWindowsWithTitle(title)
        if not windows:
            raise Exception(f"未找到标题中包含'{title}'的窗口。")
        logger.info(f"找到窗口：{windows[0].title}")
        return windows[0]
    except Exception as e:
        # logger.error(f"Error in get_window: {e}")
        return None


client = "mac"

class Config:
    _instance = None
    region = {
        'stargate':{
            'navigation/stargate.png':['0_3','1_3']
        }
    }

    def __init__(self) -> None:
        self.window = get_window_by_title("EVE - ")

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance.window = None  # 初始化共享变量
        return cls._instance

    def set_window(self, window):
        self.window = window

    def get_window(self):
        return self.window
    
    def get_client(self):
        return client
    
config = Config()