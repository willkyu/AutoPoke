from multiprocessing.connection import wait
from time import sleep
from utils.pressTool import *
from utils.colorTool import *
from utils.mailTools import sendMail
from random import choice
from atexit import register, unregister
from utils.iniTool import *


class posConfig:
    def __init__(self, eo) -> None:
        getColor(eo, 1, 1)
        self.w, self.h = getSize()

        # self.colorPos = [self.percentXPos(955), self.percentYPos(400)]
        self.colorPos = [943, 430]  # BGYellow
        # self.colorPos0 = [self.percentXPos(555), self.percentYPos(
        #     360)] if inCave else self.colorPos
        self.colorPos0 = [510, 350]
        # self.colorPos1 = [self.percentXPos(945), self.percentYPos(660)]
        self.colorPos1 = [900, 620]

    # def percentXPos(self, x: int):
    #     return int(x*self.w/1116)

    # def percentYPos(self, y: int):
    #     return int(y*self.h/714)


# (255, 251, 247)白色
white = [(254+i, 250+j, 246+k) for i in range(2)
         for j in range(3) for k in range(3)]
# (255, 251, 255)(77, 76, 77)Dialogue
dialogueColor = [(254+i, 250+j, 254+k) for i in range(3) for j in range(3) for k in range(3)] + \
    [(76+i, 75+j, 76+k) for i in range(3)
     for j in range(3) for k in range(3)]
# (0, 0, 0) 黑色
black = [(0+i, 0+j, 0+k) for i in range(3) for j in range(3) for k in range(3)]
# (107, 162, 165)BG深绿 宝石
BGdeepGreen = [(106+i, 161+j, 165+k) for i in range(3)
               for j in range(3) for k in range(3)]
# (41, 81, 107)BG深蓝 火叶
BGdeepBlue = [(41+i, 81+j, 107+k) for i in range(3)
              for j in range(3) for k in range(3)]
# (255, 251, 222)BG浅黄
BGYellow = [(254+i, 250+j, 221+k) for i in range(2)
            for j in range(3) for k in range(3)]


def RandomHitKey(eo, keyList):
    HitKey(eo, choice(keyList))


def exit_print_i(i, cfg: Config):
    print('no shiny pokemon in {} times.'.format(i))
    cfg.writeCountConfig(i)
    sleep(5)


def RUN(eo, cfg: Config):
    HitKey(eo, cfg.keymap['RIGHT'])
    HitKey(eo, cfg.keymap['DOWN'])
    HitKey(eo, cfg.keymap['A'])
    sleep(0.5)
    HitKey(eo, cfg.keymap['A'])
    sleep(2.7)


def sendMail_(cfg: Config, i):
    sendMail(i, cfg.toMail, cfg.mail_host, cfg.sendMail, cfg.sendMail_password)


