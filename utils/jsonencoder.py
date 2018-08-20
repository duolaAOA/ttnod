# -*-coding:utf-8 -*-

import json
import datetime
from bson import ObjectId


class JsonEncoder(json.JSONEncoder):
    """
    # 1 >>>   JsonEncoder().encode(dic)
    # 2 >>>   json.dumps(dic, cls=JsonEncoder)
    """
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, datetime.datetime):
            return str(o.strftime('%Y-%m-%d %H:%M:%S'))

        return json.JSONEncoder.default(self, o)
