import win32gui
from utils.pressTool import *
from utils.colorTool import *
from utils.Functions import *
from utils.mailTools import sendMail

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

# get_all_window()


# t=getColor(eo,955,400)
# print(t)
# sendMail()

wildPoke(eo,jump=False,inCave=True,ifLR=True)