from time import sleep
from random import choice

from core.autopoke_core import AutoPokeCore
from core.stationary_encounter_core import StationaryEncounteringFactory


class AutoPokeCoreStationary(AutoPokeCore):
    def __init__(self, func: str, **kwargs):
        super().__init__(**kwargs)
        self.func = func
        self.mode = 1
        self.delay_list = [a / 100 for a in range(0, 60, 2)]
        self.encountering = (
            StationaryEncounteringFactory(
                self.color_monitor, self.hit_key, self.printf, self.add_one_count
            )
            .get_encountering(self.func, self.extra_value)
            .encounter
        )

    def function(self):
        if self.func == "Normal Hit A":
            self.NormalHitA()
        elif self.func == "FrLg Starters":
            self.StartersFrLg()
        elif self.func == "RSE Starters":
            self.StartersRSE()
        elif self.func == "FrLg Gifts":
            self.GiftsFrLg()
        pass

    def NormalHitA(self):

        while 1:
            sleep(choice(self.delay_list))

            self.encountering()
            if self.check_shiny():
                break

            self.printf("Not shiny, SLing...")
            self.SL()
            self.after_SL()
        pass

    def GiftsFrLg(self):
        self.ifFRLG = True
        while 1:
            sleep(choice(self.delay_list))
            self.encountering()
            # print("start checking")
            if self.check_shiny_in_bag(no_dex=False, first=False):
                break

            self.printf("Not shiny, SLing...")
            self.SL()
            self.after_SL()
        pass

    def StartersFrLg(self):
        self.ifFRLG = True
        while 1:
            sleep(choice(self.delay_list))

            self.encountering()
            # print("start checking")
            if self.check_shiny_in_bag(no_dex=True, first=True):
                break

            self.printf("Not shiny, SLing...")
            self.SL()
            self.after_SL()
        pass

    def StartersRSE(self):
        self.ifFRLG = False
        last_delay = (
            0 if self.config.general.game_version == "E" else choice(self.delay_list)
        )
        while 1:
            new_delay = (
                last_delay + 1 / 60
                if self.config.general.game_version == "E"
                else choice(self.delay_list)
            )
            sleep(new_delay)
            last_delay = new_delay

            self.encountering()
            # print("start checking")
            if self.check_shiny_rse_starters():
                break

            self.printf("Not shiny, SLing...")
            self.SL()
            self.after_SL()
        pass
