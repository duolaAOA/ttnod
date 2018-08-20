# -*-coding:utf-8 -*-

import hashlib

import tornado.escape

from ..base import BaseHandler
from handler.routes import Route
from models.user import User

@Route('/login')
class LoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('email')
        password = (self.get_argument('password')).encode('utf-8')

        user = User.select().where(User.username == username)
        auth = False
        for u in user:
            if u.username == username:
                auth = True
                salt1 = u.salt
                salt1 = salt1.encode('utf-8')
                hashed_password = hashlib.sha512(password + salt1).hexdigest()

            if auth and (hashed_password == u.password):
                self.set_secure_cookie("user", tornado.escape.json_encode(username))
                # set session
                self.session.set("session", username)
                self.redirect('/')

            else:
                error_msg = "?error = " + tornado.escape.url_escape("username or password incorrect")
                self.redirect("/login" + error_msg)

        if not auth:
            error_msg = "?error " + tornado.escape.url_escape("user not exist")
            self.redirect("/register" + error_msg)

