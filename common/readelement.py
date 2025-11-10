import os
import yaml
from config.config import WEB_ELEMENT_PATH


class Element:

    def __init__(self, path, name):
        self.file_name = '{}.yaml'.format(name)
        self.element_path = os.path.join(path, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("{} File not found.".format(self.element_path))
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def __getitem__(self, item):
        """
        :param item: element location
        :return:
        """
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{} Element not found:{}".format(self.file_name, item))


if __name__ == '__main__':
    search = Element(WEB_ELEMENT_PATH, 'web_login_element')
    print(search['organizationIdInput'])
