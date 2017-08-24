# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : main.py
# @Software: PyCharm

import os

import unicorn.exceptions as exceptions
from unicorn import Unicorn
from unicorn.view import Controller, BaseView, SessionView


class API(BaseView):

    def get(self, request):
        data = {
            "name": "ywh",
            "company": "aimei",
            "department": "Software Engineering"
        }
        return self.render_json(data)


class Index(SessionView):

    def get(self, request):
        user = session.get(request, 'user')
        return self.render_template("index.html", user=user, message="Hello, Unicorn")


class Login(BaseView):

    def get(self, request, *args, **kwargs):
        return self.render_template("login.html")

    def post(self, request, *args, **kwargs):
        # 从 POST 请求中获取 user 参数的值
        user = request.form['user']
        session.push(request, 'user', user)
        return self.redirect("/")


class Logout(SessionView):
    def get(self, request, *args, **kwargs):
        session.pop(request, 'user')
        return self.redirect("/")


class Download(BaseView):

    def get(self, request, *args, **kwargs):
        filename = "main.py"
        if not os.path.exists(filename):
            raise exceptions.FileNotExistsError
        return self.render_file()

unicorn_url_map = [
    {
        'url': '/',
        'view': Index,
        'endpoint': 'index'
    }, {
        'url': '/login',
        'view': Login,
        'endpoint': 'test'
    }, {
        'url': '/logout',
        'view': Logout,
        'endpoint': 'logout'
    }, {
        "url": "/api",
        "view": API,
        "endpoint": "api",
    }, {
        "url": "/download",
        "view": Download,
        "endpoint": "download"
    }
]

app = Unicorn()
index_controller = Controller("index", unicorn_url_map)
app.load_controller(index_controller)
app.run()
