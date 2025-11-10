import os
import logging
from config.config import LOG_PATH
import datetime


class Logger:
    def __init__(self):
        self.logger = logging.getLogger()
        if not self.logger.handlers:
            self.logger.setLevel(logging.DEBUG)

            # File handler
            if not os.path.exists(LOG_PATH):
                os.makedirs(LOG_PATH)
            log_path = os.path.join(LOG_PATH, '{}.log'.format(datetime.datetime.now().strftime("%Y%m")))
            fh = logging.FileHandler(log_path, encoding='utf-8')
            fh.setLevel(logging.INFO)

            # Print to control panel
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # Define format
            fmt = '%(levelname)s\t%(asctime)s\t[%(filename)s:%(lineno)d]\t%(message)s'
            formatter = logging.Formatter(fmt)
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # add to handler
            self.logger.addHandler(fh)
            self.logger.addHandler(ch)


Logger = Logger().logger  # type: ignore

if __name__ == '__main__':
    Logger.info('LOG')  # type: ignore
