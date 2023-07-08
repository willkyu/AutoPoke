import win32gui
from utils.pressTool import *
from utils.colorTool import *
from utils.Functions import *
from utils.iniTool import *

def get_all_hwnd(hwnd, mouse):
	hwnd_title = dict()
	if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
		hwnd_title.update({hwnd: win32gui.GetWindowText(hwnd)})
	return hwnd_title

def get_all_window(hwnd_title):
    
    win32gui.EnumWindows(get_all_hwnd, 0)
    for h, t in hwnd_title.items():
	    if t != "":
		    print(h, t)

eo=win32gui.FindWindow(None,'Operator × v0.9.0-beta')

cfg=Config()
cfg.readConfig()
# get_all_window()


# t=getColor(eo,955,400)
# print(t)
# sendMail()


#=================================
# How to use?
# Make player role where you need to encounter PM, and set parameters below. Then run this file.
# if not found Operator: run function 'get_all_window()' and copy your Operator's name to eo=win32gui.FindWindow(None,'Operator × v0.9.1-beta').
#=================================
# jump:bool=False. if you want to encounter PM by riding Acro Bike and jumping, set 'jump' True.
# inCave:bool=False. if you are in Cave where is dark around, set it True.
# ifLR:bool=True. if you want to move left and right, set it True. Up and down, set it False.
# i:int=0. Start counting from i.
#=================================
wildPoke(eo, cfg, jump = False, inCave = True, ifLR = True)
