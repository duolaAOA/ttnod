# -*-coding:utf-8 -*-

import os
from configparser import ConfigParser

SETTINGS_FILENAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.ini'))
config = ConfigParser()
config.read(SETTINGS_FILENAME)


def load_wx_auth():

    return {
        'appid': config.get('INFO', 'appid'),
        'mch_id': config.get('INFO', 'mch_id'),
        'key': config.get('INFO', 'key'),
    }


def load_download_bill_path():
    return config['PATH']['DOWNLOAD_BILL_URL']


