from multiprocessing.connection import wait
from time import sleep
from .pressTool import *
from .colorTool import *
from .mailTools import sendMail
from random import choice
from atexit import register,unregister
from .iniTool import *



class posConfig:
	def	__init__(self,eo,inCave) -> None:
		getColor(eo,1,1)
		self.w,self.h=getSize()

		self.colorPos=[self.percentXPos(955),self.percentYPos(400)]
		self.colorPos0=[self.percentXPos(555), self.percentYPos(360)] if inCave else self.colorPos
		self.colorPos1=[self.percentXPos(945),self.percentYPos(660)]

	def percentXPos(self,x:int):
		return int(x*self.w/1116)
	
	def percentYPos(self,y:int):
		return int(y*self.h/714)

# (255, 251, 247)白色
white=[(254+i, 250+j, 246+k) for i in range(2) for j in range(3) for k in range(3)]
# (0, 0, 0) 黑色
black=[(0+i, 0+j, 0+k) for i in range(3) for j in range(3) for k in range(3)]
# (107, 162, 165)BG深绿
BGdeepGreen=[(106+i, 161+j, 165+k) for i in range(3) for j in range(3) for k in range(3)]
# (255, 251, 222)BG浅黄
BGYellow=[(254+i, 250+j, 221+k) for i in range(2) for j in range(3) for k in range(3)]
	


def RandomHitKey(eo,keyList):
    HitKey(eo,choice(keyList))

def exit_print_i(i,cfg:Config):
	print('no shiny pokemon in {} times.'.format(i))
	cfg.writeConfig(i)

def RUN(eo,cfg:Config):
	HitKey(eo,cfg.keymap['RIGHT'])
	HitKey(eo,cfg.keymap['DOWN'])
	HitKey(eo,cfg.keymap['A'])
	sleep(0.5)
	HitKey(eo,cfg.keymap['A'])
	sleep(2.7)

def wildPoke(eo,cfg:Config,jump=False,inCave=False,ifLR=True,i=0):
	'''
	Input:
		eo: the window of operator
		jump: if use bicycle to jump
		inCave: if player is in cave
		ifLR: move left and right or up and down, needed only jump is false
		i: start count from i 
	'''
	pos=posConfig(eo,inCave)
	# print(pos.colorPos0)
	if i==0:
		SLs=cfg.i
	else:
		SLs=i
	# 默认左右走，ifLR=False时，上下走
	register(exit_print_i,i=SLs,cfg=cfg)
	keyList = [cfg.keymap['LEFT'],cfg.keymap['RIGHT']] if ifLR else [cfg.keymap['UP'],cfg.keymap['DOWN']]

	# 如果在洞穴就检测中间部分
	# [555, 375]  [590,475]
	# pos.colorPos0 if inCave else pos.colorPos
	while 1:
        # move till encounter
		if jump:
			PressKey(eo,cfg.keymap['B'])
		while 1:
			if not jump:
				RandomHitKey(eo,keyList)
			colorGot=getColor(eo,*(pos.colorPos0))
			if colorGot in black:
				if jump:
					ReleaseKey(eo,cfg.keymap['B'])
				SLs+=1
				unregister(exit_print_i)
				register(exit_print_i,i=SLs,cfg=cfg)
				break
		
		sleep(4)
		HitKey(eo,cfg.keymap['A'])
		# if in safari zone, its much more faster than others.
		sleep(0.1)
		colorGot=getColor(eo,*pos.colorPos)
		if colorGot in BGYellow:
			# print('Zone')
			RUN(eo,cfg)
			continue

		sleep(2.9)
		colorGot=getColor(eo,*pos.colorPos)
		# print(colorGot)
		if colorGot not in BGYellow:
			print('Got Shiny Pokemon!')
			sendMail(i=SLs)
			cfg.writeConfig(0)
			unregister(exit_print_i)
			break
		colorGot=getColor(eo,*pos.colorPos1)
		if colorGot in BGdeepGreen:
			# 威吓检测
			# print('威吓!')
			# sleep(3.6)
			while 1:
				colorGot=getColor(eo,*pos.colorPos1)
				if colorGot not in BGdeepGreen:
					break
		RUN(eo,cfg)

def stationary(eo,cfg:Config,ifFRLG=False,hitkeys=[],i=0):
	# 还没测试
	pos=posConfig(eo,inCave=False)
	SLs = i
	while 1:
		for key in hitkeys:
			HitKey(key)
		# hit 'A' till encounter
		while 1:
			HitKey(cfg.keymap['A'])
			colorGot=getColor(eo,*pos.colorPos)
			if colorGot==(0, 0, 0):
				SLs+=1
				break
		sleep(4)
		HitKey(eo,cfg.keymap['A'])
		sleep(3)
		colorGot=getColor(eo,*pos.colorPos)
		if colorGot!=(255, 251, 222):
			print('Got Shiny Pokemon!')
			sendMail(i=SLs)
			break
		SL(eo,cfg)
		sleep(2)
		HitKey(cfg.keymap['A'])
		HitKey(cfg.keymap['A'])
		sleep(0.5)
		HitKey(cfg.keymap['A'])
		sleep(0.5)
		if ifFRLG:
			# skip memory recall 跳过回忆
			HitKey(cfg.keymap['B'])
			sleep(0.5)
	pass

def fishing(eo,ifFRLG=False):

		pass

def SL(eo,cfg:Config):
    """
        eo SL once
    """
    PressKey(eo,cfg.keymap['A'])
    PressKey(eo,cfg.keymap['B'])
    PressKey(eo,cfg.keymap['ENTER'])
    PressKey(eo,cfg.keymap['BACKSPACE'])
    sleep(0.3)
    ReleaseKey(eo,cfg.keymap['A'])
    ReleaseKey(eo,cfg.keymap['B'])
    ReleaseKey(eo,cfg.keymap['ENTER'])
    ReleaseKey(eo,cfg.keymap['BACKSPACE'])

