import win32gui
import win32ui
import win32con

from core.config import ColorConfig, Config

# from PIL import Image

dialogue_color = [
    (255, 251, 255),
    (77, 76, 77),
]
text_color = [(74, 73, 74), (99, 97, 99)]
bg_deep_green = [(107, 162, 165)]
bg_deep_blue = [(41, 81, 107)]
bg_yellow = [(255, 251, 222)]
shiny_star_yellow = [(255, 210, 82)]


def read_color(color_config: ColorConfig):
    global dialogue_color, text_color, bg_deep_green, bg_deep_blue, bg_yellow, shiny_star_yellow
    try:
        (
            _,
            dialogue_color_main,
            dialogue_color_rainy,
            text_color,
            bg_deep_green,
            bg_deep_blue,
            bg_yellow,
            shiny_star_yellow,
        ) = [[color] for color in color_config.__dict__.values()]
        dialogue_color = dialogue_color_main + dialogue_color_rainy

    except Exception as e:
        print(f"Read color from ini failed:\n{e}")


def rgbint2rgbtuple(RGBint):
    red = RGBint & 255
    green = (RGBint >> 8) & 255
    blue = (RGBint >> 16) & 255
    return (red, green, blue)
    # return (blue, green, red)


def color_distance_square(color01, color02):
    return sum([(color01[i] - color02[i]) ** 2 for i in range(3)])


mode2color = {
    "right_top_rse_in_game": dialogue_color[:1],
    "ally_battle_status": bg_yellow,
    "normal_dialogue": dialogue_color + text_color,
    "battle_dialogue_RSE": bg_deep_green,
    "battle_dialogue_FrLg": bg_deep_blue,
    "get_fish": text_color,
    "no_fish": text_color,
    "encounter_fish": text_color,
    "dialogue": dialogue_color,
    "right_bottom_bggreen": bg_deep_green,
    "shiny_star": shiny_star_yellow,
    "dialogue_for_FrLg_Starters_and_RS_fishing": dialogue_color,
    # "dialogue_for_RS_fishing": dialogue_color,
}


class ColorMonitor(object):
    def __init__(self, hander, config: Config, print_f=print) -> None:
        self.hander = hander
        self.config = config
        self.print = print_f
        self.sqr_dis = self.config.color.color_distance**2
        self.refresh()

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

    def refresh(self) -> None:
        self.window = win32gui.GetWindowDC(self.hander)
        left, top, right, bot = win32gui.GetWindowRect(self.hander)
        self.window_width = right - left
        self.window_height = bot - top

        self.density = 30
        self.boundary_init()

    def check(self, mode=""):
        # self.refresh()
        if mode == "black_out":
            return self.check_black_out()
        if mode == "normal_dialogue":
            return self.color_exist(mode2color[mode][:-1], mode) and self.color_exist(
                mode2color[mode][-1:], mode
            )
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
        elif mode == "right_top_rse_in_game":
            x_list = [
                i
                for i in range(
                    0, self.game_width // 8, self.get_interval(self.game_width // 8)
                )
            ]
            y_list = [
                i
                for i in range(
                    0, self.game_height // 8, self.get_interval(self.game_height // 4)
                )
            ]
        elif (
            mode == "dialogue_for_FrLg_Starters_and_RS_fishing"
            or mode == "right_bottom_bggreen"
        ):
            x_list = [
                self.game_width // 8 * 7 + i
                for i in range(
                    0, self.game_width // 8, self.get_interval(self.game_width // 8)
                )
            ]
            y_list = [
                self.game_height // 4 * 3 + i
                for i in range(
                    0, self.game_height // 4, self.get_interval(self.game_height // 4)
                )
            ]
        elif mode == "normal_dialogue" or mode == "dialogue":
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
        elif mode in ["encounter_fish"]:
            # C4+1/45
            x_list = [
                self.game_width // 2 + i
                for i in range(
                    0,
                    self.game_width // 4,
                    self.get_interval(self.game_width // 4),
                    # 0,
                    # self.game_width // 4,
                    # 3,
                )
            ]
            y_list = [
                self.game_height // 4 * 3 + i
                for i in range(
                    0, self.game_height // 45, max(self.game_height // 45 // 5, 1)
                )
            ]
        elif mode in ["shiny_star"]:
            x_list = [
                i for i in range(self.game_width // 3, self.game_width // 3 * 2, 3)
            ]
            y_list = [i for i in range(0, self.game_height // 2, 3)]
        return self.color_exist_core(x_list, y_list, color_list)

    def color_exist_core(self, x_list, y_list, target_color_list):
        # color_set = set()
        for x in self.get_absolute_x(x_list):
            for y in self.get_absolute_y(y_list):
                color = self.get_color(x, y)
                # color_set.add(color)
                for target_color in target_color_list:
                    if self.in_color_range(color, target_color):
                        return True
        # print(color_set)
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

    def check_black_out(self, interval_ratio=10):
        interval = self.window_height // interval_ratio
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

    def check_white_out(self, interval_ratio=10):
        interval = self.window_height // interval_ratio
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
            map(lambda x: self.get_color(x[0], x[1]) == dialogue_color[0], check_list)
        )
        return res

    def get_color(self, x, y):
        """
        return RGB value
        """
        return rgbint2rgbtuple(win32gui.GetPixel(self.window, x, y))

    def get_color_center(self):
        return self.get_color(self.window_width // 2, self.window_height // 2)

    def in_color_range(self, color0, color1):
        return color_distance_square(color0, color1) <= self.sqr_dis

    def get_absolute_x(self, x_list):
        return [self.l_start + x for x in x_list]

    def get_absolute_y(self, y_list):
        return [self.u_start + y for y in y_list]

    def get_interval(self, x):
        return max(x // self.density, 1)

    def check_black_boundary(self):
        interval = self.window_width // 32
        # print(self.window_width, self.window_height)
        return (
            win32gui.GetPixel(self.window, interval, self.window_height // 2) == 0
            and win32gui.GetPixel(
                self.window, self.window_width - interval, self.window_height // 2
            )
            == 0
        )

    def boundary_init(self):
        if self.check_black_boundary():
            self.l_start = self.r_end = 107
            self.u_start = 106
            self.d_end = 7
            # print("black")
        else:
            self.l_start = self.r_end = 0
            self.u_start = 0
            self.d_end = 0
            # print("no black")
        self.game_width = self.window_width - self.l_start - self.r_end
        self.game_height = self.window_height - self.u_start - self.d_end
        pass

    def save_image(self, filename="AutoPoke.shinyshoot.bmp"):
        try:
            print(
                f"win_h:{self.window_height}\nwin_w:{self.window_width}\ngame_h:{self.game_height}\ngame_w:{self.game_width}"
            )
            # 创建设备描述表
            mfcDC = win32ui.CreateDCFromHandle(self.window)
            # 创建内存设备描述表
            saveDC = mfcDC.CreateCompatibleDC()
            # 创建位图对象准备保存图片
            saveBitMap = win32ui.CreateBitmap()
            # 为bitmap开辟存储空间
            saveBitMap.CreateCompatibleBitmap(
                mfcDC, self.window_width, self.window_height
            )
            # 将截图保存到saveBitMap中
            saveDC.SelectObject(saveBitMap)
            # 保存bitmap到内存设备描述表
            saveDC.BitBlt(
                (0, 0),
                (self.window_width, self.window_height),
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
