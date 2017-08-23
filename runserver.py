# -*- coding: utf-8 -*-
# @Time    : 2017/8/21 22:33
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : runserver.py
# @Software: PyCharm

import os

import unicorn.exceptions as exceptions
from unicorn import Unicorn, render, render_json, render_file, redirect
from unicorn.session import session
from unicorn.view import Controller, BaseView, SessionView


class API(BaseView):

    def get(self, request):
        data = {
            "name": "ywh",
            "company": "aimei",
            "department": "Software Engineering"
        }
        return render_json(data)


class Index(SessionView):

    def get(self, request):
        user = session.get(request, 'user')
        return render("index.html", user=user, message="Hello, Unicorn")


class Login(BaseView):

    def get(self, request, *args, **kwargs):
        return render("login.html")

    def post(self, request, *args, **kwargs):
        # 从 POST 请求中获取 user 参数的值
        user = request.form['user']
        session.push(request, 'user', user)
        return redirect("/")


class Logout(SessionView):
    def get(self, request, *args, **kwargs):
        session.pop(request, 'user')
        return redirect("/")


class Download(BaseView):

    def get(self, request, *args, **kwargs):
        filename = "runserver.py"
        if not os.path.exists(filename):
            raise exceptions.FileNotExistsError
        return render_file()

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
