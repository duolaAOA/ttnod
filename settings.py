# -*-coding:utf-8 -*-

import os
import uuid
import base64

from models import user
from db.mongohelper import MongoWrapper
from db.mongo_query import MongodbFetch
from db.mongohelper import MongoConnect

mongo_db = MongodbFetch
db = MongoConnect.get_current_db()

cookie_secret = base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)

setting = {
    'debug': True,
    'template_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates/"),
    'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/"),
    'mongo_db': mongo_db,
    'db': db,
    'cookie_secret': cookie_secret,
    'pycket': {
        'engine': 'redis',
        'storage': {
            'host': 'localhost',
            'port': 6379,
            'db_sessions': 10,
            'db_notifications': 11,
        },
        'cookie': {
            'expiers_days': 120,
        },
    }
}
