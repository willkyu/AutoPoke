import flet
import win32gui
import inspect
import threading
import ctypes
from utils.myUI import myHome
from utils.iniTool import Config
from utils.Functions import *

class Home(myHome):
    """Home page of AutoPoke.
    """

    def __init__(self, page: flet.Page) -> None:
        super().__init__(page)
        self.readConfig()
        self.findEO()
        self.refresh.on_click=self.findEO
        self.start_button.on_click=self.start
        self.mode_dropdown.on_change=self.mode_on_change
        self.version_dropdown.on_change=self.version_on_change
        self.direction.on_click=self.on_click_direction_button
        self.count_pannel.controls[1].on_change=self.count_on_change
        self.jump_block.controls[1].on_change=self.jump_on_change
        self.run_block.controls[1].on_change=self.run_on_change
        self.mode="WILDPOKE"
        self.page.update()
        
    
    def readConfig(self):
        self.print_to_pannel("Reading config from config.ini file...")
        self.cfg = Config(self.print_to_pannel)
        self.update_count(self.cfg.i)
        self.print_to_pannel("Done.")

    def update_count(self,count):
        self.count_pannel.controls[1].value=str(count)
        self.count_pannel.update()
        # self.cfg.updateConfig("DEFAULT","i",str(count))
    
    def count_on_change(self,e):
        self.cfg.updateConfig("DEFAULT","count",e.control.value)

    def jump_on_change(self,e):
        self.cfg.updateConfig("WILDPOKE","jump",str(e.control.value))

    def run_on_change(self,e):
        self.cfg.updateConfig("WILDPOKE","run",str(e.control.value))

    def findEO(self,e=None):
        # self.findeo=False
        self.print_to_pannel("Searching for "+self.cfg.window_name+"......")
        self.eo=win32gui.FindWindow(None, self.cfg.window_name)
        if self.eo:
            self.findeo=True
            self.print_to_pannel("Done.")
        else:
            self.findeo=False
            self.print_to_pannel(self.cfg.window_name+" not found.")

    def start(self,e=None):
        self.cfg.readini()
        if not self.eo:
            self.print_to_pannel(self.cfg.window_name+" not found, please refresh.")
            return
        if not self.version_dropdown.value or not self.mode_dropdown.value:
            self.print_to_pannel("Please choose version or AutoPoke mode.")
            return
        
        self.lock()
        self.print_to_pannel("=== AutoPoke Start===")
        self.count_pannel.controls[1].on_change=None
        self.count_pannel.controls[1].disabled=True
        self.running=threading.Thread(target=eval(self.cfg.mode.upper()), args=(self.eo, self.cfg, self.print_to_pannel, self.update_count))
        self.running.start()

        e.control.text="Stop!"
        e.control.on_click=self.end
        e.control.update()
        # self.start_button.text="Stop!"
        # self.start_button.update()
        # self.start_button.on_click=self.end

        self.running.join()
        release_all_keys(self.eo,self.cfg)
        self.print_to_pannel("Done.")
        self.unlock()
        self.count_pannel.controls[1].on_change=self.count_on_change
        self.count_pannel.controls[1].disabled=False
        e.control.text="Start!"
        e.control.on_click=self.start

        pass

    def end(self,e=None):
        try:
            self.stop_thread(self.running)
            release_all_keys(self.eo,self.cfg)
            self.cfg.writeCountConfig()
            self.print_to_pannel("Stopped.")
        except:
            self.print_to_pannel("Stopping failed.")

        e.control.text="Start!"
        e.control.on_click=self.start
        e.control.update()
        pass

    def on_click_direction_button(self, e):
        # print("111")
        if e.control.value=='lr':
            e.control.update_state('ud')
        elif e.control.value=='ud':
            e.control.update_state('lr')
        self.cfg.updateConfig("WILDPOKE","iflr","True" if e.control.value=='lr' else "False")  
        
        e.control.update()
        # return super().on_click

    def unlock(self):
        self.jump_block.controls[1].disabled=False
        self.jump_block.controls[1].tristate=False
        self.jump_block.controls[1].value=eval(self.cfg.config['WILDPOKE']['jump'])
        self.run_block.controls[1].disabled=False
        self.run_block.controls[1].tristate=False
        self.run_block.controls[1].value=eval(self.cfg.config['WILDPOKE']['run'])
        self.direction.disabled=False
        self.direction.update_state('lr') if self.cfg.config['WILDPOKE']['iflr'] else self.direction.update_state('ud')
        self.page.update()

    def lock(self):
        self.jump_block.controls[1].disabled=True
        self.jump_block.controls[1].tristate=True
        self.jump_block.controls[1].value=None
        self.run_block.controls[1].disabled=True
        self.run_block.controls[1].tristate=True
        self.run_block.controls[1].value=None
        self.direction.disabled=True
        self.page.update()

    def mode_on_change(self,e=None):
        # print("111")
        # print(e.control.value)
        if e.control.value=='Wild Encounter':
            self.mode="WILDPOKE"
            self.unlock()
        elif e.control.value=='Stationary':
            self.mode='Stationary'.upper()
            self.lock()
            
        self.cfg.updateConfig("DEFAULT","mode",self.mode)
        self.page.update()
        pass

    def version_on_change(self,e=None):
        self.cfg.updateConfig("DEFAULT","version",e.control.value)

    def _async_raise(self, tid, exctype):
        """raises the exception, performs cleanup if needed"""
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    def stop_thread(self, thread):
        self._async_raise(thread.ident, SystemExit)

