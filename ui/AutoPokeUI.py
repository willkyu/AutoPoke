import flet as ft
import win32gui
import sys
import os

from core.config import Config, VERSION
from ui.WildPmUI import WildPmUI
from ui.StationaryUI import StationaryUI
from ui.SettingsUI import SettingsUI


# from utils.my_ui import VERSION
def get_resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_eo(name):
    def get_window_size(hwnd):
        # 获取窗口矩形 (left, top, right, bottom)
        rect = win32gui.GetWindowRect(hwnd)
        width = rect[2] - rect[0]
        height = rect[3] - rect[1]
        return width + height

    def enum_child_windows(parent_hwnd, name):
        windows = []

        def callback(hwnd, extra):
            # 获取窗口标题
            window_title = win32gui.GetWindowText(hwnd)
            # if window_title.strip() == name:
            if name in window_title:
                windows.append(hwnd)

        # 枚举所有子窗口
        win32gui.EnumChildWindows(parent_hwnd, callback, None)
        return windows

    hd = win32gui.GetDesktopWindow()
    win_list = []
    for win in enum_child_windows(hd, name):
        if get_window_size(win) > 100:
            win_list.append(win)
        # print(get_window_size(win))
    return win_list


class AutoPokeUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.config = Config()
        self.page.window.icon = get_resource_path("src/icon.ico")
        self.page.window.prevent_close = True
        self.page.window.on_event = self.close_app

        self.sidebar = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            leading=ft.Container(
                image_src=get_resource_path("src/icon-grey.png"),
                width=100,
                height=100,
                shape=ft.BoxShape.CIRCLE,
                expand=1,
                tooltip=f"未发现{self.config.general.window_name}，点击以刷新。\nNo {self.config.general.window_name} found. Click for refreshing.",
                on_click=lambda e: self.search_windows(e, True),
            ),
            trailing=ft.Text(
                "© willkyu",
                size=15,
                text_align=ft.TextAlign.CENTER,
                color=ft.colors.GREY_700,
            ),
            # group_alignment=-0.9,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.GRASS_ROUNDED,
                    selected_icon=ft.icons.GRASS,
                    label="Wild PM",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.CATCHING_POKEMON_ROUNDED,
                    selected_icon=ft.icons.CATCHING_POKEMON,
                    label="Stationary",
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS_ROUNDED,
                    selected_icon=ft.Icon(ft.icons.SETTINGS),
                    label_content=ft.Text("Settings"),
                ),
            ],
            on_change=lambda e: self.set_value(e.control.selected_index),
        )

        self.search_windows()

        self.navigation_view = NavigationView(self.config, self)

        self.output_view = ft.Column(
            [
                ft.Container(height=100),
                ft.Container(
                    OutputView(maxlen=50, width=270),
                    bgcolor=ft.colors.BACKGROUND,
                    border=ft.border.all(2, ft.colors.BLUE_GREY_500),
                    expand=True,
                ),
            ],
            visible=False,
        )
        self.output_logger_buttom = ft.IconButton(
            icon_size=20,
            icon=ft.icons.ASSIGNMENT_OUTLINED,
            on_click=self.set_logger_visible,
        )
        self.page.overlay.append(self.output_view)
        self.page.overlay.append(self.output_logger_buttom)

        self.page.add(
            ft.Row(
                controls=[
                    self.sidebar,
                    ft.VerticalDivider(width=1),
                    self.navigation_view,
                ],
                expand=True,
            )
        )

    def set_logger_visible(self, e=None):
        self.output_view.visible = not self.output_view.visible
        self.page.update()

    def search_windows(self, e: ft.Control = None, trigger: bool = False):
        self.eo = get_eo(self.config.general.window_name)
        self.find_eo = len(self.eo) > 0
        if self.find_eo:
            self.sidebar.leading.image_src = get_resource_path("src/icon.png")
            self.sidebar.leading.tooltip = (
                f"发现{len(self.eo)}个窗口。\nFind {len(self.eo)} window(s)."
            )
        else:
            self.sidebar.leading.image_src = get_resource_path("src/icon-grey.png")
            self.sidebar.leading.tooltip = f"未发现{self.config.general.window_name}，点击以刷新。\nNo {self.config.general.window_name} found. Click for refreshing."
        if trigger:
            self.navigation_view.wild_pm_ui.pannel.start_buttom_refresh()
            self.navigation_view.stationary_ui.pannel.start_buttom_refresh()
        self.page.update()

    def set_value(self, value: int):
        # if self.navigation_view.value == value:
        #     return
        # print(value)
        assert value in [0, 1, 2]
        self.navigation_view.set_value(value)
        # self.all_ui.set_show_extra(show_extra=False if value == 2 else True)
        self.page.update()

    def enable_lock(self, lock: bool = True):
        self.output_view.visible = lock
        self.sidebar.disabled = lock
        self.navigation_view.enable_lock(lock)
        self.page.update()

    def printf(self, text: str):
        self.output_view.controls[-1].content.append(
            ft.Text(value=text, weight=ft.FontWeight.BOLD)
        )

    def close_app(self, e):
        if e.data == "close":
            self.navigation_view.wild_pm_ui.pannel.stop()
            self.navigation_view.stationary_ui.pannel.stop()
            self.page.window.destroy()


