# -*- coding: utf-8 -*-
"""
手机屏幕截图的代码
"""
import subprocess
import os
import sys
from PIL import Image
from io import StringIO
from common.auto_adb import auto_adb
adb = auto_adb()

# SCREENSHOT_WAY 是截图方法，经过 check_screenshot 后，会自动递减，不需手动修改
SCREENSHOT_WAY = 3

name = 'screen.png'

def pull_screenshot():
    """
    获取屏幕截图，目前有 0 1 2 3 四种方法，未来添加新的平台监测方法时，
    可根据效率及适用性由高到低排序
    """
    global SCREENSHOT_WAY
    if 1 <= SCREENSHOT_WAY <= 3:
        process = subprocess.Popen(
            adb.adb_path + ' shell screencap -p',
            shell=True, stdout=subprocess.PIPE)
        binary_screenshot = process.stdout.read()
        if SCREENSHOT_WAY == 2:
            binary_screenshot = binary_screenshot.replace(b'\r\n', b'\n')
        elif SCREENSHOT_WAY == 1:
            binary_screenshot = binary_screenshot.replace(b'\r\r\n', b'\n')
        return Image.open(StringIO(binary_screenshot))
    elif SCREENSHOT_WAY == 0:
        adb.run('shell screencap -p /sdcard/{}'.format(name))
        adb.run('pull /sdcard/{} ./tmp/'.format(name))
        return Image.open('./tmp/{}'.format(name))


def check_screenshot():
    """
    检查获取截图的方式
    """
    global SCREENSHOT_WAY
    if os.path.isfile('./tmp/{}'.format(name)):
        try:
            os.remove('./tmp/{}'.format(name))
        except Exception:
            pass
    if SCREENSHOT_WAY < 0:
        print('暂不支持当前设备')
        sys.exit()
    try:
        im = pull_screenshot()
        im.load()
        im.close()
        print('采用方式 {} 获取截图'.format(SCREENSHOT_WAY))
    except Exception:
        SCREENSHOT_WAY -= 1
        check_screenshot()