def WILDPOKE(eo, cfg: Config):

    #inCave = eval(cfg.mode_config['incave'])
    jump = eval(cfg.mode_config['jump'])
    ifLR = eval(cfg.mode_config['iflr'])
    SLs = cfg.i
    pos = posConfig(eo)

    # 默认左右走，ifLR=False时，上下走
    register(exit_print_i, i=SLs, cfg=cfg)
    keyList = [cfg.keymap['LEFT'], cfg.keymap['RIGHT']] if ifLR else [
        cfg.keymap['UP'], cfg.keymap['DOWN']]

    # 如果在洞穴就检测中间部分
    # [555, 375]  [590,475]
    # pos.colorPos0 if inCave else pos.colorPos
    while 1:
        # move till encounter
        if jump:
            PressKey(eo, cfg.keymap['B'])
        while 1:
            if not jump:
                RandomHitKey(eo, keyList)
                # HitKey(eo,cfg.keymap['B'])
            colorGot = getColor(eo, *pos.colorPos0)
            if colorGot in black:
                if jump:
                    ReleaseKey(eo, cfg.keymap['B'])
                while colorGot in black:
                    colorGot = getColor(eo, *pos.colorPos0)

                SLs += 1
                unregister(exit_print_i)
                register(exit_print_i, i=SLs, cfg=cfg)
                break
            elif cfg.version == 'E':
                colorGot = getColor(eo, *pos.colorPos1)
                if colorGot in dialogueColor:
                    while colorGot in dialogueColor:
                        HitKey(eo, cfg.keymap['B'])
                        colorGot = getColor(eo, *pos.colorPos1)

        sleep(3.0)
        HitKey(eo, cfg.keymap['A'])
        # if in safari zone, its much more faster than others.
        sleep(0.12)
        colorGot = getColor(eo, *pos.colorPos)
        if colorGot in BGYellow:
            # print('Zone')
            RUN(eo, cfg)
            continue

        sleep(2.88)
        colorGot = getColor(eo, *pos.colorPos)
        # print(colorGot)
        if colorGot not in BGYellow:
            print('Got Shiny Pokemon!')
            sendMail_(cfg, i=SLs)
            cfg.writeCountConfig(0)
            unregister(exit_print_i)
            break
        colorGot = getColor(eo, *pos.colorPos1)
        if colorGot in BGdeepGreen + BGdeepBlue:
            # 额外动画检测
            # print('威吓!')
            # sleep(3.6)
            while 1:
                colorGot = getColor(eo, *pos.colorPos1)
                if colorGot not in BGdeepGreen:
                    sleep(0.02)
                    break
        RUN(eo, cfg)


def STATIONARY(eo, cfg: Config, ifFRLG=False, hitkeys=[], i=0):

    ifFRLG = cfg.version in ['Fr', 'Lg']

    SLs = eval(cfg.i)
    register(exit_print_i, i=SLs, cfg=cfg)
    pos = posConfig(eo, False)
    delay_list = [a/100 for a in range(0, 60, 2)]
    # SLs = i
    while 1:
        sleep(choice(delay_list))
        for key in hitkeys:
            HitKey(key)
        # hit 'A' till encounter
        while 1:
            HitKey(eo, cfg.keymap['A'])
            colorGot = getColor(eo, *pos.colorPos)
            if colorGot in black:
                SLs += 1
                unregister(exit_print_i)
                register(exit_print_i, i=SLs, cfg=cfg)
                break
        sleep(4)
        HitKey(eo, cfg.keymap['A'])
        sleep(3)
        colorGot = getColor(eo, *pos.colorPos)
        if colorGot not in BGYellow:
            print('Got Shiny Pokemon!')
            sendMail_(cfg, i=SLs)
            cfg.writeCountConfig(0)
            unregister(exit_print_i)
            break
        SL(eo, cfg)
        sleep(2)
        HitKey(eo, cfg.keymap['A'])
        HitKey(eo, cfg.keymap['A'])
        sleep(0.5)
        HitKey(eo, cfg.keymap['A'])
        sleep(0.5)
        if ifFRLG:
            # skip memory recall 跳过回忆
            HitKey(eo, cfg.keymap['B'])
            sleep(0.5)

        # hit 'A' till entering
        while 1:
            HitKey(eo, cfg.keymap['A'])
            colorGot = getColor(eo, *pos.colorPos)
            if colorGot in black:
                break

        while 1:
            HitKey(eo, cfg.keymap['A'])
            colorGot = getColor(eo, *pos.colorPos)
            if colorGot in black:
                break
    pass


def fishing(eo, ifFRLG=False):

    pass


def SL(eo, cfg: Config):
    """
        eo SL once
    """
    PressKey(eo, cfg.keymap['A'])
    PressKey(eo, cfg.keymap['B'])
    PressKey(eo, cfg.keymap['START'])
    PressKey(eo, cfg.keymap['SELECT'])
    sleep(0.3)
    ReleaseKey(eo, cfg.keymap['A'])
    ReleaseKey(eo, cfg.keymap['B'])
    ReleaseKey(eo, cfg.keymap['START'])
    ReleaseKey(eo, cfg.keymap['SELECT'])
