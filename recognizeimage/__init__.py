import cv2 as cv
import numpy as np
import os

# from matplotlib import pyplot as plt
# 列表中所有的6种比较方法
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
           'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']


method1 = cv.TM_CCOEFF_NORMED
method2 = cv.TM_CCOEFF_NORMED

IMAGE_SIZE_WIDTH = 320
IMAGE_SIZE_HEIGHT = 128

weapon_template_div_width = 0.4
weapon_template_div_height = 0.4
package_template_div_width = 0.13
package_template_div_height = 0.325

err_image = np.zeros((IMAGE_SIZE_HEIGHT, IMAGE_SIZE_WIDTH), dtype=np.uint8)
err_image = cv.cvtColor(err_image, cv.COLOR_GRAY2BGR)


def resize_image(image, height=IMAGE_SIZE_HEIGHT, width=IMAGE_SIZE_WIDTH):
    # 防止空图像错误输入
    if image.size == 0:
        return err_image
    # 调整图像大小并返回
    return cv.resize(image, (int(width), int(height)), interpolation=cv.INTER_LINEAR)


def mean_2d_coordinates(arg):
    res_x = []
    res_y = []
    for coordinate in arg:
        res_x.append(coordinate[0])
        res_y.append(coordinate[1])
    res_x = int(np.array(res_x).mean())
    res_y = int(np.array(res_y).mean())
    res_coordinate = [res_x, res_y]
    return res_coordinate


def recognize_image(img, WeaponTemplateWidthDiv = weapon_template_div_width,
                    WeaponTemplateDivHeight = weapon_template_div_height,
                    PackageTemplateDivWidth = package_template_div_width,
                    PackageTemplateDivHeight = package_template_div_height):
    # 防止空图像错误输入
    if img.size == 0:
        return None, 0
    img = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    height, width = img.shape
    template_image_size_width = int(width * WeaponTemplateWidthDiv)
    template_image_size_height = int(height * WeaponTemplateDivHeight)
    weapons_res = []
    weapons_arg = []
    weapon_res = None
    weapon_arg = []
    turbo_res = 0
    for weapon in os.listdir("./weapons"):
        # 应用模板匹配
        data1_res = []
        data1_arg = []
        for i in os.listdir("./weapons/%s" % weapon):
            template = cv.imread('./weapons/%s/%s' % (weapon, i), 0)
            template = resize_image(template, template_image_size_height, template_image_size_width)
            res = cv.matchTemplate(img, template, method1)
            if method1 in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                data1_res.append(res.min())
                data1_arg.append(cv.minMaxLoc(res)[2])
            else:
                data1_res.append(res.max())
                data1_arg.append(cv.minMaxLoc(res)[3])
            # print(data1_res)
            # print(data1_arg)
        data1_res = np.array(data1_res)
        # print(data1_res)
        # print(data1_res.mean())
        weapons_res.append(data1_res.mean())
        weapons_arg.append(mean_2d_coordinates(data1_arg))
    if method1 in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        weapon_res = np.argmin(weapons_res)
    else:
        weapon_res = np.argmax(weapons_res)
    if method1 in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        if weapons_res[weapon_res] >= 0.25:
            # print(weapons_res[weapon_res])
            weapon_res = "None"
        else:
            weapon_arg = weapons_arg[weapon_res]
            weapon_res = os.listdir("./weapons")[weapon_res]
    else:
        if weapons_res[weapon_res] <= 0.75:
            # print(weapons_res[weapon_res])
            weapon_res = "None"
        else:
            weapon_arg = weapons_arg[weapon_res]
            weapon_res = os.listdir("./weapons")[weapon_res]
    # print(weapon_arg)
    if weapon_res == "HWK" or weapon_res == "ZZ":
        img = img[weapon_arg[1]:(weapon_arg[1]+template_image_size_height), weapon_arg[0]:(weapon_arg[0]+template_image_size_width)]
        # img = cv.cvtColor(img, cv.COLOR_GRAY2RGB)
        # cv.imwrite('img.png', img)
        data2_res = []
        for i in os.listdir("./packages/HWK_WL"):
            template = cv.imread('./packages/HWK_WL/%s' % i, 0)
            template = resize_image(template, int(template_image_size_height * PackageTemplateDivHeight),
                                    int(template_image_size_width * PackageTemplateDivWidth))
            # template = cv.fastNlMeansDenoising(template, None, 10, 7, 21)
            res = cv.matchTemplate(img, template, method2)
            # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
            # top_left = max_loc
            # # print(max_val)
            # h, w, ret = template.shape
            # bottom_right = (top_left[0] + w, top_left[1] + h)
            # cv.rectangle(img, top_left, bottom_right, 255, 2)
            # cv.imwrite("1.png", img)
            # cv.waitKey(0)
            if method2 in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                data2_res.append(res.min())
            else:
                data2_res.append(res.max())
            # print(res.max())
        data2_res = np.array(data2_res)
        # print(data2_res)
        data2_res = data2_res[data2_res > 0.5]
        data2_res = data2_res.mean()
        print(data2_res)
        if method2 in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            if data2_res < 0.3:
                turbo_res = 0
            else:
                turbo_res = 1
        else:
            if 0.7 > data2_res:
                turbo_res = 1
            else:
                turbo_res = 0
    # print(weapon_res)
    # print(turbo_res)
    return weapon_res, turbo_res

