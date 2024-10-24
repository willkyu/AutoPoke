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
        pass

    def exe_function(self, function: str):
        # try:
        # with ColorMonitor(self.hander, self.printf) as self.color_monitor:
        self.color_monitor = ColorMonitor(self.hander, self.printf)
        if function == "WILDPOKE":
            self.WILDPOKE()
        elif function == "STATIONARY":
            self.STATIONARY()
        elif function == "FISHING" and self.cfg.version in ["RS", "E"]:
            self.FISHING_RSE()
        # except Exception as e:
        #     self.printf(str(e))
        self.release_all_keys()

    def release_all_keys(self):
        self.press_controller.release_all_keys(self.cfg.keymap.values())

    def key(self, str):
        return self.cfg.keymap[str]

    def WILDPOKE(self):
        jump = eval(self.cfg.mode_config["jump"])
        run = eval(self.cfg.mode_config["run"])
        ifLR = eval(self.cfg.mode_config["iflr"])

        # 默认左右走，ifLR=False时，上下走
        move_key_list = (
            [self.key("LEFT"), self.key("RIGHT")]
            if ifLR
            else [self.key("UP"), self.key("DOWN")]
        )

        # 开始遇敌
        self.printf("Encountering...")
        while 1:
            if jump or run:
                self.press_controller.key_down(self.key("B"))
            while 1:
                if not jump:
                    self.press_controller.random_hit_key(move_key_list)
                else:
                    sleep(0.1)

                if self.color_monitor.check_black_out():
                    self.printf("A wild pokemon encountered!")
                    if jump or run:
                        self.press_controller.key_up(self.key("B"))
                    while self.color_monitor.check_black_out():
                        sleep(0.98)
                    self.cfg.i += 1
                    self.update_count(self.cfg.i)
                    break
                elif self.cfg.version == "E":
                    if self.color_monitor.check("normal_dialogue"):
                        # self.printf("PokeNav detected.")
                        if jump or run:
                            self.press_controller.key_up(self.key("B"))
                            sleep(0.2)
                        while self.color_monitor.check("normal_dialogue"):
                            self.press_controller.hit_key(self.key("B"))
                            sleep(0.2)
                        if jump or run:
                            self.press_controller.key_down(self.key("B"))
                            sleep(0.2)

            # 遇敌黑屏到第一次按A的时间
            sleep(3.6)
            # 绿宝石额外动画时间
            if self.cfg.version == "E":
                sleep(1)
            self.press_controller.hit_key(self.key("A"))
            self.press_controller.hit_key(self.key("A"))
            self.printf("Hit A.")

            # safari zone 判定
            sleep(0.5)
            if self.color_monitor.check("ally_battle_status"):
                self.printf("Not shiny, run...")
                self.RUN()
                continue

            self.printf("not safari...")
            # 非safari zone额外等待时间
            sleep(2.5)

            if not self.color_monitor.check("ally_battle_status"):
                self.printf("Got Shiny Pokemon! {} times.".format(self.cfg.i))
                self.send_mail()
                self.cfg.i = 0
                self.cfg.write_count_config()
                break

            # 额外动画检测
            if self.color_monitor.check(
                "battle_dialogue_RSE"
            ) or self.color_monitor.check("battle_dialogue_FrLg"):
                self.printf("Special anime detected.")
                while 1:
                    if not self.color_monitor.check(
                        "battle_dialogue_RSE"
                    ) and not self.color_monitor.check("battle_dialogue_FrLg"):
                        sleep(0.02)
                        break
                    sleep(0.1)

            self.printf("Not shiny, run...")
            self.RUN()
            self.printf("Encountering...")

    def STATIONARY(self, hitkeys=[]):
        ifFRLG = self.cfg.version == "FrLg"
        delay_list = [a / 100 for a in range(0, 60, 2)]

        while 1:
            sleep(choice(delay_list))
            for key in hitkeys:
                self.press_controller.hit_key(key)

            # hit 'A' till encounter
            while 1:
                self.press_controller.hit_key(self.key("A"))
                if self.color_monitor.check_black_out():
                    self.printf("encountered!")
                    while self.color_monitor.check_black_out():
                        sleep(0.98)

                    self.cfg.i += 1
                    self.update_count(self.cfg.i)
                    break
                sleep(0.1)

            sleep(4)
            self.press_controller.hit_key(self.key("A"))
            self.printf("Hit A.")
            sleep(3)

            if not self.color_monitor.check("ally_battle_status"):
                self.printf("Got Shiny Pokemon!")
                self.send_mail()
                self.cfg.i = 0
                self.cfg.write_count_config()
                break

            self.printf("SLing...")
            self.SL()
            sleep(2)

            if ifFRLG:
                sleep(2)
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
                sleep(0.5)
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
            else:
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
                sleep(0.5)
                self.press_controller.hit_key(self.key("A"))
                self.printf("Hit A")
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
            if ifFRLG:
                sleep(2)
                # skip memory recall 跳过回忆
                self.press_controller.hit_key(self.key("B"))
                sleep(0.5)
                continue
        pass

    def FISHING_RSE(self):

        fishflag: bool = False
        while 1:
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

                    elif self.color_monitor.check(
                        "no_fish"
                    ):  # Actually we do have fish
                        self.press_controller.hit_key(self.key("A"))
                        sleep(0.1)
                        self.press_controller.hit_key(self.key("A"))
                        break

                while not self.color_monitor.check_black_out():
                    # print("blackout?")
                    self.press_controller.hit_key(self.key("B"))
                    sleep(0.2)

                if self.color_monitor.check_black_out():
                    self.printf("encountered!")
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

            # 遇敌黑屏到第一次按A的时间
            sleep(3.6)
            self.press_controller.hit_key(self.key("A"))
            self.press_controller.hit_key(self.key("A"))
            self.printf("Hit A.")

            # safari zone 判定
            sleep(0.2)
            if self.color_monitor.check("ally_battle_status"):
                self.printf("Not shiny, run...")
                self.RUN()
                continue

            self.printf("not safari...")
            # 非safari zone额外等待时间
            sleep(2.8)

            if self.color_monitor.check("ally_battle_status"):
                self.printf("Got Shiny Pokemon! {} times.".format(self.cfg.i))
                self.send_mail()
                self.cfg.i = 0
                self.cfg.write_count_config()
                break

            # 额外动画检测
            if self.color_monitor.check(
                "battle_dialogue_RSE"
            ) or self.color_monitor.check("battle_dialogue_FrLg"):
                self.printf("Special anime detected.")
                while 1:
                    if not self.color_monitor.check(
                        "battle_dialogue_RSE"
                    ) and not self.color_monitor.check("battle_dialogue_FrLg"):
                        sleep(0.02)
                        break
                    sleep(0.1)

            self.printf("Not shiny, run...")
            self.RUN()
            self.printf("Encountering...")

        pass

    def RUN(self):
        self.press_controller.hit_key(self.key("RIGHT"))
        self.press_controller.hit_key(self.key("DOWN"))
        self.press_controller.hit_key(self.key("A"))
        sleep(0.5)
        self.press_controller.hit_key(self.key("A"))
        sleep(2.7)

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
