import os
import configparser
from config.config import INI_PATH


class ReadConfig:

    def __init__(self):
        if not os.path.exists(INI_PATH):
            raise FileNotFoundError("Configuration file {} does not exist.".format(INI_PATH))
        self.config = configparser.RawConfigParser()
        self.config.read(INI_PATH, encoding='utf-8')

    def get(self, section, option):
        return self.config.get(section, option)

    def set(self, section, option, value):
        self.config.set(section, option, value)
        with open(INI_PATH, 'w') as f:
            self.config.write(f)


con = ReadConfig()

if __name__ == '__main__':
    print(con.get("ENV", "HOST"))
