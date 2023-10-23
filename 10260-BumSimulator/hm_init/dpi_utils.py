import time
import ctypes
import logging
import win32api
import pywintypes
from win32 import win32gui, win32print
from win32.lib import win32con
from win32.win32api import GetSystemMetrics

SPI_SETLOGICALDPIOVERRIDE = 0x009F
# dpi等级 0为100% 1为125% 依此类推
DPI_LEVEL = 1
logger = logging.getLogger()

fh = logging.FileHandler(
    f'./{time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())}.log', encoding='utf-8')
ch = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(funcName)s - %(filename)s [%(lineno)d] - %(message)s')
logger.setLevel(logging.INFO)
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

def get_real_resolution() -> tuple:
    """获取真实的分辨率"""
    hDC = win32gui.GetDC(0)
    # 横向分辨率
    w = win32print.GetDeviceCaps(hDC, win32con.DESKTOPHORZRES)
    # 纵向分辨率
    h = win32print.GetDeviceCaps(hDC, win32con.DESKTOPVERTRES)
    return w, h


def get_screen_size() -> tuple:
    """获取缩放后的分辨率"""
    w = GetSystemMetrics(0)
    h = GetSystemMetrics(1)
    return w, h


def get_dpi_scaling() -> int:
    """通过计算获得当前dpi值"""
    real_resolution = get_real_resolution()
    screen_size = get_screen_size()
    screen_scale_rate = round(real_resolution[0] / screen_size[0], 2)
    screen_scale_rate = screen_scale_rate * 100
    return int(screen_scale_rate)


def set_screen_size(screenSize: tuple) -> None:
    """设置系统分辨率为1080P"""
    devmode = pywintypes.DEVMODEType()
    devmode.PelsWidth = screenSize[0]
    devmode.PelsHeight = screenSize[1]
    devmode.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(devmode, 0)


def set_dpi_scaling(dpi_level: int) -> None:
    """设置系统dpi为指定等级"""
    h = ctypes.windll.LoadLibrary("C:\\Windows\\System32\\user32.dll")
    h.SystemParametersInfoA(SPI_SETLOGICALDPIOVERRIDE, dpi_level, 0, 1)


def main(main_logger: logging.Logger):
    set_screen_size((1920, 1080))
    main_logger.info("set screen size to 1080P success")
    set_dpi_scaling(0)
    main_logger.info(f"set dpi success, change dpi to 100%")


if __name__ == "__main__":
    main(logger)
