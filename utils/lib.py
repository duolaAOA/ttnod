# -*-coding:utf-8 -*-
import six
import random
import hashlib

from string import ascii_letters, digits

from bs4 import BeautifulSoup
from wechatpy.utils import to_text

from utils import settings

params = settings.load_wx_auth()


def get_nonce_str(length=32):

    return "".join(random.sample(ascii_letters + digits, length))


def create_sign(params, key):
    """
    签名
    :param key:    API 密钥
    :return:   sign  string
    """

    param_list = []
    for k in sorted(params.keys()):
        v = params.get(k)
        if not str(v).strip():
            continue
        param_list.append('{0}={1}'.format(k, v))
    param_list.append('key={}'.format(key))
    md5 = hashlib.md5()
    md5.update('&'.join(param_list).encode('utf-8'))
    return md5.hexdigest().upper()


def verify_sign(dict_res):
    """签名验证"""
    signature = dict_res.pop("sign", None)
    sign = create_sign(params=dict_res, key=params['key'])
    return signature == sign


def dict_to_xml(d):
    xml = ['<xml>\n']
    for k in sorted(d):
        v = d[k]
        if isinstance(v, six.integer_types) or v.isdigit():
            xml.append('<{0}>{1}</{0}>\n'.format(to_text(k), to_text(v)))
        else:
            xml.append('<{0}><![CDATA[{1}]]></{0}>\n'.format(
                to_text(k), to_text(v)))
    xml.append('\n</xml>')
    return ''.join(xml)


def xml_to_dict(xml):
    soup = BeautifulSoup(xml, features='xml')
    xml = soup.find('xml')
    if not xml:
        return {}
    res = dict([(item.name, item.text) for item in xml.find_all()])
    return res

