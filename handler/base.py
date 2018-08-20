# -*-coding:utf-8 -*-

from tornado.web import RequestHandler
from pycket.session import SessionMixin
from pycket.notification import NotificationMixin


class BaseHandler(RequestHandler, SessionMixin, NotificationMixin):

    def initialize(self):
        self.mongdb_db = self.settings['mongo_db']
        self.db = self.settings['db']

    def get_current_user(self):
        return self.get_secure_cookie('user')


