from time import sleep


from core.color_core import ColorMonitor


class Encountering(object):
    def __init__(
        self,
        color_monitor: ColorMonitor,
        hit_key,
        printf,
        add_one_count,
        extra_value: str = "",
    ):
        self.color_monitor = color_monitor
        self.hit_key = hit_key
        self.printf = printf
        self.add_one_count = add_one_count
        self.extra_value = extra_value
        pass

    def encounter(self):
        pass


class StationaryEncounteringFactory(object):
    def __init__(self, color_monitor: ColorMonitor, hit_key, printf, add_one_count):
        self.color_monitor = color_monitor
        self.hit_key = hit_key
        self.printf = printf
        self.add_one_count = add_one_count
        pass

    def get_encountering(self, func, extra_value: str = "") -> Encountering:
        if func == "Normal Hit A":
            return HitAEncountering(
                self.color_monitor, self.hit_key, self.printf, self.add_one_count
            )
        elif func == "FrLg Starters":
            return StartersFrLgEncountering(
                self.color_monitor, self.hit_key, self.printf, self.add_one_count
            )
        elif func == "RSE Starters":
            assert extra_value in ["left", "right", "center"]
            return StartersRSEEncountering(
                self.color_monitor,
                self.hit_key,
                self.printf,
                self.add_one_count,
                extra_value,
            )
        elif func == "FrLg Gifts":
            return GiftFrLgEncountering(
                self.color_monitor, self.hit_key, self.printf, self.add_one_count
            )


class HitAEncountering(Encountering):
    def encounter(self):
        # hit 'A' till encounter
        while 1:
            self.hit_key("A")
            if self.color_monitor.check_black_out():
                self.printf("Encountered!")
                while self.color_monitor.check_black_out():
                    sleep(0.98)

                self.add_one_count()
                break
            sleep(0.1)


class StartersFrLgEncountering(Encountering):
    def encounter(self):
        self.hit_key("A")
        sleep(1)
        self.hit_key("A")
        sleep(1)
        self.hit_key("A")
        count_no_dialogue = 0
        while 1:
            self.hit_key("B")
            # print("hit b")
            # sleep(3)
            if not self.color_monitor.check(
                "dialogue_for_FrLg_Starters_and_RS_fishing"
            ):
                count_no_dialogue += 1
                # print(count_no_dialogue)
                if count_no_dialogue == 1:
                    sleep(2)
                else:
                    self.add_one_count()
                    break

            sleep(0.2)


class GiftFrLgEncountering(Encountering):
    def encounter(self):
        while 1:
            self.hit_key("A")
            sleep(1)
            # print("hit b")
            # sleep(3)
            if not self.color_monitor.check(
                "dialogue_for_FrLg_Starters_and_RS_fishing"
            ):
                self.add_one_count()
                break

            # sleep(0.2)


class StartersRSEEncountering(Encountering):
    def encounter(self):
        self.hit_key("A")
        sleep(1)
        self.hit_key(self.extra_value.upper()) if self.extra_value != "center" else None
        sleep(1)
        self.hit_key("A")
        sleep(1)
        self.hit_key("A")
        while not self.color_monitor.check_black_out():
            sleep(0.1)
        if self.color_monitor.check_black_out():
            self.printf("A wild pokemon encountered!")
            while self.color_monitor.check_black_out():
                sleep(0.98)
            self.add_one_count()

        # while 1:
        #     self.hit_key("B")
        #     # print("hit b")
        #     # sleep(3)
        #     if not self.color_monitor.check(
        #         "dialogue_for_FrLg_Starters_and_RS_fishing"
        #     ):
        #         # print(count_no_dialogue)
        #         if count_no_dialogue == 1:
        #             sleep(2)
        #         else:
        #             self.add_one_count()
        #             break

        #     sleep(0.2)
