# -*- coding: utf-8 -*-
# @Time    : 2017/8/22
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import os
import json

from werkzeug.wrappers import Response

import unicorn.exceptions as exceptions
from unicorn.session import AuthSession, session, get_session_id
from unicorn.template_engine import replace_template


class View(object):
    """ 视图内置基类 """
    methods = None              # 支持的请求方法
    methods_meta = None         # 请求处理函数映射

    def dispatch_request(self, request, *args, **kwargs):
        """ 视图处理函数调度入口 """
        raise NotImplementedError

    @classmethod
    def get_func(cls, name):
        """ 生成视图处理函数，name为节点名 """

        def func(*args, **kwargs):
            # 在处理函数内部实例化视图对象，通过视图对象调用处理函数调度入口，返回视图处理结果
            obj = func.view_class()
            return obj.dispatch_request(*args, **kwargs)

        # 为处理函数绑定属性
        func.view_class = cls
        func.methods = cls.methods
        func.__name__ = name
        func.__doc__ = cls.__doc__
        func.__module__ = cls.__module__

        return func


class BaseView(View):
    """ 视图基类 """

    methods = ["GET", "POST", "PUT", "DELETE"]
    request = None
    session_id = None
    session_map = None

    def post(self):
        pass

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass

    def dispatch_request(self, request, *args, **kwargs):
        methods_meta = {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "DELETE": self.delete,
        }

        self.request = request
        self.session_id = get_session_id(request)
        self.session_map = session.map(request)

        if request.method in methods_meta:
            # 以调用由子类实现的get、post等请求处理方法
            return methods_meta[request.method](*args, **kwargs)
        else:
            raise exceptions.InvalidRequestMethodError

    def get_arg(self, arg, default=None):
        """ 获取请求参数 """
        value = self.request.args.get(arg, None)
        value = self.request.form.get(arg, None) if not value else value
        return value if value else default

    def render_template(self, path, **kwargs):
        """ 返回模板 """
        return replace_template(path, **kwargs)

    def render_json(self, data):
        """ 封装json数据 """
        content_type = "text/plain"
        if isinstance(data, (dict, list)):
            data = json.dumps(data)
            content_type = "application/json"
        return Response(
            response=data,
            content_type="{0}; charset=UTF-8".format(content_type),
            status=200
        )

    @staticmethod
    def redirect(url, status_code=302):
        """ URL重定向 """
        response = Response("", status=status_code)
        response.headers["Location"] = url
        return response

    @exceptions.captcure
    def render_file(self, file_path, file_name=None):
        """ 文件下载 """

        if os.path.exists(file_path):
            if not os.access(file_path, os.R_OK):
                raise exceptions.RequirePermissionError
            with open(file_path, "rb") as f:
                content = f.read()
            if not file_name:
                file_name = file_path.split("/")[-1]

            headers = {
                "Content-Disposition": "attachment; filename='{0}'".format(
                    file_name
                )
            }
            return Response(
                response=content, headers=headers, status=200
            )


class AuthLogin(AuthSession):

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        return BaseView.redirect("/login")

    @staticmethod
    def auth_logic(request, *args, **kwargs):
        return True if "user" in session.map(request) else False


class SessionView(BaseView):
    """ 会话视图基类 """

    @AuthLogin.auth_session
    def dispatch_request(self, request, *args, **kwargs):
        return super(SessionView, self).dispatch_request(request, *args, **kwargs)


class Controller(object):
    """ 控制器类，建立URL与视图的关联 """

    def __init__(self, name, url_map):

        # 存放URL和视图映射关系，[{"url": "/", "view": Index, "endpoint": "index"},]
        self.url_map = url_map
        self.name = name        # 控制器名称，相当于视图的命名空间

    def __name__(self):
        return self.name
