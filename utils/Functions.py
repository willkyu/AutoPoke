# from multiprocessing.connection import wait
from time import sleep
from utils.pressTool import *
from utils.colorTool import *
from utils.mailTools import sendMail
from random import choice

# from atexit import register, unregister
from utils.iniTool import *


# class posConfig:
#     def __init__(self, eo) -> None:
#         # getColor(eo, 1, 1)
#         # self.w, self.h = getSize()

#         # self.colorPos = [self.percentXPos(955), self.percentYPos(400)]
#         # self.colorPos = [943, 430]  # BGYellow
#         # self.colorPos = [915,430]
#         self.colorPos = [690, 455]
#         # self.colorPos0 = [self.percentXPos(555), self.percentYPos(
#         #     360)] if inCave else self.colorPos
#         self.colorPos0 = [510, 350]
#         # self.colorPos1 = [self.percentXPos(945), self.percentYPos(660)]
#         self.colorPos1 = [900, 620]

# def percentXPos(self, x: int):
#     return int(x*self.w/1116)

# def percentYPos(self, y: int):
#     return int(y*self.h/714)


# (255, 251, 247)白色
# white = [(255, 251, 247)]  # +[(254+i, 250+j, 246+k) for i in range(2)
# for j in range(3) for k in range(3)]
# (255, 251, 255)(77, 76, 77)Dialogue
dialogueColor = [
    (255, 251, 255),
    (77, 76, 77),
]  # +[(254+i, 250+j, 254+k) for i in range(3) for j in range(3) for k in range(3)] + \
# [(76+i, 75+j, 76+k) for i in range(3)
# for j in range(3) for k in range(3)]
# (0, 0, 0) 黑色
# black = [(0+i, 0+j, 0+k) for i in range(3) for j in range(3) for k in range(3)]
# (107, 162, 165)BG深绿 宝石
BGdeepGreen = [(107, 162, 165)]  # +[(106+i, 161+j, 165+k) for i in range(3)
# for j in range(3) for k in range(3)]
# (41, 81, 107)BG深蓝 火叶
BGdeepBlue = [(41, 81, 107)]  # +[(41+i, 81+j, 107+k) for i in range(3)
#   for j in range(3) for k in range(3)]

# (255, 251, 222)BG浅黄
BGYellow = [(255, 251, 222)]  # +[(254+i, 250+j, 221+k) for i in range(2)
# for j in range(3) for k in range(3)]


def ReadColor(colorList: list):
    global dialogueColor, BGdeepGreen, BGdeepBlue, BGYellow
    try:
        dialogueColor, BGdeepGreen, BGdeepBlue, BGYellow = colorList
    except:
        print("Read color from ini failed.")


def RandomHitKey(eo, keyList):
    HitKey(eo, choice(keyList))


def exit_print_i(i, cfg: Config, printf):
    printf("No shiny pokemon in {} times.".format(i))
    cfg.writeCountConfig(i)
    # sleep(5)


def RUN(eo, cfg: Config, printf):
    # printf("Run...")
    HitKey(eo, cfg.keymap["RIGHT"])
    HitKey(eo, cfg.keymap["DOWN"])
    HitKey(eo, cfg.keymap["A"])
    sleep(0.5)
    HitKey(eo, cfg.keymap["A"])
    sleep(2.7)


def sendMail_(eo, cfg: Config, i, printf):
    if cfg.ifsend:
        saveImg(eo)
        try:
            sendMail(
                i,
                cfg.toMail,
                cfg.mail_host,
                cfg.sendMail,
                cfg.sendMail_password,
                printf,
            )
        except:
            printf("Please open config.ini file to config email information.")


