# -*-coding:utf-8 -*-

import pymongo
from bson import ObjectId


class MongoPipeline(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 27017
        self.mongo_db = 'zoomeye'
        self.coll = 'scores'

    def process_item(self, items):
        """
        批量插入
        :param items: 列表套字典
        :return:
        """
        with pymongo.MongoClient(host=self.host, port=self.port) as client:
            db = client[self.mongo_db]
            db[self.coll].insert_many(items, ordered=True)

import datetime
import random
def string_to_datetime(string: str):
    """
    将string转为datetime类型
    """
    return datetime.datetime.strptime(string, "%Y-%m-%d")

def get_days_before_current_datetime(string: str, days=1) -> datetime:
    current_datetime = string_to_datetime(string)

    n_days_before = current_datetime + datetime.timedelta(days)
    return datetime.datetime(n_days_before.year, n_days_before.month,
                             n_days_before.day, n_days_before.hour,
                             n_days_before.minute, n_days_before.second)

items = [
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
},
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
},
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
},
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
},
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
},
]

pipe = MongoPipeline()
# for i in range(30):

pipe.process_item(items)



"""
scores表
{
	"balance" : 1,
	"created_at" : get_days_before_current_datetime("2018-08-05"),
	"recharge" : ObjectId("5b519d7375c76353d9e542c1"),
	"score_diff" : random.randint(1,255),
	"score_type" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
}
"""

"""
user 表
{
	"_id" : ObjectId("598047c5b5208c00c65fccfe"),
	"avatar" : "https://images.telnet404.com/avatar.png",
	"email" : "i55m411@sina.com",
	"nickname" : "root",
	"score" : 93,
	"username" : "admin",
	"uuid" : "598047c5bs44vg3c00c65fccfe"
}
"""

"""
recharges 表
{
	"_id" : ObjectId("5b519d7375c76353d9e542c1"),
	"amount" : 21,
	"created_at" : ISODate("2018-07-21T00:29:39.449+08:00"),
	"finished_at" : ISODate("2018-08-01T08:00:00.000+08:00"),
	"msg" : "{\"openid\": \"wxd930ea5d5a258f4f\", \"sub_mch_id\": null, \"cash_fee_type\": \"CNY\", \"settlement_total_fee\": \"301\", \"nonce_str\": \"KnFueXRQbEyYcw7JVdsovq6N9kLzG3rZ\", \"return_code\": \"SUCCESS\", \"err_code_des\": \"SUCCESS\", \"time_end\": \"20180720170444\", \"mch_id\": \"1353383502\", \"trade_type\": \"NATIVE\", \"trade_state_desc\": \"ok\", \"trade_state\": \"SUCCESS\", \"sign\": \"0A974E9BCF1BB6E79DDDA2215374DF80\", \"cash_fee\": \"301\", \"is_subscribe\": \"Y\", \"return_msg\": \"OK\", \"fee_type\": \"CNY\", \"bank_type\": \"CMC\", \"attach\": \"sandbox_attach\", \"device_info\": \"sandbox\", \"out_trade_no\": \"z-20180720162939-19472560\", \"transaction_id\": \"4914992017520180720170444323968\", \"total_fee\": \"301\", \"appid\": \"wxaac7ec0426a05c6c\", \"result_code\": \"SUCCESS\", \"err_code\": \"SUCCESS\"}",
	"out_trade_no" : "z-20180720162939-19472561",
	"pay_type" : 0,
	"score" : 151,
	"status" : 2,
	"user" : ObjectId("598047c5b5208c00c65fccfe")
}
"""