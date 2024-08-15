import pygetwindow as gw

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
