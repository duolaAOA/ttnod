# -*-coding:utf-8 -*-

import json
from pprint import pprint
from settings import db
from db.mongo_query import transform_payment_status_type, transform_score_type
from utils.jsonencoder import JsonEncoder


def _recharges(page, table='recharges', show_num=25):
    """
    测试recharges
    """
    params = [
        {
            "$sort": {
                "finished_at": -1
            },
        },
        {
            "$limit": show_num * page
        },
        {
            "$skip": (page - 1) * show_num
        }]

    record_obj = db[table].aggregate(params)
    a = list(record_obj)
    #
    pprint(a)
    for item in a:
        new_item = transform_payment_status_type(json.loads(JsonEncoder().encode(item)))
        yield new_item


test = _recharges(page=1)
for t in test:
    pprint(t)


def _score(page, table='score', show_num=25):
    """
    测试record

    """
    params = [{
        "$match": {
            "created_at": {
                "$gte": get_weeks_before_toady(),
                "$lt": datetime.datetime.now()
            }
        }
    }, {
        '$lookup': {
            'from': 'users',
            'localField': 'user',
            'foreignField': '_id',
            'as': 'userinfo',
        }
    },
        {
            "$sort": {
                "created_at": -1
            },
        },
        {
            "$limit": show_num * page
        },
        {
            "$skip": (page - 1) * show_num
        }]