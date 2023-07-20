import configparser


class Config:
    def __init__(self, inifile='config.ini') -> None:
        self.inifile = inifile
        self.config = configparser.ConfigParser(allow_no_value=True)
        self.config.read(self.inifile, encoding='utf-8')

        self.window_name = self.config.get('DEFAULT', 'window_name')
        self.version = self.config.get('DEFAULT', 'version')
        self.mode = self.config.get('DEFAULT', 'mode')
        self.readConfig()
        self.i = eval(self.config.get('DEFAULT', 'count'))
        dic = dict(self.config.items('KEYMAP'))
        self.keymap = {key.upper(): dic[key] for key in dic}
        self.toMail=self.config.get('MAIL', 'tomail')
        self.mail_host=self.config.get('MAIL', 'host')
        self.sendMail=self.config.get('MAIL', 'sendmail')
        self.sendMail_password=self.config.get('MAIL', 'password')

    def readConfig(self):
        mode_list = ['WILDPOKE', 'STATIONARY']
        if self.mode not in mode_list:
            self.endApp("Error 'mode' in config.ini file.")
        self.mode_config = dict(self.config.items(self.mode))
        pass

    def writeCountConfig(self, i):
        self.config['DEFAULT']['count'] = str(i)
        with open(self.inifile, 'w') as cfgfile:
            self.config.write(cfgfile)

    def endApp(self, message):
        print(message)
        input()
        raise SystemExit(message)
