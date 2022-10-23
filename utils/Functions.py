from multiprocessing.connection import wait
from time import sleep
from .pressTool import *
from .colorTool import *
from .mailTools import sendMail
from random import choice

colorPos=[955,400]
colorPos1=[945,660]
# (255, 251, 247)白色
# (0, 0, 0) 黑色
# (107, 162, 165)BG深绿
# (255, 251, 222)BG浅黄


def RandomHitKey(eo,keyList):
    HitKey(eo,choice(keyList))

def RUN(eo):
	HitKey(eo,'RIGHT')
	HitKey(eo,'DOWN')
	HitKey(eo,'X')
	sleep(0.5)
	HitKey(eo,'X')
	sleep(2.7)

def wildPoke(eo,jump=False,inCave=False,ifLR=True,i=0):
	'''
	Input:
		eo: the window of operator
		jump: if use bicycle to jump
		inCave: if player is in cave
		ifLR: move left and right or up and down, needed only jump is false
		i: start count from i 
	'''
	# 默认左右走，ifLR=False时，上下走
	SLs=i
	keyList = ['LEFT','RIGHT'] if ifLR else ['UP','DOWN']

	# 如果在洞穴就检测中间部分
	colorPos0=[590,475] if inCave else colorPos
	while 1:
        # move till encounter
		if jump:
			PressKey(eo,'Z')
		while 1:
			if not jump:
				RandomHitKey(eo,keyList)
			colorGot=getColor(eo,*colorPos0)
			if colorGot==(0, 0, 0):
				if jump:
					ReleaseKey(eo,'Z')
				SLs+=1
				break
		
		sleep(4)
		HitKey(eo,'X')
		sleep(3)
		colorGot=getColor(eo,*colorPos)
		if colorGot!=(255, 251, 222):
			print('Got Shiny Pokemon!')
			sendMail(i=SLs)
			break
		elif getColor(eo,*colorPos1)==(107, 162, 165):
			# 威吓检测
			# print('威吓!')
			sleep(3.5)

		RUN(eo)

def stationary(eo,ifFRLG=False,hitkeys=[],i=0):
	# 还没测试
	SLs = i
	while 1:
		for key in hitkeys:
			HitKey(key)
		# hit 'A' till encounter
		while 1:
			HitKey('X')
			colorGot=getColor(eo,*colorPos)
			if colorGot==(0, 0, 0):
				SLs+=1
				break
		sleep(4)
		HitKey(eo,'X')
		sleep(3)
		colorGot=getColor(eo,*colorPos)
		if colorGot!=(255, 251, 222):
			print('Got Shiny Pokemon!')
			sendMail(i=SLs)
			break
		SL(eo)
		sleep(2)
		HitKey('X')
		HitKey('X')
		sleep(0.5)
		HitKey('X')
		sleep(0.5)
		if ifFRLG:
			# skip memory recall 跳过回忆
			HitKey('Z')
			sleep(0.5)
	pass
