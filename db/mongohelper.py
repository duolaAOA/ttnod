# -*-coding:utf-8 -*-

import json
import datetime
from pymongo import MongoClient, ReadPreference

from utils.time_helper import get_weeks_before_toady, string_to_datetime, get_days_before_current_datetime
from utils.jsonencoder import JsonEncoder


class Config:
    """
    Mongodb Config
    """
    MONGODB_HOST = 'localhost'
    MONGODB_PORT = 27017
    MONGODB_URI = 'mongodb://localhost:27017'
    MONGODB_DB = 'zoomeye'


class MongoConnect:
    """
    Mongodb  连接
    """
    __conn = None
    __mongo_db = None

    @classmethod
    def init(cls):
        """
        初始化一个mongodb连接
        """
        conn = None
        try:
            # 只进行查询操作， 选择secondary节点读取
            conn = MongoClient(Config.MONGODB_URI, read_preferenve=ReadPreference.SECONDARY_PREFERRED)
        except Exception as e:
            print(e)
            conn = MongoClient(host=Config.MONGODB_HOST, port=Config.MONGODB_PORT)
        return conn

    @classmethod
    def get_conn(cls):
        """
        返回数据库连接
        """
        if cls.__conn is None:
            cls.__conn = cls.init()
        return cls.__conn

    @classmethod
    def get_new_db(cls):
        """返回数据库实例"""
        return cls.init()[Config.MONGODB_DB]

    @classmethod
    def get_current_db(cls):
        """返回当前数据库"""
        if cls.__mongo_db is None:
            cls.__mongo_db = MongoConnect.get_conn()[Config.MONGODB_DB]
        return cls.__mongo_db


class MongoWrapper:
    """
    mongo manager
    """

    @classmethod
    def init(cls):
        client = MongoClient(Config.MONGODB_HOST, Config.MONGODB_PORT)
        return client

    @classmethod
    def connect_db(cls):
        db = cls.init()[Config.MONGODB_DB]
        return db

    @classmethod
    def get_aggregate_recharges(cls, table='recharges'):
        """
        历史总览
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "status": {
                    "$eq": 2
                }
            }
        }, {
            "$group": {
                "_id": "$toUid",
                "recharge_total_amount": {
                    "$sum": "$amount"
                },
                "recharge_total_score": {
                    "$sum": "$score"
                },
                "recharge_total_count": {
                    "$sum": 1
                }
            }
        }]
        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_week_aggregate_recharges(cls, table='recharges'):
        """
        一周总览
        """
        db = cls.connect_db()

        params = [{
            "$match": {
                "status": {
                    "$eq": 2
                },
                "finished_at": {
                    "$gte": get_weeks_before_toady(),
                    "$lt": datetime.datetime.now()
                }
            }
        }, {
            "$group": {
                "_id": "$toUid",
                "recharge_week_total_amount": {
                    "$sum": "$amount"
                },
                "recharge_week_total_score": {
                    "$sum": "$score"
                },
                "recharge_week_total_count": {
                    "$sum": 1
                }
            },
        },
            {
                "$project": {
                    "_id": 0
                }
        }]
        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_aggregate_scores(cls, table='scores'):
        """
        历史总览  scores
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "score_type": {
                    "$eq": 2
                },
            },
        },
            {
            "$group": {
                "_id": "$toUid",
                "score_total_score": {
                    "$sum": "$score_diff"
                },
                "score_total_count": {
                    "$sum": 1
                }
            }
        }]
        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_week_aggregate_scores(cls, table='scores'):
        """
        一周总览  scores
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "score_type": {
                    "$eq": 2
                },
                "created_at": {
                    "$gte": get_weeks_before_toady(),
                    "$lt": datetime.datetime.now()
                }
            }
        }, {
            "$group": {
                "_id": "$toUid",
                "score_week_total_score": {
                    "$sum": "$score_diff"
                },
                "score_week_total_count": {
                    "$sum": 1
                }
            },
        },
            {
                "$project": {
                    "_id": 0
                }
        }]
        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_week_recharge_record(cls, page, table='recharges', show_num=20):
        """
        一周充值记录
        :param page:
        :param table:
        :param show_num:   每页显示数据条数
        :return:
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "finished_at": {
                    "$gte": get_weeks_before_toady(),
                    "$lt": datetime.datetime.now()
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
                },
            },
            {
                "$limit": show_num * page
            },
            {
                "$skip": (page - 1) * show_num
        }]
        record_obj = db[table].aggregate(params)

        for item in record_obj:
            new_item = transform_week_recharge_record_status(json.loads(JsonEncoder().encode(item)))
            yield new_item

    @classmethod
    def get_specify_datetime_recharges(cls, specify_datetime, table='recharges'):
        """
        指定日期充值记录总览 -- >  recharges
        """
        db = cls.connect_db()

        params = [{
            "$match": {
                "status": {
                    "$eq": 2
                },
                "finished_at": {
                    "$gte": string_to_datetime(specify_datetime),
                    "$lt": get_days_before_current_datetime(specify_datetime)
                }
            }
        }, {
            "$group": {
                "_id": "$toUid",
                "recharge_specify_total_amount": {
                    "$sum": "$amount"
                },
                "recharge_specify_total_score": {
                    "$sum": "$score"
                },
                "recharge_specify_total_count": {
                    "$sum": 1
                }
            },
        },
            {
                "$project": {
                    "_id": 0
                }

        }]

        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_specify_datetime_scores(cls, specify_datetime, table='scores'):
        """
        指定日期积分记录总览   -->  scores
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "created_at": {
                    "$gte": string_to_datetime(specify_datetime),
                    "$lt": get_days_before_current_datetime(specify_datetime)
                }
            }
        }, {
            "$group": {
                "_id": "$toUid",
                "score_specify_total_score": {
                    "$sum": "$score_diff"
                },
                "score_specify_total_count": {
                    "$sum": 1
                }
            },
        },
            {
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
        record_obj = db[table].aggregate(params)

        for item in record_obj:
            new_item = transform_week_recharge_record_status(json.loads(JsonEncoder().encode(item)))
            yield new_item

    @classmethod
    def get_recharge_specify_datetime_record(cls, specify_datetime, table='recharges', show_num=20000):
        """
        指定日期查询
        """
        db = cls.connect_db()
        params = [{
            "$match": {
                "finished_at": {
                    "$gte": string_to_datetime(specify_datetime),
                    "$lt": get_days_before_current_datetime(specify_datetime)
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
                },
            },
            {
                "$limit": show_num

        }]
        record_obj = db[table].aggregate(params)

        for item in record_obj:
            new_item = transform_week_recharge_record_status(json.loads(JsonEncoder().encode(item)))
            yield new_item


def transform_week_recharge_record_status(dict_item):
    """
    转换订单status
    """
    status_dic = {
        0: "待支付",
        1: "处理中",
        2: "支付成功",
        3: "支付失败"
    }
    status = status_dic.get(int(dict_item["status"]))
    dict_item["status"] = status
    return dict_item
