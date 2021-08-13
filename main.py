import cv2
import numpy
import win32api
import win32con
import win32gui
import win32ui
import win32print
import time
from recognizeimage import recognize_image
import os

dataset_path = '.\dataset'
file_path = 'D:\AutoRecognize.lua'
config_path = '.\config.txt'

Manual = 0
width = 2560
height = 1440
win_img_div_width = 4
win_img_div_height = 8
weapon_template_div_width = 0.4
weapon_template_div_height = 0.55
package_template_div_width = 0.13
package_template_div_height = 0.325

if __name__ == '__main__':
    exec(open(config_path, "r").read())
    # print(Manual)
    os.chdir(dataset_path)
    # 截取桌面
    hWnd = win32gui.GetDesktopWindow()
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    if Manual == 0:
        # 分辨率适应
        # width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        # height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        width = win32print.GetDeviceCaps(hWndDC, win32con.DESKTOPHORZRES)
        height = win32print.GetDeviceCaps(hWndDC, win32con.DESKTOPVERTRES)
        # print(width, height)
        # print(hWnd)
        # 分辨率适应 截图区域比例
        AspectRatio = width / height
        if AspectRatio == 5 / 4:
            win_img_div_width = 4
            win_img_div_height = 8
            weapon_template_div_width = 0.4
            weapon_template_div_height = 0.4
            package_template_div_width = 0.13
            package_template_div_height = 0.325
        elif AspectRatio == 16 / 9:
            win_img_div_width = 4
            win_img_div_height = 8
            weapon_template_div_width = 0.4
            weapon_template_div_height = 0.55
            package_template_div_width = 0.13
            package_template_div_height = 0.325
        elif AspectRatio == 16 / 10:
            win_img_div_width = 4
            win_img_div_height = 8
            weapon_template_div_width = 0.4
            weapon_template_div_height = 0.55
            package_template_div_width = 0.13
            package_template_div_height = 0.446
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, int(width / win_img_div_width), int(height / win_img_div_height))
    #   将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    while True:
        hWnd_apex = win32gui.FindWindow("Respawn001", "Apex Legends")
        if hWnd_apex != 0 and win32gui.IsIconic(hWnd_apex) == 0:
            while hWnd_apex != 0 and win32gui.IsIconic(hWnd_apex) == 0:
                # 保存bitmap到内存设备描述表
                saveDC.BitBlt((0, 0), (int(width / win_img_div_width), int(height / win_img_div_height)), mfcDC,
                              (width - int(width / win_img_div_width), height - int(height / win_img_div_height)), win32con.SRCCOPY)
                # 获取位图信息
                signedIntsArray = saveBitMap.GetBitmapBits(True)
                # PrintWindow成功
                im_opencv = numpy.frombuffer(signedIntsArray, dtype='uint8')
                im_opencv.shape = (int(height / win_img_div_height), int(width / win_img_div_width), 4)
                img = cv2.cvtColor(im_opencv, cv2.COLOR_BGRA2BGR)
                weapon_index, turbo_index = recognize_image(img, WeaponTemplateWidthDiv=weapon_template_div_width,
                                                            WeaponTemplateDivHeight=weapon_template_div_height,
                                                            PackageTemplateDivWidth=package_template_div_width,
                                                            PackageTemplateDivHeight=package_template_div_height)
                print("weapon_index=\"%s\" \n" % weapon_index + "turbo_index=%d" % turbo_index)
                file = open(file_path, "w")
                file.write("weapon_index=\"%s\" \n" % weapon_index + "turbo_index=%d" % turbo_index)
                file.close()
                if weapon_index != "None":
                    time.sleep(0.4)
                else:
                    time.sleep(0.2)
            cv2.destroyAllWindows()
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(hWnd, hWndDC)
        file = open(file_path, "w")
        file.write("weapon_index=\"None\" \n" + "turbo_index=0")
        file.close()
        print("全屏或无边框窗口化开启Apex Legends")
        time.sleep(1)
        
