# -*-coding:utf-8 -*-

from db.mongohelper import MongoWrapper
from utils.time_helper import get_weeks_before_toady
import datetime

db = MongoWrapper.connect_db()
def fun():
    obj = db.recharges.aggregate(
        [
                {
       "$lookup":
         {
             "from": "users",
             "localField": "user",
             "foreignField": "_id",
             "as": "userinfo"
         }
            }]
    )
    return obj

a = fun()
from pprint import pprint
for i in a:
    pprint(i)