# -*-coding:utf-8 -*-

import json
import datetime

from db.mongohelper import MongoConnect
from utils.jsonencoder import JsonEncoder
from utils.time_helper import get_weeks_before_toady, string_to_datetime, get_days_before_current_datetime


class MongodbFetch:
    """
    mongodb  数据查询
    """

    @classmethod
    def get_aggregate_recharges(cls, table='recharges'):
        """
        历史总览
        """
        db = MongoConnect.get_current_db()
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
        db = MongoConnect.get_current_db()

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
        db = MongoConnect.get_current_db()
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
        db = MongoConnect.get_current_db()
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
        db = MongoConnect.get_current_db()
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
                'foreignField': '_id',
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
            new_item = transform_payment_status_type(json.loads(JsonEncoder().encode(item)))
            yield new_item

    @classmethod
    def get_specify_datetime_recharges(cls, specify_datetime, table='recharges'):
        """
        指定日期充值记录总览 -- >  recharges
        """
        db = MongoConnect.get_current_db()

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
        db = MongoConnect.get_current_db()
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
        obj = db[table].aggregate(params)
        for item in obj:
            yield item

    @classmethod
    def get_recharge_specify_datetime_record(cls, specify_datetime, table='recharges', show_num=20000):
        """
        指定日期查询充值记录
        """
        db = MongoConnect.get_current_db()
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
                'foreignField': '_id',
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
            new_item = transform_payment_status_type(json.loads(JsonEncoder().encode(item)))
            yield new_item


class RechargeRecords:
    """
    充值记录查询
    """

    @classmethod
    def get_recharges(cls, db, out_trade_no=None, limit=20, page=0, table='recharges'):
        if out_trade_no:
            params = [
                {
                    "$match": {
                        "out_trade_no": {
                            "$eq": out_trade_no
                        }
                    }
                },
                {
                    '$lookup': {
                        'from': 'users',
                        'localField': 'user',
                        'foreignField': '_id',
                        'as': 'userinfo',
                    }
                },
                {
                    "$project": {
                        "_id": 0
                    },
                }
            ]
            record_obj = list(db[table].aggregate(params))
            total = len(record_obj)
        else:
            params = [
                {
                    '$lookup': {
                        'from': 'users',
                        'localField': 'user',
                        'foreignField': '_id',
                        'as': 'userinfo',
                    },
                },
                {
                    "$sort": {
                        "finished_at": -1
                    },
                },
                {
                    "$project": {
                        "_id": 0
                    },
                },
                {
                    "$limit": limit * page
                },
                {
                    "$skip": (page - 1) * limit
             }]

            record_obj = list(db[table].aggregate(params))
            total = db[table].find().count()
        recharge_obj = {
            "total": total,
            "rows": record_obj
        }
        for index, item in enumerate(recharge_obj["rows"]):
            item["user"] = item["userinfo"][0]["username"]
            item.pop("userinfo")
            recharge_obj["rows"][index] = transform_payment_status_type(json.loads(JsonEncoder().encode(item)))
        return recharge_obj


def transform_payment_status_type(status_type_dic):
    """
    支付状态 类型 转换
    """
    status_dic = {
        0: "待支付",
        1: "处理中",
        2: "支付成功",
        3: "支付失败"
    }

    pay_type_dic = {
        0: "微信支付",
        1: "支付宝支付",
    }
    pay_status = status_dic.get(int(status_type_dic["status"]))
    pay_type = pay_type_dic.get(int(status_type_dic["pay_type"]))
    status_type_dic["status"] = pay_status
    status_type_dic["pay_type"] = pay_type
    return status_type_dic


def transform_score_type(score_type):
    """
    充值类型
    """
    score_type_dic = {
        1: "内部人员充值",
        2: "充值中心充值",
        3: "兑换API"
    }
    new_score_type = score_type_dic.get(int(score_type["score_type"]))
    score_type["score_type"] = new_score_type
    return score_type