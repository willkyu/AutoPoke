import flet as ft
from typing import Literal

from core.config import Config
from ui.GeneralUI import BoolSettingItem, ControlAndTips
from ui.PannelUI import Panel


class WildPmUI(ft.Column):
    def __init__(self, config: Config, auto_poke_ui: object, **kwargs):
        super().__init__(**kwargs)
        self.config = config

        self.pannel = Panel(self.config, auto_poke_ui, mode=0, func="Move", width=200)
        self.pannel_and_tips = ControlAndTips(pannel=self.pannel, width=200)
        self.wild_pm_navigation_view = WildPmNavigationView(
            config, self.pannel_and_tips, width=150
        )
        self.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    icon=ft.icons.DIRECTIONS_WALK_ROUNDED,
                    label="Move",
                    # tooltip="Move for encounters.",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.MOTORCYCLE_ROUNDED,
                    label="Jump",
                    # tooltip="使用越野自行车跳跃来遇敌。\nRide Acro Bike and jump for emcounters.",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.FILTER_VINTAGE_ROUNDED,
                    label="Sweet Scent",
                    # tooltip="使用甜甜香气来遇敌。\nUse sweet scent for encounters.",
                ),
                ft.NavigationBarDestination(
                    icon=ft.icons.WATER_ROUNDED,
                    label="Fish",
                    # tooltip="使用各种钓竿钓鱼。\nUse various rods to fish.",
                ),
            ],
            on_change=lambda e: self.set_value(e.control.selected_index),
            bgcolor=ft.colors.with_opacity(0, "white"),
            indicator_shape=ft.StadiumBorder(),
            height=80,
        )
        self.controls = [
            self.navigation_bar,
            ft.Divider(thickness=1, height=1),
            ft.Row(
                controls=[
                    ft.Container(
                        self.wild_pm_navigation_view,
                        # expand=True,
                        alignment=ft.alignment.center,
                        width=150,
                    ),
                    ft.Container(
                        self.pannel_and_tips,
                        expand=True,
                        alignment=ft.alignment.center,
                    ),
                ],
                expand=True,
                # vertical_alignment=ft.CrossAxisAlignment.CENTER,
                # height=300,
            ),
        ]
        # print(id(self.pannel_and_tips))

    def set_value(self, value: int):
        if self.wild_pm_navigation_view.value == value:
            return
        assert value in [0, 1, 2, 3]
        self.pannel_and_tips.pannel.func = self.navigation_bar.destinations[value].label
        # print(self.pannel_and_tips.pannel.func)
        self.wild_pm_navigation_view.set_value(value)
        # self.pannel_and_tips.set_mode(value)
        # self.all_ui.set_show_extra(show_extra=False if value == 2 else True)
        self.page.update()


class WildPmNavigationView(ft.Container):
    def __init__(
        self,
        config: Config,
        pannel_and_tips: ControlAndTips,
        alignment=ft.alignment.center,
        **kwargs,
    ):
        super().__init__(expand=True, alignment=alignment, **kwargs)
        self.value = 0
        self.pannel_and_tips = pannel_and_tips
        self.move_view = MoveView(config, self.pannel_and_tips)
        self.jump_view = TipsView("JumpView")
        self.sweet_scent_view = TipsView("SweetScentView")
        self.fish_view = TipsView("FishView")
        self.view_list = [
            self.move_view,
            self.jump_view,
            self.sweet_scent_view,
            self.fish_view,
        ]
        self.set_value(self.value)
        self.content = ft.Stack(controls=self.view_list)

    def set_value(self, value: int):
        # if self.value == value:
        #     return
        # print(value)
        assert value in [0, 1, 2, 3]
        self.value = value
        for i, view in enumerate(self.view_list):
            view.visible = i == self.value
        # self.content = self.view_list[value]
        # self.update()


class MoveView(ft.Column):
    def __init__(self, config: Config, pannel_and_tips: ControlAndTips, **kwargs):
        super().__init__(**kwargs)
        self.config = config
        self.pannel_and_tips = pannel_and_tips
        self.controls = [
            ft.Container(expand=True),
            BoolSettingItem(
                value=self.config.move.lr,
                true_icon=ft.icons.SWAP_HORIZ,
                false_icon=ft.icons.SWAP_VERT,
                title="Direction",
                on_click_buttom=lambda e: self.on_click_action_move(e, "lr"),
                pannel_and_tips=self.pannel_and_tips,
                tips=tips_dict["lr"],
            ),
            ft.Container(expand=1.5),
            BoolSettingItem(
                value=self.config.move.run,
                true_icon=ft.icons.DIRECTIONS_RUN_ROUNDED,
                title="Run",
                on_click_buttom=lambda e: self.on_click_action_move(e, "run"),
                pannel_and_tips=self.pannel_and_tips,
                tips=tips_dict["Run"],
            ),
            ft.Container(expand=1.5),
            BoolSettingItem(
                value=self.config.move.repel,
                true_icon=ft.icons.FIRE_HYDRANT,
                title="Repel",
                on_click_buttom=lambda e: self.on_click_action_move(e, "repel"),
                tips=tips_dict["Repel"],
                pannel_and_tips=self.pannel_and_tips,
            ),
            ft.Container(expand=True),
        ]
        self.alignment = ft.alignment.center
        # self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # self.spacing = 0

    def on_click_action_move(self, e: ft.TapEvent, attr_name: str):
        e.control.toggle()
        setattr(self.config.move, attr_name, e.control.value)
        self.config.save_config()


class TipsView(ft.Container):
    def __init__(
        self, view_name: Literal["JumpView", "FishView", "SweetScentView"], **kwargs
    ):
        super().__init__(expand=True, **kwargs)
        self.content = ft.Text(value=tips_dict[view_name], size=15)
        self.alignment = ft.alignment.center

    # def update_value(self, target_name):
    #     self.content.value = tips_dict[target_name]


tips_dict = {
    # "MoveView": "Move your role for encounters.",
    "JumpView": "使用越野自行车跳跃遇敌。\nRide Acro Bike and jump for emcounters.",
    "FishView": "使用各种钓竿钓鱼，注意提前在设置中配置游戏版本。\nUse various rods to fish. Configur the game version in the settings in advance.",
    "SweetScentView": "使用甜甜香气。甜甜香气应为你队伍末位宝可梦的第一项战斗外技能。\nUse sweet scent. The sweet scent should be the first out-battle skill of your last pokemon.",
    "Run": "一些地方是不允许骑车的。启用该配置来让你的角色跑步以加快遇敌速度。\nNo cycling some places. Enable this to control your character to run, speeding up encounters.",
    "Repel": "自动续喷雾。确保菜单指针位于背包，且进入背包后第一项为喷雾。\nAutomatic repel. Make sure the menu pointer points to BAG and the first item is repel.",
    "lr": "移动方向，左右或是上下。\nMovement direction, left and right or up and down.",
}
