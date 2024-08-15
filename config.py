# config.py

class Config:
    _instance = None
    region = {
        'stargate':{
            'navigation/stargate.png':['0_3','1_3']
        }
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
            cls._instance.window = None  # 初始化共享变量
        return cls._instance

    def set_window(self, window):
        self.window = window

    def get_window(self):
        return self.window
    
config = Config()