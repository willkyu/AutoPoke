import flet as ft
from typing import Literal

from core.config import Config
from ui.GeneralUI import Block


class SettingsUI(ft.ListView):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.general_block = GeneralBlockView(self.config, spacing=10)
        self.mail_block = MailBlockView(self.config, spacing=10)
        self.key_block = KeyBlockView(self.config, spacing=0)
        self.color_block = ColorBlockView(self.config, spacing=10)
        self.interval_block = IntervalBlockView(self.config, spacing=10)
        self.controls = [
            self.general_block,
            divider,
            self.mail_block,
            divider,
            self.key_block,
            divider,
            self.color_block,
            divider,
            self.interval_block,
        ]
        self.spacing = 10


class SettingTittle(ft.Row):
    def __init__(self, title: str, icon: str, **kwargs):
        super().__init__(**kwargs)
        self.controls = [
            ft.Icon(icon),
            ft.Text(f"{title}:", size=30, weight=ft.FontWeight.BOLD),
        ]


class GeneralBlockView(ft.Column):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.controls = [
            SettingTittle("General", ft.icons.SETTINGS_OUTLINED),
            Block_General(
                "Game Language",
                ft.Dropdown(
                    label="Language",
                    options=[ft.dropdown.Option(lan) for lan in ["Eng", "Jpn"]],
                    border_color=ft.colors.GREY_800,
                    width=150,
                ),
                self.config,
            ),
            divider_small,
            Block_General(
                "Game Version",
                ft.Dropdown(
                    label="Version",
                    options=[ft.dropdown.Option(lan) for lan in ["RS", "E", "FrLg"]],
                    border_color=ft.colors.GREY_800,
                    width=150,
                ),
                self.config,
            ),
            divider_small,
            Block_General("Send Notification", ft.Checkbox(), self.config),
            divider_small,
            Block_General(
                "Window Name",
                ft.TextField(
                    hint_text="Input here.",
                    height=40,
                    border_color=ft.colors.GREY_800,
                ),
                self.config,
            ),
        ]


class Block_General(Block):
    def __init__(self, text: str, another, config: Config, expand=0):
        self.config = config
        self.name = text
        # print(self.text)
        super().__init__(
            text + ":",
            another,
            general_setting_tips_dict[text],
            expand=expand,
            spacing=0,
        )
        self.another.value = getattr(self.config.general, get_variable(self.name))
        self.another.on_change = self.on_update

    def on_update(self, e: ft.ControlEvent):
        setattr(self.config.general, get_variable(self.name), e.control.value)
        self.config.save_config()


class MailBlockView(ft.Column):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.controls = [
            SettingTittle("Mail", ft.icons.MAIL_ROUNDED),
            Block_Mail("Send Mail", ft.Checkbox(), self.config),
        ] + [
            x
            for item in zip(
                [divider_small] * (len(mail_setting_tips_dict) - 1),
                [
                    Block_Mail(
                        key,
                        ft.TextField(
                            hint_text="Input here.",
                            height=40,
                            border_color=ft.colors.GREY_800,
                        ),
                        self.config,
                    )
                    for key in list(mail_setting_tips_dict.keys())[1:]
                ],
            )
            for x in item
        ]


class Block_Mail(Block):
    def __init__(self, text: str, another, config: Config, expand=0):
        self.config = config
        self.name = text
        # print(self.text)
        super().__init__(
            text + ":",
            another,
            mail_setting_tips_dict[text],
            expand=expand,
            spacing=0,
        )
        self.another.value = getattr(self.config.mail, get_variable(self.name))
        self.another.on_change = self.on_update

    def on_update(self, e: ft.ControlEvent):
        setattr(self.config.mail, get_variable(self.name), e.control.value)
        self.config.save_config()


class KeyBlockView(ft.Column):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.controls = [
            SettingTittle("Kep Mapping", ft.icons.KEYBOARD_ROUNDED),
        ] + [
            Block_Key(
                key,
                ft.TextField(
                    hint_text="Key.",
                    height=40,
                    border_color=ft.colors.GREY_800,
                ),
                self.config,
            )
            for key in [
                key.capitalize() for key in self.config.key_mapping.__dict__.keys()
            ]
        ]


class Block_Key(Block):
    def __init__(self, text: str, another, config: Config, expand=0):
        self.config = config
        self.name = text
        # print(self.text)
        super().__init__(
            text + ":",
            another,
            "",
            expand=expand,
            spacing=0,
        )
        self.another.value = getattr(self.config.key_mapping, get_variable(self.name))
        self.another.on_change = self.on_update

    def on_update(self, e: ft.ControlEvent):
        setattr(self.config.key_mapping, get_variable(self.name), e.control.value)
        self.config.save_config()


class ColorBlockView(ft.Column):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.controls = [
            SettingTittle("Colors", ft.icons.COLOR_LENS_ROUNDED),
            ft.Text(value="Color customization is coming soon."),
        ]


class IntervalBlockView(ft.Column):
    def __init__(self, config: Config, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.controls = [
            SettingTittle("Intervals", ft.icons.TIMER_OUTLINED),
            ft.Text(value="Time interval customization is coming soon."),
        ]


def get_variable(text: str):
    return text.lower().replace(" ", "_")


divider_small = ft.Divider(thickness=0.5, height=0.5)
divider = ft.Divider(thickness=2, height=2)

general_setting_tips_dict = {
    "Game Language": "游戏语言。\nGame Language.",
    "Game Version": "游戏版本。RS代表红蓝宝石，E代表绿宝石，FrLg代表火红叶绿。\nGame version, where RS represents Ruby and Sapphire, E is Emerald, and FrLg denotes Fire red and Leaf green.",
    "Send Notification": "出闪后是否发送系统通知。\nWhether send Windows notification when getting shiny PM.",
    "Window Name": "Playback的窗口名称。通常不需要修改这项，除非你要使用模拟器而非GBO。\nThe window name of Playback software. Usually this shouldn't be modified unless you wanna use an emulator instead of GBO.",
}

mail_setting_tips_dict = {
    "Send Mail": "出闪后是否发送邮件。\nWhether send mail when getting shiny PM.",
    "Inbox Address": "收件箱地址。\nInbox address.",
    "Outbox Address": "发件箱地址。\nOutbox address.",
    "Outbox SMTP Host": "发件箱SMTP服务器。\nOutbox SMTP host.",
    "Outbox Authorization Code": "发件箱授权码。\nOutbox authorization code.",
}
