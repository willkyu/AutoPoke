from time import sleep, time

from core.autopoke_core import AutoPokeCore


class AutoPokeCoreWildPm(AutoPokeCore):
    def __init__(self, func: str, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.mode = 0

    def function(self):
        if self.func != "Fish":
            self.ifLR = self.config.move.lr
            self.jump = self.func == "Jump"
            self.run = self.config.move.run
            self.sweet_scent = self.func == "Sweet Scent"
            self.repel = self.config.move.repel
            self.WildPm()
        else:
            self.Fishing()

    def WildPm(self):
        if self.repel and not self.sweet_scent:
            self.use_repel()

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

    def Fishing(self):
        while 1:
            (
                self.fishing_rse_encountering()
                if not self.ifFRLG
                else self.fishing_frlg_encountering()
            )

            if self.check_shiny():
                break

            self.printf("Not shiny, run...")
            self.check_extra_anime()
            self.RUN()
            self.printf("Encountering...")

        pass

    def use_repel(self):
        self.printf("Using Repel...")
        self.hit_key("START")
        sleep(0.3)
        self.hit_key("A")
        sleep(0.3)
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                break
        self.hit_key("A", time=0.1)
        sleep(0.3)
        self.hit_key("A", time=0.1)
        while not self.color_monitor.check("dialogue"):
            self.hit_key("A", time=0.1)
        while 1:
            self.hit_key("B", time=0.1)
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                break
            sleep(0.3)
        self.hit_key("B", time=0.1)
        sleep(0.3)

    def wild_encountering(self):
        if self.jump or self.run:
            self.press_controller.key_down(self.key("B"))
        timestamp = None
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
                self.add_one_count()
                # self.config.general.count[self.mode] += 1
                # self.update_count(self.config.general.count[self.mode])
                break
            elif self.config.general.game_version == "E" or self.repel:
                if self.color_monitor.check("dialogue"):
                    if timestamp is None:
                        timestamp = time()
                        continue
                    elif time() - timestamp < 5:
                        continue
                    else:
                        # self.printf("PokeNav detected.")
                        if self.jump or self.run:
                            self.press_controller.key_up(self.key("B"))
                            sleep(0.2)
                        while self.color_monitor.check("dialogue"):
                            self.hit_key("B")
                            sleep(0.2)
                        if self.jump or self.run:
                            self.press_controller.key_down(self.key("B"))
                            sleep(0.2)
                        if self.repel:
                            self.use_repel()
                            timestamp = None

    def sweet_scent_encountering(self):
        self.hit_key("START")
        self.hit_key("A")
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                # self.add_one_count()
                break
            # else:
            #     print("not black out")
        self.hit_key("UP", time=0.1)
        sleep(0.1)
        self.hit_key("UP", time=0.1)
        self.hit_key("A", time=0.1)
        if self.ifFRLG:
            self.hit_key("DOWN", time=0.1)
        else:
            # self.press_controller.key_up(self.key(("A")))
            sleep(0.1)
        self.hit_key("A", time=0.1)
        self.printf("Using sweet scent.")
        while 1:
            if self.color_monitor.check_black_out():
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                # self.add_one_count()
                break
        sleep(1.5)
        while 1:
            if self.color_monitor.check_black_out(interval_ratio=3):
                self.printf("A wild pokemon encountered!")
                while self.color_monitor.check_black_out():
                    sleep(0.98)
                self.add_one_count()
                break
        pass

    def fishing_frlg_encountering(self):
        while 1:
            no_black_count = 10
            no_fish_flag = False
            self.printf("Fishing...")
            self.hit_key("SELECT")
            sleep(1)
            while self.color_monitor.check("dialogue"):
                self.hit_key("A")
                sleep(0.3)

            while not self.color_monitor.check_black_out():
                sleep(0.1)
                no_black_count -= 1
                if no_black_count <= 0:
                    no_fish_flag = True
                    break
            if no_fish_flag:
                continue
            self.printf("Encountered!")
            self.add_one_count()
            return

    def fishing_rse_encountering(self):
        fishflag: bool = False
        while 1:
            self.printf("Fishing...")
            self.hit_key("SELECT")
            fishflag = False
            sleep(0.5)

            while 1:
                if self.color_monitor.check("get_fish"):
                    self.hit_key("A")
                    self.printf("Got pokemon!")
                    sleep(0.1)
                    fishflag = True
                    break
                elif self.color_monitor.check("no_fish"):
                    # not even a nibble
                    self.hit_key("A")
                    self.printf("Not even a nibble...")
                    # sleep(0.5)
                    break
                sleep(0.2)

            if not fishflag:
                # no fish
                while self.color_monitor.check(
                    "dialogue_for_FrLg_Starters_and_RS_fishing"
                ):
                    self.hit_key("B")
                    sleep(0.2)
                continue
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:

            # second rod
            while self.color_monitor.check("dialogue_for_FrLg_Starters_and_RS_fishing"):
                if self.color_monitor.check("get_fish"):
                    print("next bite")
                    self.hit_key("A")
                    sleep(0.1)
                    continue

                elif self.color_monitor.check(
                    "encounter_fish"
                ):  # Actually we do have fish
                    print("getfish")
                    self.hit_key("A")
                    sleep(0.1)
                    self.hit_key("A")
                    break

            while not self.color_monitor.check_black_out():
                # print("blackout?")
                self.hit_key("B")
                sleep(0.2)

            if self.color_monitor.check_black_out():
                self.printf("Encountered!")
                flag = True
                while self.color_monitor.check_black_out():
                    if flag:
                        sleep(0.98)
                        flag = False
                self.add_one_count()
                # unregister(exit_print_i)
                # register(exit_print_i, i=cfg.i, cfg=cfg)
                break
