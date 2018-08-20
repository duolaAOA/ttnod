# -*-coding:utf-8 -*-

from settings import mongo_db
import datetime

# print(datetime.now())

def get_weeks_before_toady(n=1):
    '''''
    date format = "YYYY-MM-DD HH:MM:SS"
    '''
    now = datetime.datetime.now()
    if (n < 0):
        return datetime.datetime(now.year, now.month, now.day, now.hour,
                                 now.minute, now.second)
    else:
        n_days_before = now - datetime.timedelta(days=n * 7)
    return datetime.datetime(n_days_before.year, n_days_before.month,
                             n_days_before.day, n_days_before.hour,
                             n_days_before.minute, n_days_before.second)

db = mongo_db.connect_db()
# db.product.insert({"_id":1,"productname":"商品1","price":15})
# db.product.insert({"_id":2,"productname":"商品2","price":36})
#
#
# db.orders.insert({"_id":1,"pid":1,"ordername":"订单1"})
# db.orders.insert({"_id":2,"pid":2,"ordername":"订单2"})
# db.orders.insert({"_id":3,"pid":2,"ordername":"订单3"})
# db.orders.insert({"_id":4,"pid":1,"ordername":"订单4"})
#
# db.product.find()
# db.orders.find()

t = '2018-07-31'
from time import strptime
#把字符串转成datetime
from utils.time_helper import string_to_datetime, get_days_before_current_datetime


def fun():
    obj = db['scores'].aggregate(
        [{
            "$match": {
                "created_at": {
                    "$gte": string_to_datetime('2018-07-28'),
                    "$lt": get_days_before_current_datetime('2018-08-05')
                }
            }
        }, {
            '$lookup': {
                'from': 'users',
                'localField': 'user',
                'foreignField': 'username',
                'as': 'userinfo',
            },
        }, {
            "$project": {
                "msg": 0,
                "user": 0
            },
        },
            {
                "$sort": {
                    "finished_at": -1
                }
            }]
    )
    return obj
a = fun()
from pprint import pprint
for i in a:
    pprint(i)



