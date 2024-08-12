import platform
import mss
import os

def get_screen_resolution():
    system = platform.system()

    if system == "Windows":
        import ctypes
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)
        screen_height = user32.GetSystemMetrics(1)

    elif system == "Darwin":
        import Quartz
        main_display_id = Quartz.CGMainDisplayID()
        screen_width = Quartz.CGDisplayPixelsWide(main_display_id)
        screen_height = Quartz.CGDisplayPixelsHigh(main_display_id)

    else:
        raise NotImplementedError("This platform is not supported")

    return screen_width, screen_height

def calculate_grid_coordinates(screen_width, screen_height):
    # 分别计算单个区域的宽度和高度
    region_width = screen_width // 4
    region_height = screen_height // 2

    # 定义8个区域的坐标
    coords = []
    for row in range(2):  # 两行：上半部分和下半部分
        for col in range(4):  # 每行四个区域
            left = col * region_width
            top = row * region_height
            coords.append({
                "name": f"region_{row}_{col}",
                "left": left,
                "top": top,
                "width": region_width,
                "height": region_height
            })

    return coords

def capture_and_save(coords):
    with mss.mss() as sct:
        save_dir = "screenshots"
        os.makedirs(save_dir, exist_ok=True)
        
        for region in coords:
            capture_region(sct, region, save_dir)

def capture_region(sct, region, save_dir):
    # Capture the region
    monitor = {
        "top": region['top'],
        "left": region['left'],
        "width": region['width'],
        "height": region['height']
    }
    
    img = sct.grab(monitor)
    
    # Save the captured region
    file_path = os.path.join(save_dir, f"{region['name']}.png")
    mss.tools.to_png(img.rgb, img.size, output=file_path)
    print(f"Saved {region['name']} screenshot at {file_path}")

def main():
    import time
    time.sleep(2)
    screen_width, screen_height = get_screen_resolution()
    coords = calculate_grid_coordinates(screen_width, screen_height)

    print("屏幕分辨率: ", screen_width, "x", screen_height)

    # Capture and save screenshots of these regions
    capture_and_save(coords)

if __name__ == "__main__":
    main()
