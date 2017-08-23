# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : admin_view
# @Software: PyCharm

from unicorn.view import Controller, BaseView, SessionView


class LoginView(BaseView):

    def get(self, request):
        pass

    def post(self, request):
        pass


class LogoutView(SessionView):
    def get(self, request):
        pass

    def post(self, request):
        pass


