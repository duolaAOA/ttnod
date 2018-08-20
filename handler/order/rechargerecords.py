# -*-coding:utf-8 -*-


import time
import json
from tornado.escape import json_encode
from handler.routes import Route
from ..base import BaseHandler
from db.mongo_query import RechargeRecords


@Route('/trade/recharge/api')
@Route('/trade/recharge/api/(?P<page>\d*)')
class RechargeRecordApi(BaseHandler):
    """
    Recharge 记录查询
    """

    def get(self, page):
        if self.get_argument("out_trade_no"):
            # 按订单号查询
            out_trade_no = self.get_argument("out_trade_no")
            obj = RechargeRecords.get_recharges(self.db, out_trade_no=out_trade_no)
            self.write(json_encode(obj))

        else:
            page = int(self.get_argument("page"))
            limit = int(self.get_argument("limit"))
            recharges_obj = RechargeRecords.get_recharges(self.db, limit=limit, page=page)
            self.write(json_encode(recharges_obj))


@Route('/trade/recharge')
class Recharge(BaseHandler):
    def get(self):
        self.render('recharge_records.html')
