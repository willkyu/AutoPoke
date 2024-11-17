# from multiprocessing.connection import wait
from time import sleep
from utils.press_tool import PressController
from utils.color_tool import ColorMonitor, read_color
from utils.mail_tool import send_mail
from random import choice

# from atexit import register, unregister
from utils.config_tool import Config


class AutoPokeCore(object):
    def __init__(self, eo, cfg: Config, printf, update_count) -> None:
        self.color_monitor: ColorMonitor
        self.hander = eo
        self.cfg = cfg
        self.printf = printf
        self.update_count = update_count
        self.press_controller = PressController(self.hander)
        read_color(self.cfg.color_list)

        self.ifFRLG = self.cfg.version == "FrLg"

        pass

    def test(self):
        import win32gui, win32con

        self.printf(
            f"sendmessage return: {win32gui.SendMessage(self.hander, win32con.WM_KEYDOWN, 38, 0)}"
        )
        sleep(0.1)
        self.printf(
            f"sendmessage return: {win32gui.SendMessage(self.hander, win32con.WM_KEYUP, 38, 0)}"
        )
        sleep(0.5)
        self.printf(
            f"postmessage return: {win32gui.PostMessage(self.hander, win32con.WM_KEYDOWN, 38, 0)}"
        )
        sleep(0.1)
        self.printf(
            f"postmessage return: {win32gui.PostMessage(self.hander, win32con.WM_KEYUP, 38, 0)}"
        )
        self.color_monitor.save_image()
        self.printf("screenshot saved.")

    def exe_function(self, function: str):
        # try:
        # with ColorMonitor(self.hander, self.printf) as self.color_monitor:
        self.color_monitor = ColorMonitor(self.hander, self.printf)
        self.language = self.cfg.language
        # print(function)
        if function == "TEST":
            self.test()
        elif function == "WILDPOKE":
            self.WILDPOKE()
        elif function == "STATIONARY":
            self.STATIONARY()
        elif function == "FISHING" and not self.ifFRLG:
            assert self.cfg.version in ["RS", "E"]
            self.FISHING_RSE()
        # except Exception as e:
        #     self.printf(str(e))
        self.release_all_keys()

    def release_all_keys(self):
        self.press_controller.release_all_keys(self.cfg.keymap.values())

    def key(self, str):
        return self.cfg.keymap[str]

    def WILDPOKE(self):
        self.jump = eval(self.cfg.mode_config["jump"])
        self.run = eval(self.cfg.mode_config["run"])
        self.ifLR = eval(self.cfg.mode_config["iflr"])
        self.sweet_scent = eval(self.cfg.mode_config["sweet_scent"])

        # 默认左右走，ifLR=False时，上下走
        self.move_key_list = (
            [self.key("LEFT"), self.key("RIGHT")]
            if self.ifLR
            else [self.key("UP"), self.key("DOWN")]
        )
        # 开始遇敌
        self.printf("Encountering...")
        while 1:
            if self.sweet_scent:
                self.sweet_scent_encountering()
            else:
                self.wild_encountering()

            if self.check_shiny():
                break

            self.printf("Not shiny, run...")
            self.check_extra_anime()
            self.RUN()
            self.printf("Encountering...")

    def STATIONARY(self, hitkeys=[]):

        delay_list = [a / 100 for a in range(0, 60, 2)]

        while 1:
            sleep(choice(delay_list))
            self.stationary_encountering()

            if self.check_shiny():
                break

            self.printf("Not shiny, SLing...")
            self.SL()
            self.after_SL()
        pass

    def FISHING_RSE(self):
        while 1:
            self.fishing_rse_encountering()

            if self.check_shiny():
                break

            self.printf("Not shiny, run...")
            self.check_extra_anime()
            self.RUN()
            self.printf("Encountering...")

        pass

    def RUN(self):
        self.press_controller.hit_key(self.key("RIGHT"))
        self.press_controller.hit_key(self.key("DOWN"))
        while not self.color_monitor.check_black_out():
            self.press_controller.hit_key(self.key("A"))
            # print("A")
            # sleep(0.1)
            self.press_controller.hit_key(self.key("B"))
        while self.color_monitor.check_black_out():
            print("black")
            sleep(0.1)

    def check_shiny(self):
        # 遇敌黑屏到第一次按A的时间
        sleep(3.9)
        if self.language == "Jpn":
            sleep(0.5)
        self.press_controller.hit_key(self.key("A"))
        # self.press_controller.hit_key(self.key("A"))
        # self.printf("Hit A.")

        # safari zone 判定
        sleep(0.2)
        if self.color_monitor.check("ally_battle_status"):
            return False

        self.printf("Not safari...")
        # 非safari zone额外等待时间
        sleep(2.7)

        if not self.color_monitor.check("ally_battle_status"):
            self.printf("Got Shiny Pokemon! {} times.".format(self.cfg.i))
            self.send_mail()
            self.cfg.i = 0
            self.cfg.write_count_config()
            return True
        return False

    def check_extra_anime(self):
        # 额外动画检测
        if self.color_monitor.check("battle_dialogue_RSE") or self.color_monitor.check(
            "battle_dialogue_FrLg"
        ):
            self.printf("Special anime detected.")
            while 1:
                if not self.color_monitor.check(
                    "battle_dialogue_RSE"
                ) and not self.color_monitor.check("battle_dialogue_FrLg"):
                    sleep(0.02)
                    break
                sleep(0.1)

    def wild_encountering(self):
        if self.jump or self.run:
            self.press_controller.key_down(self.key("B"))
        while 1:
            if not self.jump:
                self.press_controller.random_hit_key(self.move_key_list)
            else:
                sleep(0.1)

            if self.color_monitor.check_black_out():
                self.printf("A wild pokemon encountered!")
                if self.jump or self.run:
                    self.press_controller.key_up(self.key("B"))
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                self.cfg.i += 1
                self.update_count(self.cfg.i)
                break
            elif self.cfg.version == "E":
                if self.color_monitor.check("dialogue"):
                    # self.printf("PokeNav detected.")
                    if self.jump or self.run:
                        self.press_controller.key_up(self.key("B"))
                        sleep(0.2)
                    while self.color_monitor.check("dialogue"):
                        self.press_controller.hit_key(self.key("B"))
                        sleep(0.2)
                    if self.jump or self.run:
                        self.press_controller.key_down(self.key("B"))
                        sleep(0.2)

    def sweet_scent_encountering(self):
        self.press_controller.hit_key(self.key("START"))
        self.press_controller.hit_key(self.key("A"))
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                self.cfg.i += 1
                self.update_count(self.cfg.i)
                break
        self.press_controller.hit_key(self.key("UP"), time=0.1)
        sleep(0.1)
        self.press_controller.hit_key(self.key("UP"), time=0.1)
        self.press_controller.hit_key(self.key("A"), time=0.1)
        if self.ifFRLG:
            self.press_controller.hit_key(self.key("DOWN"), time=0.1)
        else:
            # self.press_controller.key_up(self.key(("A")))
            sleep(0.1)
        self.press_controller.hit_key(self.key("A"), time=0.1)
        self.printf("Using sweet scent.")
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                self.cfg.i += 1
                self.update_count(self.cfg.i)
                break
        sleep(1.5)
        while 1:
            if self.color_monitor.check_black_out(interval_ratio=3):
                self.printf("A wild pokemon encountered!")
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                self.cfg.i += 1
                self.update_count(self.cfg.i)
                break
        pass

    def stationary_encountering(self, hitkeys=[]):
        for key in hitkeys:
            self.press_controller.hit_key(key)
        # hit 'A' till encounter
        while 1:
            self.press_controller.hit_key(self.key("A"))
            if self.color_monitor.check_black_out():
                self.printf("Encountered!")
                while self.color_monitor.check_black_out():
                    sleep(0.98)

                self.cfg.i += 1
                self.update_count(self.cfg.i)
                break
            sleep(0.1)

    def fishing_rse_encountering(self):
        fishflag: bool = False
        while 1:
            self.printf("Fishing...")
            self.press_controller.hit_key(self.key("SELECT"))
            fishflag = False
            sleep(0.5)

            while 1:
                if self.color_monitor.check("get_fish"):
                    self.press_controller.hit_key(self.key("A"))
                    self.printf("Got pokemon!")
                    sleep(0.2)
                    fishflag = True
                    break
                elif self.color_monitor.check("no_fish"):
                    # not even a nibble
                    self.press_controller.hit_key(self.key("A"))
                    self.printf("Not even a nibble...")
                    # sleep(0.5)
                    break
                sleep(0.1)

            if not fishflag:
                # no fish
                while self.color_monitor.check("normal_dialogue"):
                    self.press_controller.hit_key(self.key("B"))
                    sleep(0.2)
                continue
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:

            # second rod
            while self.color_monitor.check("normal_dialogue"):
                if self.color_monitor.check("get_fish"):
                    self.press_controller.hit_key(self.key("A"))
                    sleep(0.1)
                    continue

                elif self.color_monitor.check("no_fish"):  # Actually we do have fish
                    self.press_controller.hit_key(self.key("A"))
                    sleep(0.1)
                    self.press_controller.hit_key(self.key("A"))
                    break

            while not self.color_monitor.check_black_out():
                # print("blackout?")
                self.press_controller.hit_key(self.key("B"))
                sleep(0.2)

            if self.color_monitor.check_black_out():
                self.printf("Encountered!")
                flag = True
                while self.color_monitor.check_black_out():
                    if flag:
                        sleep(0.98)
                        flag = False
                self.cfg.i += 1
                self.update_count(self.cfg.i)
                # unregister(exit_print_i)
                # register(exit_print_i, i=cfg.i, cfg=cfg)
                break

    def after_SL(self):
        sleep(2)

        if self.ifFRLG:
            sleep(2)
        self.press_controller.hit_key(self.key("A"))
        self.printf("Hit A")
        self.press_controller.hit_key(self.key("A"))
        self.printf("Hit A")
        sleep(0.5)
        self.press_controller.hit_key(self.key("A"))
        self.printf("Hit A")
        if not self.ifFRLG:
            sleep(0.5)

        # hit 'A' till entering
        while 1:
            self.press_controller.hit_key(self.key("A"))
            if self.color_monitor.check_black_out():
                self.printf("Entering save-choose ui.")
                break
            sleep(0.1)

        while 1:
            self.press_controller.hit_key(self.key("A"))
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:
            if self.color_monitor.check_black_out():
                self.printf("Entering game.")
                break
            sleep(0.1)

        # if ifFRLG:
        if self.ifFRLG:
            sleep(2)
            # skip memory recall 跳过回忆
            self.press_controller.hit_key(self.key("B"))
            sleep(0.5)
            # continue

    def SL(self):
        """
        eo SL once
        """
        self.press_controller.key_down(self.key("A"))
        self.press_controller.key_down(self.key("B"))
        self.press_controller.key_down(self.key("START"))
        self.press_controller.key_down(self.key("SELECT"))
        sleep(0.3)
        self.press_controller.key_up(self.key("A"))
        self.press_controller.key_up(self.key("B"))
        self.press_controller.key_up(self.key("START"))
        self.press_controller.key_up(self.key("SELECT"))

    def exit_print_i(self):
        self.printf("No shiny pokemon in {} times.".format(self.cfg.i))
        self.cfg.write_count_config()

    def send_mail(self):
        if self.cfg.ifsend:
            self.color_monitor.save_image()
            try:
                send_mail(
                    self.cfg.i,
                    self.cfg.to_mail,
                    self.cfg.mail_host,
                    self.cfg.send_mail,
                    self.cfg.send_mail_password,
                    self.printf,
                )
            except:
                self.printf("Please open config.ini file to config email information.")
