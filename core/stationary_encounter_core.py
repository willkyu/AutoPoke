from time import sleep


from core.color_core import ColorMonitor


class Encountering(object):
    def __init__(self, color_monitor: ColorMonitor, hit_key, printf, add_one_count):
        self.color_monitor = color_monitor
        self.hit_key = hit_key
        self.printf = printf
        self.add_one_count = add_one_count
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

    def get_encountering(self, func) -> Encountering:
        if func == "Normal Hit A":
            return HitAEncountering(
                self.color_monitor, self.hit_key, self.printf, self.add_one_count
            )
        elif func == "FrLg Starters":
            return StartersFrLgEncountering(
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
