import configparser


class Config:
    def __init__(self, printf, inifile='config.ini') -> None:
        self.inifile = inifile
        try:
            self.readini()
        except:
            printf("config.ini file not found...")
            self.create_ini()
            printf("New config.ini file has been created.")
            self.readini()

    def readini(self):
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(self.inifile, encoding='utf-8')

        self.window_name = self.config.get('DEFAULT', 'window_name')
        self.version = self.config.get('DEFAULT', 'version')
        self.mode = self.config.get('DEFAULT', 'mode')
        self.readConfig()
        self.i = eval(self.config.get('DEFAULT', 'count'))
        dic = dict(self.config.items('KEYMAP'))
        self.keymap = {key.upper(): dic[key] for key in dic if key in ['up','down','left','right','a','b','start','select']}
        self.toMail=self.config.get('MAIL', 'tomail')
        self.mail_host=self.config.get('MAIL', 'host')
        self.sendMail=self.config.get('MAIL', 'sendmail')
        self.sendMail_password=self.config.get('MAIL', 'password')
        self.ifsend=eval(self.config.get('MAIL', 'ifsend'))

    def readConfig(self):
        mode_list = ['WILDPOKE', 'STATIONARY']
        if self.mode not in mode_list:
            self.endApp("Error 'mode' in config.ini file.")
        self.mode_config = dict(self.config.items(self.mode))
        pass

    def writeCountConfig(self):
        self.config['DEFAULT']['count'] = str(self.i)
        with open(self.inifile, 'w',encoding='utf-8') as cfgfile:
            self.config.write(cfgfile)

    def updateConfig(self,block,item,value):
        self.config[block][item]=value
        with open(self.inifile, 'w',encoding='utf-8') as cfgfile:
            self.config.write(cfgfile)

    def endApp(self, message):
        print(message)
        input()
        raise SystemExit(message)

    def create_ini(self):
        configfile = configparser.ConfigParser(allow_no_value=True)
        configfile["DEFAULT"]={'window_name_comment': '"Window name of Operator."', 'window_name': 'Playback', 'version_comment': '"Your game version, RS/E/FrLg."', 'version': 'RS', 'mode_comment': '"Choose mode, WILDPOKE or STATIONARY."', 'mode': 'WILDPOKE', 'count_comment': '"Count of encounters."', 'count': '0'}
        configfile["MAIL"]={'ifsend_comment': '"If send the mail."', 'ifsend': 'False', 'tomail_comment': '"The mail to receive message."', 'tomail': 'your receiving mail', 'host_comment': '"The host of the mail to send message."', 'host': 'smtp host', 'sendmail_comment': '"The mail to send message."', 'sendmail': 'yourmail', 'password_comment': '"Password of your sendMail."', 'password': 'yourpassword'}
        configfile["WILDPOKE"]={'jump_comment': '"If use bicycle to jump."', 'jump': 'False', 'run_comment': '"If running."', 'run': 'False', 'iflr_comment': '"Move left and right or up and down, needed only jump is false."', 'iflr': 'True'}
        configfile["STATIONARY"]={'hitkeys_comment': '"NOT Completed."', 'hitkeys': '[]'}
        configfile["KEYMAP"]={'up': 'UP', 'down': 'DOWN', 'left': 'LEFT', 'right': 'RIGHT', 'a': 'X', 'b': 'Z', 'start': 'ENTER', 'select': 'BACKSPACE'}
        with open(self.inifile, 'w',encoding='utf-8') as cfgfile:
            configfile.write(cfgfile)
        pass
