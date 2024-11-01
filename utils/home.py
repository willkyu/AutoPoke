import flet
import inspect
import threading
import ctypes
import win32gui
from utils.my_ui import myHome
from utils.config_tool import Config
from utils.autopoke_core import AutoPokeCore


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
            if window_title.strip() == name:
                windows.append(hwnd)

        # 枚举所有子窗口
        win32gui.EnumChildWindows(parent_hwnd, callback, None)
        return windows

    hd = win32gui.GetDesktopWindow()
    count = 0
    for win in enum_child_windows(hd, name):
        if get_window_size(win) > 10:
            count += 1
            return win
    # assert False
    return False


class Home(myHome):
    """Home page of AutoPoke."""

    def __init__(self, page: flet.Page) -> None:
        super().__init__(page)
        self.read_config()
        self.findEO()
        self.refresh.on_click = self.findEO
        self.start_button.on_click = self.start
        self.mode_dropdown.on_change = self.mode_on_change
        self.version_dropdown.on_change = self.version_on_change
        self.direction.on_click = self.on_click_direction_button
        self.count_pannel.controls[1].on_change = self.count_on_change
        self.jump_block.controls[1].on_change = self.jump_on_change
        self.run_block.controls[1].on_change = self.run_on_change
        self.mode = "WILDPOKE"
        self.page.update()

    def read_config(self):
        self.print_to_pannel("Reading config from config.ini file...")
        self.cfg = Config(self.print_to_pannel)
        self.update_count(self.cfg.i)
        self.print_to_pannel("Done.")

    def update_count(self, count):
        self.count_pannel.controls[1].value = str(count)
        self.count_pannel.update()

    def count_on_change(self, e):
        self.cfg.update_config("DEFAULT", "count", e.control.value)

    def jump_on_change(self, e):
        self.cfg.update_config("WILDPOKE", "jump", str(e.control.value))

    def run_on_change(self, e):
        self.cfg.update_config("WILDPOKE", "run", str(e.control.value))

    def findEO(self, e=None):
        self.print_to_pannel("Searching for " + self.cfg.window_name + "......")
        # self.eo = win32gui.FindWindow(None, self.cfg.window_name)
        self.eo = get_eo(self.cfg.window_name)
        if self.eo:
            self.findeo = True
            self.print_to_pannel("Done.")
        else:
            self.findeo = False
            self.print_to_pannel(self.cfg.window_name + " not found.")

        # print(win32gui.GetWindowRect(self.eo))

    def start(self, e=None):
        self.cfg.read_ini()
        if not self.eo:
            self.print_to_pannel(self.cfg.window_name + " not found, please refresh.")
            return
        if not self.version_dropdown.value or not self.mode_dropdown.value:
            self.print_to_pannel("Please choose version or AutoPoke mode.")
            return

        self.lock()
        self.print_to_pannel("=== AutoPoke Start===")
        self.auto_poke_core = AutoPokeCore(
            self.eo, self.cfg, self.print_to_pannel, self.update_count
        )
        self.running = threading.Thread(
            target=self.auto_poke_core.exe_function,
            args=(self.cfg.mode.upper(),),
        )
        self.running.start()

        e.control.text = "Stop!"
        e.control.on_click = self.end
        e.control.update()

        self.running.join()
        self.print_to_pannel("Done.")
        self.unlock()

        e.control.text = "Start!"
        e.control.on_click = self.start
        self.page.update()

        pass

    def end(self, e=None):
        try:
            self.stop_thread(self.running)
            self.auto_poke_core.release_all_keys()
            self.cfg.write_count_config()
            self.print_to_pannel("Stopped.")
        except:
            self.print_to_pannel("Stopping failed.")

        e.control.text = "Start!"
        e.control.on_click = self.start
        e.control.update()
        pass

    def on_click_direction_button(self, e):
        if e.control.value == "lr":
            e.control.update_state("ud")
        elif e.control.value == "ud":
            e.control.update_state("lr")
        self.cfg.update_config(
            "WILDPOKE", "iflr", "True" if e.control.value == "lr" else "False"
        )

        e.control.update()

    def unlock(self):
        self.jump_block.controls[1].disabled = False
        self.jump_block.controls[1].tristate = False
        self.jump_block.controls[1].value = eval(self.cfg.config["WILDPOKE"]["jump"])
        self.run_block.controls[1].disabled = False
        self.run_block.controls[1].tristate = False
        self.run_block.controls[1].value = eval(self.cfg.config["WILDPOKE"]["run"])
        self.direction.disabled = False
        (
            self.direction.update_state("lr")
            if self.cfg.config["WILDPOKE"]["iflr"] == "True"
            else self.direction.update_state("ud")
        )
        self.count_pannel.controls[1].on_change = self.count_on_change
        self.count_pannel.controls[1].disabled = False
        self.version_dropdown.disabled = False
        self.mode_dropdown.disabled = False
        self.page.update()

    def lock(self):
        self.jump_block.controls[1].disabled = True
        self.jump_block.controls[1].tristate = True
        self.jump_block.controls[1].value = None
        self.run_block.controls[1].disabled = True
        self.run_block.controls[1].tristate = True
        self.run_block.controls[1].value = None
        self.direction.disabled = True
        self.count_pannel.controls[1].on_change = None
        self.count_pannel.controls[1].disabled = True
        self.version_dropdown.disabled = True
        self.mode_dropdown.disabled = True
        self.page.update()

    def mode_on_change(self, e=None):
        if e.control.value == "Wild Encounter":
            self.mode = "WILDPOKE"
            self.unlock()
        elif e.control.value == "Stationary":
            self.mode = "Stationary".upper()
            self.lock()
            self.direction.update_state("no")
            self.count_pannel.controls[1].on_change = self.count_on_change
            self.count_pannel.controls[1].disabled = False
            self.version_dropdown.disabled = False
            self.mode_dropdown.disabled = False
        elif e.control.value == "Fishing":
            self.mode = "Fishing".upper()
            self.lock()
            self.direction.update_state("no")
            self.count_pannel.controls[1].on_change = self.count_on_change
            self.count_pannel.controls[1].disabled = False
            self.version_dropdown.disabled = False
            self.mode_dropdown.disabled = False

        self.cfg.update_config("DEFAULT", "mode", self.mode)
        self.page.update()
        pass

    def version_on_change(self, e=None):
        self.cfg.update_config("DEFAULT", "version", e.control.value)

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
