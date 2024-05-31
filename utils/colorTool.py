# 对后台窗口截图
import win32gui, win32ui, win32con
from PIL import Image

# from random import randint


def getColor_(eo, x, y):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(eo)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    ###保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC, "tempIMG.bmp")

    im = Image.open("tempIMG.bmp")  # 文件的路径
    # print(im.mode)
    # print(im.getpixel((x,y)))#像素点的rgb

    # 内存释放
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(eo, hWndDC)
    return im.getpixel((x, y))


def rgbint2rgbtuple(RGBint):

    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255

    return (blue, green, red)


def getColor(eo, x, y):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    color = rgbint2rgbtuple(win32gui.GetPixel(win32gui.GetWindowDC(eo), x, y))
    # win32gui.ReleaseDC(eo,hWndDC)
    # print("{},{} ====> ".format(x,y)+str(color))
    return color


def getColorTest(eo, printf):
    try:
        # print('width:{}, height:{}.'.format(width,height))
        # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        rgbint2rgbtuple(win32gui.GetPixel(win32gui.GetWindowDC(eo), 1, 1))
        # win32gui.ReleaseDC(eo,hWndDC)
        # print("{},{} ====> ".format(x,y)+str(color))
        # return color
    except:
        printf("Something wrong, please refresh.")


def saveImg(eo):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(eo)
    # 创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    # 创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
    # 将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    # 保存bitmap到内存设备描述表
    saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)
    ###保存bitmap到文件
    saveBitMap.SaveBitmapFile(saveDC, "tempIMG.bmp")

    return


def getSize():
    im = Image.open("tempIMG.bmp")
    return [im.width, im.height]


def get_color_dict(eo):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [width - i for i in range(50, width // 4, 13)]
    y_list = [height // 2 + i for i in range(50, height // 4, 13)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    color_dict = {}
    for x in x_list:
        for y in y_list:
            color = rgbint2rgbtuple(win32gui.GetPixel(screenshot, x, y))
            if color not in color_dict:
                color_dict[color] = 1
            else:
                color_dict[color] += 1
            # if color==(255, 251, 222):
            #     print(x,y)

    win32gui.ReleaseDC(eo, screenshot)
    # print("{},{} ====> ".format(x,y)+str(color))
    return color_dict


def color_exist_core(screenshot, x_list, y_list, color0, printf):

    for x in x_list:
        for y in y_list:
            try:
                color = rgbint2rgbtuple(win32gui.GetPixel(screenshot, x, y))
            except Exception as e:
                printf(str(e))
            if color in color0:
                return True
    return False


def color_exist(eo, color0, printf):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [width - i for i in range(50, width // 4, 13)]
    y_list = [height // 2 + i for i in range(50, height // 4, 13)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    res = color_exist_core(screenshot, x_list, y_list, color0, printf)
    win32gui.ReleaseDC(eo, screenshot)
    return res


def color_exist_(eo, color0, printf):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [width - i for i in range(50, width // 4, 13)]
    y_list = [height - i for i in range(50, height // 4, 13)]
    screenshot = win32gui.GetWindowDC(eo)
    res = color_exist_core(screenshot, x_list, y_list, color0, printf)
    win32gui.ReleaseDC(eo, screenshot)
    return res


def color_exist_fishing0(eo, color0, printf):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [i for i in range(100, width // 2, 5)]
    y_list = [height - i for i in range(50, height // 4, 5)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    res = color_exist_core(screenshot, x_list, y_list, color0, printf)
    win32gui.ReleaseDC(eo, screenshot)
    return res


def color_exist_fishing1(eo, color0, printf):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [i for i in range(100, width // 2, 5)]
    y_list = [height - i for i in range(50, height // 8, 5)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    res = color_exist_core(screenshot, x_list, y_list, color0, printf)
    win32gui.ReleaseDC(eo, screenshot)
    return res


def color_exist_fishing2(eo, color0, printf):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    x_list = [width // 2 + i for i in range(0, width // 4, 5)]
    y_list = [height - i for i in range(50, height // 4, 5)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    res = color_exist_core(screenshot, x_list, y_list, color0, printf)
    win32gui.ReleaseDC(eo, screenshot)
    return res


def black_out(eo):
    left, top, right, bot = win32gui.GetWindowRect(eo)
    width = right - left
    height = bot - top
    aa = height // 10
    # x,y=left+width//2
    # x_list=[left+i for i in range(0,width//2,3)]
    # y_list=[top+i for i in range(0,height//2,3)]
    # print('width:{}, height:{}.'.format(width,height))
    # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    # mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    screenshot = win32gui.GetWindowDC(eo)
    # color_set=set()
    res = (
        win32gui.GetPixel(screenshot, width // 2 - aa, height // 2 - aa) == 0
        and win32gui.GetPixel(screenshot, width // 2 + aa, height // 2 - aa) == 0
        and win32gui.GetPixel(screenshot, width // 2 - aa, height // 2 + aa) == 0
        and win32gui.GetPixel(screenshot, width // 2 + aa, height // 2 + aa) == 0
    )
    win32gui.ReleaseDC(eo, screenshot)
    return res