def WILDPOKE(eo, cfg: Config, printf, update_count):
    getColorTest(eo, printf)
    # inCave = eval(cfg.mode_config['incave'])
    jump = eval(cfg.mode_config["jump"])
    run = eval(cfg.mode_config["run"])
    ifLR = eval(cfg.mode_config["iflr"])
    # SLs = cfg.i
    # pos = posConfig(eo)

    # 默认左右走，ifLR=False时，上下走
    # register(exit_print_i, i=SLs, cfg=cfg, printf=printf)
    keyList = (
        [cfg.keymap["LEFT"], cfg.keymap["RIGHT"]]
        if ifLR
        else [cfg.keymap["UP"], cfg.keymap["DOWN"]]
    )

    # 如果在洞穴就检测中间部分
    # [555, 375]  [590,475]
    # pos.colorPos0 if inCave else pos.colorPos
    printf("Encountering...")
    while 1:
        # print(run)
        # move till encounter
        if jump or run:

            PressKey(eo, cfg.keymap["B"])
            # PressKey(eo, cfg.keymap['B'])
            # sleep(0.1)
        # colorcount=100
        # colorGot = getColor(eo, *pos.colorPos0)
        while 1:
            if not jump:
                RandomHitKey(eo, keyList)
                # HitKey(eo,cfg.keymap['B'])
            else:
                sleep(0.1)

            # colorGot = getColor(eo, *pos.colorPos0)
            # colorcount-=1
            # if colorcount<=0:
            #     colorGot = getColor(eo, *pos.colorPos0)
            #     colorcount=100

            # encounter
            # if colorGot in black:
            if black_out(eo):
                printf("A wild pokemon encountered!")
                if jump or run:
                    ReleaseKey(eo, cfg.keymap["B"])
                flag = True
                while black_out(eo):
                    if flag:
                        sleep(0.98)
                        flag = False
                # while colorGot in black:
                #     colorGot = getColor(eo, *pos.colorPos0)
                #     if flag:
                #         sleep(0.98)
                #         flag=False

                cfg.i += 1
                update_count(cfg.i)
                # unregister(exit_print_i)
                # register(exit_print_i, i=SLs, cfg=cfg)
                break
            elif cfg.version == "E":
                # colorGot = getColor(eo, *pos.colorPos1)
                # if colorGot in dialogueColor:
                #     printf("PokeNav detected.")
                #     while colorGot in dialogueColor:
                #         HitKey(eo, cfg.keymap['B'])
                #         colorGot = getColor(eo, *pos.colorPos1)
                if color_exist(eo, dialogueColor):
                    printf("PokeNav detected.")
                    while color_exist(eo, dialogueColor):
                        HitKey(eo, cfg.keymap["B"])
                        sleep(0.2)

        sleep(3.6)
        # if cfg.version=='E':
        #     sleep(0.27)
        HitKey(eo, cfg.keymap["A"])
        HitKey(eo, cfg.keymap["A"])
        printf("Hit A.")
        # if in safari zone, it's much more faster than others.
        # sleep(0.2)
        # colorGot = getColor(eo, *pos.colorPos)
        # if colorGot in BGYellow:
        #     printf("Not shiny, run...")
        #     # print('Zone')
        #     RUN(eo, cfg)
        #     continue
        if color_exist(eo, BGYellow):
            printf("Not shiny, run...")
            RUN(eo, cfg, printf)
            continue

        printf("not safari...")
        sleep(2.8)
        # getColor_(eo,*pos.colorPos)
        # printf("detecting...")
        # colorGot = getColor(eo, *pos.colorPos)
        # # print(colorGot)
        # if colorGot not in BGYellow:
        #     printf('Got Shiny Pokemon!')
        #     sendMail_(eo,cfg, i=cfg.i,printf=printf)
        #     cfg.writeCountConfig(0)
        #     # unregister(exit_print_i)
        #     break
        if not color_exist(eo, BGYellow):
            printf("Got Shiny Pokemon! {} times.".format(cfg.i))
            sendMail_(eo, cfg, i=cfg.i, printf=printf)
            cfg.i = 0
            cfg.writeCountConfig()
            # cfg.i += 1
            # update_count(cfg.i)
            # unregister(exit_print_i)
            break

        # colorGot = getColor(eo, *pos.colorPos1)
        # if colorGot in BGdeepGreen + BGdeepBlue:
        #     # 额外动画检测
        #     # print('威吓!')
        #     # sleep(3.6)
        #     printf("Special anime detected.")
        #     while 1:
        #         colorGot = getColor(eo, *pos.colorPos1)
        #         if colorGot not in BGdeepGreen + BGdeepBlue:
        #             sleep(0.02)
        #             break
        #         sleep(0.1)
        if color_exist_(eo, BGdeepGreen) or color_exist_(eo, BGdeepBlue):
            # 额外动画检测
            # print('威吓!')
            # sleep(3.6)
            printf("Special anime detected.")
            while 1:
                # colorGot = getColor(eo, *pos.colorPos1)
                if not color_exist_(eo, BGdeepGreen) and not color_exist_(
                    eo, BGdeepBlue
                ):
                    sleep(0.02)
                    break
                sleep(0.1)

        printf("Not shiny, run...")
        RUN(eo, cfg, printf)
        printf("Encountering...")