# class AllUI(ft.Row):
#     def __init__(
#         self,
#         extra_controls: list[ft.Control],
#         org_controls: list[ft.Control],
#         show_extra: bool = True,
#         **kwargs,
#     ):
#         super().__init__(**kwargs)
#         self.org_controls = org_controls
#         self.extra_controls = extra_controls
#         self.set_show_extra(show_extra)

#     def set_show_extra(self, show_extra: bool):
#         self.show_extra = show_extra
#         self.controls = (
#             self.org_controls + self.extra_controls
#             if self.show_extra
#             else self.org_controls
#         )
#         # self.update()


class NavigationView(ft.Container):
    def __init__(self, config: Config, eo: list, expand=True, **kwargs):
        super(NavigationView, self).__init__(expand=expand, **kwargs)
        self.value = 0
        self.wild_pm_ui = WildPmUI(config, eo)
        self.stationary_ui = StationaryUI(config, eo)
        self.settings_ui = SettingsUI(config)
        self.view_list = [
            self.wild_pm_ui,
            self.stationary_ui,
            self.settings_ui,
        ]
        self.set_value(self.value)
        self.content = ft.Stack(controls=self.view_list)

    def set_value(self, value: int):
        # if self.value == value:
        #     return
        # print(value)
        assert value in [0, 1, 2]
        self.value = value
        for i, view in enumerate(self.view_list):
            view.visible = i == self.value
        # self.content = self.view_list[value]
        # self.update()

    def enable_lock(self, lock: bool):
        self.wild_pm_ui.navigation_bar.disabled = lock
        self.wild_pm_ui.wild_pm_navigation_view.disabled = lock
        self.wild_pm_ui.pannel.count_view.count.disabled = lock

        self.stationary_ui.target_dropdown.disabled = lock
        self.stationary_ui.pannel.count_view.count.disabled = lock


class OutputView(ft.ListView):
    """panel"""

    def __init__(self, maxlen=100, auto_scroll=True, **kwargs):
        super().__init__(auto_scroll=auto_scroll, **kwargs)

        self.maxlen = maxlen
        self.controls.append(
            ft.Text(value=f"==== AutoPoke {VERSION} ====", weight=ft.FontWeight.BOLD)
        )
        self.controls.append(
            ft.Text(
                value="Text Speed of Game MUST be Fast AND NO Window Minimizing of Playback.",
                weight=ft.FontWeight.BOLD,
            )
        )

    def append(self, text: ft.Text):
        self.controls.append(text)
        if len(self.controls) > 50:
            self.controls = self.controls[-50:]
        self.update()
