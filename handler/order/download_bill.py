# -*-coding:utf-8 -*-
import json
import datetime

import requests
from handler.routes import Route
from ..base import BaseHandler
from utils import settings, lib


@Route('/trade/bill/(?P<bill_type>\w+)')
class DownloadBill(BaseHandler):
    """
    微信对账单下载
    """
    def post(self, bill_type):
        download_bill_url = settings.load_download_bill_path()
        date_data = json.loads(self.request.body)
        start_date = datetime.datetime.strptime(date_data['st'], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(date_data['et'], '%Y-%m-%d')
        wx_params = settings.load_wx_auth()
        params = {
            'appid': wx_params['appid'],
            'mch_id': wx_params['mch_id'],
            'bill_type': bill_type.upper(),
        }
        while end_date >= start_date:
            bill_date = start_date.strftime('%Y%m%d')
            params['nonce_str'] = lib.get_nonce_str()
            params['bill_date'] = bill_date
            params['sign'] = lib.create_sign(params, wx_params['key'])
            xml = lib.dict_to_xml(params)
            params.pop('sign')
            try:
                req = requests.post(url=download_bill_url, data=xml.encode('utf-8'), timeout=15)
                req.encoding = 'utf-8'
                resp = req.text
                if resp.startswith('<xml>'):
                    xml_to_dict_resp = lib.xml_to_dict(resp)
                    self.write(params["bill_date"] + ' ' + xml_to_dict_resp["return_msg"] + '\n\n')

                else:
                    self.write(resp + '\n')
            except:
                pass

            start_date += datetime.timedelta(days=1)
        self.finish()
