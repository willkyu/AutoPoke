import win32gui
import win32ui
import win32con

# from PIL import Image

dialogue_color = [
    (255, 251, 255),
    (77, 76, 77),
]
text_color = [(74, 73, 74)]
bg_deep_green = [(107, 162, 165)]
bg_deep_blue = [(41, 81, 107)]
bg_yellow = [(255, 251, 222)]


def read_color(colorList: list):
    global dialogue_color, text_color, bg_deep_green, bg_deep_blue, bg_yellow
    try:
        dialogue_color, text_color, bg_deep_green, bg_deep_blue, bg_yellow = colorList
    except:
        print("Read color from ini failed.")


def rgbint2rgbtuple(RGBint):
    blue = RGBint & 255
    green = (RGBint >> 8) & 255
    red = (RGBint >> 16) & 255
    return (red, green, blue)
    # return (blue, green, red)


def color_distance_square(color01, color02):
    return sum([(color01[i] - color02[i]) ** 2 for i in range(3)])


mode2color = {
    "ally_battle_status": bg_yellow,
    "normal_dialogue": dialogue_color + text_color,
    "battle_dialogue_RSE": bg_deep_green,
    "battle_dialogue_FrLg": bg_deep_blue,
    "get_fish": text_color,
    "no_fish": text_color,
}


class ColorMonitor(object):
    def __init__(self, hander, print_f=print, color_distance=10) -> None:
        self.hander = hander
        self.refresh(hander, print_f, color_distance)

    def __enter__(self):
        return self

    def __exit__(self, type, value, trace):
        win32gui.ReleaseDC(self.hander, self.window)

    # def __init__(self, hander) -> None:
    #     # 返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    #     self.window = win32gui.GetWindowDC(hander)
    #     left, top, right, bot = win32gui.GetWindowRect(hander)
    #     self.width = right - left
    #     self.height = bot - top

    def refresh(self, hander, print_f, color_distance) -> None:
        self.window = win32gui.GetWindowDC(hander)
        left, top, right, bot = win32gui.GetWindowRect(hander)
        self.window_width = right - left
        self.window_height = bot - top
        self.print = print_f
        self.sqr_dis = color_distance**2

        self.density = 30

        self.l_start = self.r_end = 107
        self.u_start = 106
        self.d_end = 7
        self.boundary_init()

    def check(self, mode=""):
        if mode == "black_out":
            return self.check_black_out()
        return self.color_exist(mode2color[mode], mode)

    def color_exist(self, color_list, mode=""):
        # no 'match' in python 3.9
        if mode == "ally_battle_status":
            # D3
            x_list = [
                self.game_width // 4 * 3 + i
                for i in range(
                    0, self.game_width // 4, self.get_interval(self.game_width // 4)
                )
            ]
            y_list = [
                self.game_height // 2 + i
                for i in range(
                    0, self.game_height // 4, self.get_interval(self.game_height // 4)
                )
            ]
        elif mode == "normal_dialogue":
            # AB4
            x_list = [
                i
                for i in range(
                    0, self.game_width // 2, self.get_interval(self.game_width // 4)
                )
            ]
            y_list = [
                self.game_height // 4 * 3 + i
                for i in range(
                    0, self.game_height // 4, self.get_interval(self.game_height // 4)
                )
            ]
        elif mode in ["battle_dialogue_RSE", "battle_dialogue_FrLg"]:
            # D4
            x_list = [
                self.game_width // 4 * 3 + i
                for i in range(
                    0, self.game_width // 4, self.get_interval(self.game_width // 4)
                )
            ]
            y_list = [
                self.game_height // 4 * 3 + i
                for i in range(
                    0, self.game_height // 4, self.get_interval(self.game_height // 4)
                )
            ]
        elif mode in ["get_fish"]:
            # AB4.5
            x_list = [
                i
                for i in range(
                    0, self.game_width // 2, self.get_interval(self.game_width // 4)
                )
            ]
            y_list = [
                self.game_height // 8 * 7 + i
                for i in range(
                    0, self.game_height // 8, self.get_interval(self.game_height // 8)
                )
            ]
        elif mode in ["no_fish"]:
            # AB4+1/45
            x_list = [
                i
                for i in range(
                    0, self.game_width // 2, self.get_interval(self.game_width // 4)
                )
            ]
            y_list = [
                self.game_height // 4 * 3 + i
                for i in range(
                    0, self.game_height // 45, max(self.game_height // 45 // 5, 1)
                )
            ]
        return self.color_exist_core(x_list, y_list, color_list)

    def color_exist_core(self, x_list, y_list, target_color_list):
        for x in self.get_absolute_x(x_list):
            for y in self.get_absolute_y(y_list):
                color = self.get_color(x, y)
                for target_color in target_color_list:
                    if self.in_color_range(color, target_color):
                        return True
        return False

    def color_exist_core_with_count(self, x_list, y_list, target_color_list):
        num = 0
        for x in self.get_absolute_x(x_list):
            for y in self.get_absolute_y(y_list):
                color = self.get_color(x, y)
                for target_color in target_color_list:
                    if self.in_color_range(color, target_color):
                        num += 1
        return False

    def check_black_out(self):
        interval = self.window_height // 10
        check_list = [
            [
                self.window_width // 2 + i * interval,
                self.window_height // 2 + j * interval,
            ]
            for i in [-1, 1]
            for j in [-1, 1]
        ]
        # print(check_list)
        res = all(
            map(lambda x: win32gui.GetPixel(self.window, x[0], x[1]) == 0, check_list)
        )
        return res

    def get_color(self, x, y):
        """
        return RGB value
        """
        return rgbint2rgbtuple(win32gui.GetPixel(self.window, x, y))

    def in_color_range(self, color0, color1):
        return color_distance_square(color0, color1) <= self.sqr_dis

    def get_absolute_x(self, x_list):
        return [self.l_start + x for x in x_list]

    def get_absolute_y(self, y_list):
        return [self.u_start + y for y in y_list]

    def get_interval(self, x):
        return max(x // self.density, 1)

    def boundary_init(self):
        self.game_width = self.window_width - self.l_start - self.r_end
        self.game_height = self.window_height - self.u_start - self.d_end
        pass

    def save_image(self, filename="shortcut.bmp"):
        try:
            # 创建设备描述表
            mfcDC = win32ui.CreateDCFromHandle(self.window)
            # 创建内存设备描述表
            saveDC = mfcDC.CreateCompatibleDC()
            # 创建位图对象准备保存图片
            saveBitMap = win32ui.CreateBitmap()
            # 为bitmap开辟存储空间
            saveBitMap.CreateCompatibleBitmap(mfcDC, self.game_width, self.game_height)
            # 将截图保存到saveBitMap中
            saveDC.SelectObject(saveBitMap)
            # 保存bitmap到内存设备描述表
            saveDC.BitBlt(
                (0, 0),
                (self.game_width, self.game_height),
                mfcDC,
                (0, 0),
                win32con.SRCCOPY,
            )
            # 保存bitmap到文件
            saveBitMap.SaveBitmapFile(saveDC, filename)
            # 内存释放
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
        except Exception as e:
            self.print("Save Image Error: {}".format(e))


# print(color_distance_square((255, 251, 255), (255, 251, 255)))

# def get_color(eo, x, y):
