# -*-coding:utf-8 -*-


from peewee import Model, CharField
from playhouse.pool import PooledMySQLDatabase


mysql_db = PooledMySQLDatabase("tornado_auth", user='root', password='1219960386', host='127.0.0.1', port=3306,
                               max_connections=20, stale_timeout=300)


class AuthenticationModel(Model):
    class Meta:
        database = mysql_db


class User(AuthenticationModel):
    username = CharField(unique=True, null=False)
    password = CharField(null=False)
    salt = CharField()


mysql_db.connect()
mysql_db.create_tables([User, ], safe=True)
