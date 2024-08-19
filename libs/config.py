import pygetwindow as gw
from loguru import logger
import pyautogui
import mss


# client = "mac"
client = '4k'

class Config:
    _instance = None

    # 第 1 块（左下角）：(0.0, 0.0, 1/3, 1.5/3)
    # 第 2 块（中下）：(1/3, 0.0, 2/3, 1.5/3)
    # 第 3 块（右下角）：(2/3, 0.0, 6/6, 1.5/3)
    # 第 4 块（左上角）：(0.0, 1.5/3, 1/3, 3/3)
    # 第 5 块（中上）：(1/3, 1.5/3, 2/3, 3/3)
    # 第 6 块（右上角）：(2/3, 1.5/3, 6/6, 3/3)
    region = {
        'stargate': (f'navigation/{client}/stargate.png', (2/3, 0.0, 6/6, 3/3)),  # 第6块（右上角）+ 第3块（右下角）合并
        'station': (f'navigation/{client}/station.png', (2/3, 0.0, 6/6, 3/3)),  # 第6块（右上角）+ 第3块（右下角）合并
        'wrapping1': (f'navigation/{client}/warpping1.png', (1/3, 1.5/3, 2/3, 3/3)),  # 第二块（中下）
        'wrapping2': (f'navigation/{client}/warpping2.png', (1/3, 1.5/3, 2/3, 3/3)),  # 第二块（中下）
        'jumping': (f'navigation/{client}/jumping.png', (1/3, 1.5/3, 2/3, 3/3)),  # 第二块（中下）
        '1_jump': (f'navigation/{client}/1_jump.png', (0.0, 0, 1/3, 1.5/3)),  # 第四块（左上角）
        '0_jump': (f'navigation/{client}/0_jump.png', (0.0, 0, 1/3, 1.5/3)),  # 第四块（左上角）
        'not_found': (f'navigation/{client}/not_found.png', (2/3, 0.0, 3/3, 1.5/3)),  # 第六块（右上角）
        '0ms': (f'navigation/{client}/0ms.png', (1/3, 1.5/3, 2/3, 3/3)),  # 第二块（中下）
    }

    def __init__(self) -> None:
        self.client = client
        self.window = get_window_by_title("EVE - ")
        self.screen_size = pyautogui.size()
        self.init_window()

    def init_window(self):
        """
        初始化窗口对象，获取窗口的尺寸和位置。
        """
        self.window = get_window_by_title("EVE - ")
        if self.window:
            self.window_size = {
                "top": self.window.top,
                "left": self.window.left,
                "width": self.window.width,
                "height": self.window.height
            }
        else:
            # 如果获取窗口失败（比如mac），采用第一个显示器的尺寸
            with mss.mss() as sct:
                self.screen = sct.monitors[1]
                self.window_size = sct.monitors[1]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance.window = None  # 初始化共享变量
        return cls._instance

    
def get_window_by_title(title = "EVE - "):
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

config = Config()