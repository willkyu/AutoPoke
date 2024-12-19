# from multiprocessing.connection import wait
from time import sleep
from typing import Literal
from random import random

from core.press_core import PressController
from core.color_core import ColorMonitor, read_color
from core.mail_core import send_mail
from core.config import Config
from core.notification_core import send_toast


class AutoPokeCore(object):
    def __init__(self, eo, cfg: Config, printf, update_count) -> None:
        # self.color_monitor: ColorMonitor
        self.hander = eo
        self.config = cfg
        self.printf = printf
        self.update_count = update_count
        self.press_controller = PressController(self.hander)
        read_color(self.config.color)
        self.color_monitor = ColorMonitor(self.hander, self.printf)
        self.language = self.config.general.game_language
        self.ifFRLG = self.config.general.game_version == "FrLg"

        pass

    def key(self, key: str):
        return self.config.key_mapping.__dict__[key.lower()]

    def release_all_keys(self):
        self.press_controller.release_all_keys(
            self.config.key_mapping.__dict__.values()
        )

    def check_shiny(self):
        # 遇敌黑屏到第一次按A的时间
        sleep(3.9)
        if self.language == "Jpn":
            sleep(1)
        self.hit_key("A")
        # self.hit_key("A")
        # self.printf("Hit A.")

        # safari zone 判定
        sleep(0.2)
        if self.color_monitor.check("ally_battle_status"):
            return False

        self.printf("Not safari...")
        # 非safari zone额外等待时间
        sleep(2.7)

        if not self.color_monitor.check("ally_battle_status"):
            self.printf(
                "Got Shiny Pokemon! {} times.".format(
                    self.config.general.count[self.mode]
                )
            )
            self.shiny_handle()
            return True
        return False

    def check_shiny_in_bag(self, no_dex=False, first=False):
        self.hit_key("START", time=0.3)
        self.hit_key("DOWN", time=0.1) if not no_dex else None
        sleep(0.1)
        self.hit_key("A", time=0.1)
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                break
        if not first:
            self.hit_key("UP", time=0.1)
            sleep(0.1)
            self.hit_key("UP", time=0.1)
        self.hit_key("A", time=0.1)
        sleep(0.1)
        self.hit_key("A", time=0.1)
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                break
        sleep(0.3)
        if self.ifFRLG and self.color_monitor.check("shiny_star"):
            self.shiny_handle()
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

    def RUN(self):
        self.hit_key("RIGHT")
        self.hit_key("DOWN")
        self.hit_key("A")
        sleep(0.3)
        while not self.color_monitor.check_black_out():
            self.hit_key("A", time=0.1)
            # print("A")
            # sleep(0.1)
            # self.hit_key("B")
        while self.color_monitor.check_black_out():
            # print("black")
            sleep(0.1)
        sleep(1.2)

    def after_SL(self):
        sleep(2)
        sleep(random())
        if self.ifFRLG:
            sleep(2)
        self.hit_key("A")
        self.hit_key("A")
        sleep(0.5)
        self.hit_key("A")
        if self.ifFRLG:
            while 1:
                self.hit_key("A")
                if self.color_monitor.check_white_out():
                    # self.printf("whiteout")
                    self.printf("Entering save-choose ui.")
                    break
                sleep(0.3)
        else:
            sleep(0.5)

            # hit 'A' till entering
            while 1:
                self.hit_key("A")
                if self.color_monitor.check_black_out():
                    self.printf("Entering save-choose ui.")
                    break
                sleep(0.3)

        while 1:
            self.hit_key("A")
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:
            if self.color_monitor.check_black_out():
                self.printf("Entering game.")
                break
            sleep(0.1)

        # if ifFRLG:
        if self.ifFRLG:
            self.hit_key("B")
            sleep(0.3)
            self.hit_key("B")
            self.printf("Skip Memory...")
            # skip memory recall 跳过回忆
            self.hit_key("B")
            sleep(2)
            # print("finish skip")
            # continue
        sleep(random() * 3)
        self.printf("Finish SL.")

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

    # def exit_print_i(self):
    #     self.printf("No shiny pokemon in {} times.".format(self.config.general.count[self.mode]))
    #     self.config.save_config()

    def shiny_handle(self):
        self.color_monitor.save_image()
        self.send_mail()
        self.send_notification()
        self.update_count(0)

    def send_mail(self):
        if self.config.mail.send_mail:
            try:
                send_mail(
                    self.config.general.count[self.mode],
                    self.config.mail.inbox_address,
                    self.config.mail.outbox_smtp_host,
                    self.config.mail.outbox_address,
                    self.config.mail.outbox_authorization_code,
                    self.printf,
                )
            except:
                self.printf("Please open config.ini file to config email information.")

    def send_notification(self):
        if self.config.general.send_notification:
            send_toast(self.config.general.count[self.mode])

    def add_one_count(self):
        self.config.general.count[self.mode] += 1
        self.update_count(self.config.general.count[self.mode])

    def hit_key(self, key: str, time: float = 0.3):
        self.press_controller.hit_key(self.key(key), time)

    def exe_function(self):
        self.function()
        self.release_all_keys()
        pass

    def function(self):
        pass


class AutoPokeCoreFactory(object):
    def __init__(self, eo, cfg: Config, printf, update_count):
        self.eo, self.config, self.printf, self.update_count = (
            eo,
            cfg,
            printf,
            update_count,
        )

        pass

    def get_autopoke_core(self, mode: Literal[0, 1], function: str) -> AutoPokeCore:
        from core.autopoke_core_wild import AutoPokeCoreWildPm
        from core.autopoke_core_stationary import AutoPokeCoreStationary

        return (
            AutoPokeCoreWildPm(
                function,
                eo=self.eo,
                cfg=self.config,
                printf=self.printf,
                update_count=self.update_count,
            )
            if mode == 0
            else AutoPokeCoreStationary(
                function,
                eo=self.eo,
                cfg=self.config,
                printf=self.printf,
                update_count=self.update_count,
            )
        )