def STATIONARY(eo, cfg: Config, printf, update_count, hitkeys=[]):
    getColorTest(eo, printf)
    ifFRLG = cfg.version == "FrLg"

    # SLs = eval(cfg.i)
    # register(exit_print_i, i=cfg.i, cfg=cfg)
    # pos = posConfig(eo)
    delay_list = [a / 100 for a in range(0, 60, 2)]
    # SLs = i
    while 1:
        sleep(choice(delay_list))
        for key in hitkeys:
            HitKey(key)
        # hit 'A' till encounter
        while 1:
            HitKey(eo, cfg.keymap["A"])
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:
            if black_out(eo):
                printf("encountered!")
                flag = True
                while black_out(eo):
                    if flag:
                        sleep(0.98)
                        flag = False
                cfg.i += 1
                update_count(cfg.i)
                # unregister(exit_print_i)
                # register(exit_print_i, i=cfg.i, cfg=cfg)
                break
            sleep(0.1)
        sleep(4)
        HitKey(eo, cfg.keymap["A"])
        printf("Hit A.")
        sleep(3)
        # colorGot = getColor(eo, *pos.colorPos)
        # if colorGot not in BGYellow:
        if not color_exist(eo, BGYellow):
            printf("Got Shiny Pokemon!")
            sendMail_(eo, cfg, i=cfg.i, printf=printf)
            cfg.writeCountConfig(0)
            # unregister(exit_print_i)
            break
        printf("SLing...")
        SL(eo, cfg)
        sleep(2)
        HitKey(eo, cfg.keymap["A"])
        HitKey(eo, cfg.keymap["A"])
        sleep(0.5)
        HitKey(eo, cfg.keymap["A"])
        sleep(0.5)
        if ifFRLG:
            # skip memory recall 跳过回忆
            HitKey(eo, cfg.keymap["B"])
            sleep(0.5)

        # hit 'A' till entering
        while 1:
            HitKey(eo, cfg.keymap["A"])
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:
            if black_out(eo):
                break
            sleep(0.1)

        while 1:
            HitKey(eo, cfg.keymap["A"])
            # colorGot = getColor(eo, *pos.colorPos)
            # if colorGot in black:
            if black_out(eo):
                break
            sleep(0.1)
    pass


def fishing(eo, ifFRLG=False):

    pass


def SL(eo, cfg: Config):
    """
    eo SL once
    """
    PressKey(eo, cfg.keymap["A"])
    PressKey(eo, cfg.keymap["B"])
    PressKey(eo, cfg.keymap["START"])
    PressKey(eo, cfg.keymap["SELECT"])
    sleep(0.3)
    ReleaseKey(eo, cfg.keymap["A"])
    ReleaseKey(eo, cfg.keymap["B"])
    ReleaseKey(eo, cfg.keymap["START"])
    ReleaseKey(eo, cfg.keymap["SELECT"])


def release_all_keys(eo, cfg: Config):
    for key in cfg.keymap.values():
        ReleaseKey(eo, key)
