import os
import yaml
import time
from config.config import WEB_ELEMENT_PATH, LOCATE_MODE_WEB, APP_ELEMENT_PATH, LOCATE_MODE_APP


def inspect_element():
    """
    Inspect if all locations info is correct
    :return:
    """
    start_time = time.time()
    for i in os.listdir(WEB_ELEMENT_PATH):
        _path = os.path.join(WEB_ELEMENT_PATH, i)
        if os.path.isfile(_path):
            with open(_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
                for k in data.values():
                    pattern, value = k.split('==')
                    if pattern not in LOCATE_MODE_WEB:
                        raise AttributeError('Location method is not supported')
        _path = os.path.join(APP_ELEMENT_PATH, i)
        if os.path.isfile(_path):
            with open(_path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
                for k in data.values():
                    pattern, value = k.split('==')
                    if pattern not in LOCATE_MODE_APP:
                        raise AttributeError('Location method is not supported')
    end_time = time.time()
    print("Inspected all location and cost () s".format(end_time - start_time))


if __name__ == '__main__':
    inspect_element()
