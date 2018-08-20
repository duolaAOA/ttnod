# -*-coding:utf-8 -*-

import uuid
import tornado.escape
import hashlib
from ..base import BaseHandler
from handler.routes import Route
from models.user import User


@Route('/register')
class RegisterHandler(BaseHandler):

    def get(self):
        self.render('register.html')

    def post(self):
        username = self.get_argument("email")
        password = self.get_argument("password")
        password = password.encode('utf-8')

        user = User.select().where(User.username == username)
        confirm = True

        for u in user:
            if u.username == username:
                confirm = False

        if confirm:
            salt = uuid.uuid4().hex.encode('utf-8')
            hashed_passed = hashlib.sha512(password + salt).hexdigest()
            User.create(
                username=username,
                password=password,
                salt=salt
            )
            self.redirect('/login')
        else:
            user_exist = u"?attention = " + tornado.escape.url_escape("{} exist".format(username))
            self.redirect(u"/register" + user_exist)