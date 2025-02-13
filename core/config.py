import pickle
import os
from dataclasses import dataclass, field
from typing import Literal

VERSION = "V6.0.1_build5"

ColorConfigType = list[tuple[int]]


@dataclass
class MailConfig:
    send_mail: bool = False
    inbox_address: str = ""
    outbox_address: str = ""
    outbox_smtp_host: str = ""
    outbox_authorization_code: str = ""


@dataclass
class MoveConfig:
    lr: bool = True
    run: bool = False
    # sweet_scent: bool = False
    repel: bool = False


@dataclass
class KeyMappingConfig:
    up: str = "UP"
    down: str = "DOWN"
    left: str = "LEFT"
    right: str = "RIGHT"
    a: str = "X"
    b: str = "Z"
    start: str = "ENTER"
    select: str = "BACKSPACE"


@dataclass(order=True)
class AutoPokeVersion:
    a: int = 0
    b: int = 0
    c: int = 0
    build: int = 0

    def __str__(self):
        return f"V{self.a}.{self.b}.{self.c}_build{self.build}"

    def from_str(self, string: str):
        string = string[1:]
        assert len(string.split(".")) == 3
        a, b, c0 = string.split(".")
        assert len(c0.split("_build")) == 2
        c, d = c0.split("_build")
        assert a.isdigit() and b.isdigit() and c.isdigit() and d.isdigit()
        self.a, self.b, self.c, self.build = int(a), int(b), int(c), int(d)


@dataclass
class ColorConfig:
    color_distance: float = 10.0
    dialogue_color_main: ColorConfigType = field(
        default_factory=lambda: (255, 251, 255)
    )
    dialogue_color_rainy: ColorConfigType = field(default_factory=lambda: (77, 76, 77))
    text_color: ColorConfigType = field(default_factory=lambda: (74, 73, 74))
    bg_deep_green: ColorConfigType = field(default_factory=lambda: (107, 162, 165))
    bg_deep_blue: ColorConfigType = field(default_factory=lambda: (41, 81, 107))
    bg_yellow: ColorConfigType = field(default_factory=lambda: (255, 251, 222))
    shiny_star_yellow: ColorConfigType = field(default_factory=lambda: (255, 210, 82))


@dataclass
class IntervalConfig:
    press_duration: float = 0.1


@dataclass
class GeneralConfig:
    autopoke_version: AutoPokeVersion = AutoPokeVersion()
    game_language: Literal["Eng", "Jpn"] = "Eng"
    game_version: Literal["RS", "E", "FrLg"] = "RS"
    window_name: str = "Playback"
    count: list[int] = field(default_factory=lambda: [0, 0])
    send_notification: bool = True
    auto_update: bool = True
    first_time: bool = True

    def __post_init__(self):
        self.autopoke_version.from_str(VERSION)


class Config:
    def __init__(self, file="AutoPoke.willkyu.config") -> None:
        self.file = file
        if not self.read_config():
            self.set_default_config()

    def read_config(self):
        if not os.path.exists(self.file):
            return False
        with open(self.file, "rb") as fp:
            self.__dict__.update(pickle.load(fp).__dict__)
        return True

    def save_config(self):
        with open(self.file, "wb") as fp:
            pickle.dump(self, fp)

    def set_default_config(self):
        self.general = GeneralConfig()
        self.mail = MailConfig()
        self.color = ColorConfig()
        self.key_mapping = KeyMappingConfig()
        self.interval = IntervalConfig()
        self.move = MoveConfig()
        self.save_config()
