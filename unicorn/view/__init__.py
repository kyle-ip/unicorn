# -*- coding: utf-8 -*-
# @Time    : 2017/8/22
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

from unicorn.session import AuthSession, session
from unicorn import redirect


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
    methods = ["GET", "POST"]

    def post(self, request):
        pass

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass

    def dispatch_request(self, request, *args, **kwargs):
        methods_meta = {
            "GET": self.get,
            "POST": self.post,
            "PUT": self.put,
            "DELETE": self.delete,
        }
        if request.method in methods_meta:

            # 以调用由子类实现的get、post等请求处理方法
            return methods_meta[request.method](request, *args, **kwargs)
        else:
            return '<h1>Unknown or unsupported require method</h1>'


class AuthLogin(AuthSession):

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        return redirect("/login")

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
