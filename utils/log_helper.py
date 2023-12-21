import logging
from logging import config

import os

BASE_DIR = os.getcwd()

LOGGER_CONF_PATH = os.path.join(BASE_DIR, 'logger.conf')


config.fileConfig(LOGGER_CONF_PATH)

def get_logger(logger_name:str='root')-> logging.Logger:
    return logging.getLogger(logger_name)