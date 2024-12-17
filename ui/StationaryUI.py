import flet as ft
from typing import Literal

from core.config import Config
from ui.GeneralUI import ControlAndTips
from ui.PannelUI import Panel


class StationaryUI(ft.Column):
    def __init__(self, config: Config, auto_poke_ui: object, **kwargs):
        super().__init__(**kwargs)
        self.config = config

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
        self.tips_view = TipsView()
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
        ]
        # print(id(self.pannel_and_tips))

    def dropdown_on_change(self, e: ft.ControlEvent):
        # print(type(e))
        self.tips_view.update_value(e.control.value)
        self.pannel_and_tips.pannel.func = e.control.value
        # print(self.pannel_and_tips.pannel.func)
        self.tips_view.update()


class TipsView(ft.Container):
    def __init__(self, **kwargs):
        super().__init__(expand=True, **kwargs)
        self.tip_view = ft.Text(
            value="选择刷闪目标。\nChoose your target.",
            size=13,
            color=ft.colors.GREY,
        )
        self.alignment = ft.alignment.top_left
        self.extra_view = ExtraView()
        self.content = ft.Column([self.tip_view, self.extra_view])

    def update_value(self, target_name):
        self.tip_view.value = support_target_dict[target_name]
        self.extra_view.update_extra_view(target_name)
        self.update()
        # self.alignment = ft.alignment.center


class ExtraView(ft.Column):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visible = False

    def update_extra_view(self, func: str):
        pass


support_target_dict = {
    "Normal Hit A": "最简单的一直按A直到进入战斗。\nSimply hit A untill battle begins.",
    "FrLg Starters": "火叶初始御三家。\nStarters in FrLg.",
    "Coming Soon": "敬请期待后续功能。\nNew features coming soon.",
}
