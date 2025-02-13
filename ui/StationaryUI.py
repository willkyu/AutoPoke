import flet as ft
from typing import Literal

from core.config import Config
from ui.GeneralUI import ControlAndTips
from ui.PannelUI import Panel


class StationaryUI(ft.Column):
    def __init__(self, config: Config, auto_poke_ui: object, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.extra_value = ""
        self.pannel = Panel(self.config, auto_poke_ui, mode=1, func="", width=200)
        self.pannel_and_tips = ControlAndTips(pannel=self.pannel, width=200)
        self.target_dropdown = ft.Dropdown(
            label="Target",
            options=[
                ft.dropdown.Option(target) for target in support_target_dict.keys()
            ],
            on_change=self.dropdown_on_change,
            # expand=1,
        )
        self.tips_view = TipsView(self.update_extra_value)
        self.controls = [
            ft.Container(
                content=self.target_dropdown, height=80, alignment=ft.alignment.center
            ),
            ft.Divider(thickness=1, height=1),
            ft.Row(
                [
                    ft.Container(self.tips_view, width=150),
                    ft.Container(
                        self.pannel_and_tips,
                        expand=True,
                        alignment=ft.alignment.bottom_center,
                    ),
                ],
                expand=True,
            ),
            # self.extra_view,
        ]
        # print(id(self.pannel_and_tips))

    def dropdown_on_change(self, e: ft.ControlEvent):
        # print(type(e))
        self.tips_view.update_value(e.control.value)
        self.pannel_and_tips.pannel.func = e.control.value
        # print(self.pannel_and_tips.pannel.func)
        # self.extra_view.update_extra_view(e.control.value)
        self.tips_view.update()

    def update_extra_value(self, extra_value):
        self.pannel_and_tips.pannel.extra_value = extra_value
        print(extra_value)


class TipsView(ft.Container):
    def __init__(self, update_func, **kwargs):
        super().__init__(expand=True, **kwargs)
        self.update_func = update_func
        self.tip_view = ft.Text(
            value="选择刷闪目标。\nChoose your target.",
            size=13,
            color=ft.colors.GREY,
        )
        self.alignment = ft.alignment.top_left
        self.extra_view = ExtraView(self.update_extra_value)
        self.content = ft.Column([self.tip_view, self.extra_view])

    def update_value(self, target_name):
        self.tip_view.value = support_target_dict[target_name]
        self.extra_view.update_extra_view(target_name)
        self.update()
        # self.alignment = ft.alignment.center

    def update_extra_value(self, extra_value):
        self.update_func(extra_value)
        # print(self.extra_value)


class ExtraView(ft.Container):
    def __init__(self, update_func, **kwargs):
        super().__init__(**kwargs)
        self.visible = False
        self.update_value = update_func
        self.view = ft.Container()
        self.content = ft.Column([ft.Divider(thickness=1, height=1), self.view])

    def update_extra_view(self, func: str):
        print(func)
        if func == "RSE Starters":
            self.view.content = ft.RadioGroup(
                content=ft.Column(
                    [
                        ft.Radio(label="木守宫\nTreecko", value="left"),
                        ft.Radio(label="火稚鸡\nTorchic", value="center"),
                        ft.Radio(label="水跃鱼\nMudkip", value="right"),
                    ]
                ),
                on_change=lambda e: self.update_value(e.control.value),
            )
            self.view.content.value = "center"
            self.update_value("center")
        else:
            self.visible = False
            # self.update()
            return
        self.visible = True
        # self.update()
        pass


support_target_dict = {
    "Normal Hit A": "最简单的一直按A直到进入战斗。\nSimply hit A untill battle begins.",
    "FrLg Starters": "火叶初始御三家。\nStarters in FrLg.",
    "RSE Starters": "宝石御三家。\nStarters in RSE.",
    "FrLg Gifts": "火叶礼物宝可梦，如火叶伊布等。需要将菜单指针移动至第一项。",
    "Coming Soon": "敬请期待后续功能。\nNew features coming soon.",
}
