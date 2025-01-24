import flet as ft
from typing import Literal
from random import choice
import inspect
import threading
import ctypes

from core.config import Config
from core.autopoke_core import AutoPokeCoreFactory


class Panel(ft.Column):
    def __init__(
        self,
        config: Config,
        auto_poke_ui: object,
        mode: Literal[0, 1],
        func: str = "Move",
        alignment=ft.alignment.center,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
        **kwargs,
    ):
        super().__init__(
            alignment=alignment,
            horizontal_alignment=horizontal_alignment,
            expand=expand,
            **kwargs,
        )
        self.auto_poke_ui = auto_poke_ui
        self.mode = mode
        self.func = func
        self.extra_value = ""
        self.config = config
        # self.screen = ft.Container(
        #     width=200,
        #     height=200,
        #     border_radius=10,
        #     expand=1,
        # )
        self.count_view = CountView(config, mode)
        self.start_button = ft.TextButton(
            text="Start",
            width=140,
            height=50,
            on_click=self.start,
            style=ft.ButtonStyle(bgcolor=ft.colors.with_opacity(0.1, "white")),
            disabled=len(self.auto_poke_ui.eo) == 0,
            tooltip=(
                f"No {self.config.general.window_name} found. Click mimikyu for refreshing."
                if len(self.auto_poke_ui.eo) == 0
                else None
            ),
        )
        self.controls = [
            ft.Container(expand=True),
            self.count_view,
            ft.Container(expand=True),
            self.start_button,
            ft.Container(expand=True),
        ]

    def start_buttom_refresh(self):
        self.start_button.tooltip = (
            f"No {self.config.general.window_name} found. Click mimikyu for refreshing."
            if len(self.auto_poke_ui.eo) == 0
            else None
        )
        self.start_button.disabled = len(self.auto_poke_ui.eo) == 0

    def start(self, e):
        self.auto_poke_ui.enable_lock()
        self.start_button.on_click = self.stop
        self.start_button.text = "Stop"
        self.start_button.update()

        self.auto_poke_core_list = [
            AutoPokeCoreFactory(
                eo,
                self.config,
                self.auto_poke_ui.printf,
                self.count_view.update_count,
            ).get_autopoke_core(self.mode, self.func, self.extra_value)
            for eo in self.auto_poke_ui.eo
        ]
        self.running_list = [
            threading.Thread(
                target=auto_poke_core.exe_function,
                # args=(
                #     self.mode,
                #     self.func,
                # ),
            )
            for auto_poke_core in self.auto_poke_core_list
        ]
        for running in self.running_list:
            running.start()

        for running in self.running_list:
            running.join()
        self.auto_poke_ui.enable_lock(False)
        self.auto_poke_ui.set_logger_visible()
        self.start_button.on_click = self.start
        self.start_button.text = "Start"
        self.start_button.update()

    def stop(self, e=None):
        self.auto_poke_ui.enable_lock(False)
        self.start_button.on_click = self.start
        self.start_button.text = "Start"
        self.start_button.update()

        try:
            for running in self.running_list:
                self.stop_thread(running)
            for auto_poke_core in self.auto_poke_core_list:
                auto_poke_core.release_all_keys()
            self.config.save_config()
            self.auto_poke_ui.printf("Stopped.")
        except Exception as exception:
            self.auto_poke_ui.printf(str(exception))

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            """if it returns a number greater than one, you're in trouble,
            and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

    # def set_mode(self, mode: int):
    #     if mode == self.mode or mode not in [0, 1]:
    #         return
    #     self.mode = mode


class CountView(ft.Container):
    def __init__(
        self,
        config: Config,
        # auto_poke_ui: object,
        mode: Literal[0, 1],
        **kwargs,
    ):
        super().__init__(
            alignment=ft.alignment.center,
            **kwargs,
        )
        self.config = config
        # self.auto_poke_ui = auto_poke_ui
        self.mode = mode
        self.count = ft.TextField(
            value=str(self.config.general.count[self.mode]),
            text_style=ft.TextStyle(size=20),
            width=80,
            text_align=ft.TextAlign.CENTER,
            on_change=self.count_on_change,
            disabled=False,
            border="none",
        )
        self.progress_ring = RepeatProgressRing(
            value8192=self.config.general.count[self.mode],
            width=140,
            height=140,
            stroke_width=25,
        )
        self.content = ft.Stack(
            [
                self.progress_ring,
                ft.Stack(
                    controls=[
                        ft.Container(
                            content=ft.Text(value="/8192", size=10, height=15),
                            # alignment=ft.alignment.bottom_center,
                        ),
                        self.count,
                    ],
                    alignment=ft.alignment.bottom_right,
                ),
                # self.count,
            ],
            alignment=ft.alignment.center,
        )

    def update_count(self, count: int):
        self.config.general.count[self.mode] = count
        self.config.save_config()
        self.count.value = count
        self.progress_ring.update_value(count)
        self.update()

        # import time

        # # self.count_on_change(str(int(self.count.value) + 100))
        # # self.progress_ring.update_value(self.config.general.count)
        # # self.update()
        # for i in range(0, 8192 * 5, 500):
        #     self.update_count(i)
        #     time.sleep(0.05)

    def count_on_change(self, e: ft.ControlEvent):
        try:
            self.config.general.count[self.mode] = int(e.control.value)
        except Exception as e:
            self.config.general.count[self.mode] = 0
            self.config.save_config()
            self.count.value = "0"
        self.config.save_config()
        self.progress_ring.update_value(self.config.general.count[self.mode])
        self.update()


class RepeatProgressRing(ft.ProgressRing):
    def __init__(
        self,
        value8192: int = 0,
        stroke_cap: ft.StrokeCap = ft.StrokeCap.ROUND,
        **kwargs,
    ):
        super().__init__(stroke_cap=stroke_cap, **kwargs)
        self.color_set = {
            "green",
            "blue",
            "yellow",
            "red",
            "cyan",
            "purple",
            "orange",
        }
        # self.bgcolor_list=["opacity"]+self.color_list
        if value8192 <= 8192:
            self.color = "green"
            self.bgcolor = ft.colors.with_opacity(0.05, "white")
        else:
            self.color = choice(list(self.color_set))
            self.bgcolor = (
                "green"
                if value8192 < 8192 * 2
                else choice(list(self.color_set - {self.color}))
            )
        self.value8192 = value8192
        self.value = value8192 % 8192 / 8192

    def update_value(self, value8192: int):
        if value8192 <= 8192:
            self.color = "green"
            self.bgcolor = ft.colors.with_opacity(0.05, "white")
        if value8192 // 8192 > self.value8192 // 8192:
            self.bgcolor = self.color
            self.color = choice(list(self.color_set - {self.color}))
            print(f"color: {self.color}")
            print(f"bgcolor: {self.bgcolor}")
        self.value8192 = value8192
        self.value = self.value8192 % 8192 / 8192
        self.update()
