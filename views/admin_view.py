# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : admin_view
# @Software: PyCharm


from unicorn.session import session
from unicorn.view import Controller, BaseView, SessionView


class IndexView(SessionView):

    def get(self, request):
        # user = self.get_arg(request, "user")
        user = session.get(request, "user")
        return self.render_template("index.html", user=user, message="Hello, Unicorn")

    def post(self, request):
        return


class LoginView(BaseView):

    def get(self, request):
        return self.render_template("login.html")

    def post(self, request):
        user = self.get_arg(request, "user")
        session.push(request, "user", user)
        return "Login success, <a href='/'>return</a>"


class LogoutView(SessionView):
    def get(self, request):
        session.pop(request, 'user')
        return 'Logout success, <a href="/">return</a>'



