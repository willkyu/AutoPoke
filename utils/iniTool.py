import configparser





class Config:
    def __init__(self, inifile='config.ini') -> None:
        self.inifile=inifile
        self.con=configparser.ConfigParser()
        self.con.read(self.inifile,encoding='utf-8')

    def readConfig(self):
        dic=dict(self.con.items('KEYMAP'))
        self.keymap={key.upper():dic[key] for key in dic}
        self.i=eval(self.con.get('COUNT','I'))

    def writeConfig(self,i):
        self.con['COUNT']['I']=str(i)
        with open(self.inifile,'w') as cfgfile:
            self.con.write(cfgfile)
