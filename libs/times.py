import time

def timing_decorator(func):
    """
    装饰器，用于计算函数执行时间。
    
    :param func: 被装饰的函数。
    :return: 包装后的函数。
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)  # 执行被装饰的函数
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} 函数执行耗时: {elapsed_time:.4f}秒")
        return result

    return wrapper