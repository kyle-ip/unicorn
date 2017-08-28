# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import os

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response, ResponseStream

import unicorn.exceptions as exceptions
from unicorn.wsgi_adapter import wsgi_app
from unicorn.common import parse_static_key
from unicorn.route import Route
from unicorn.settings import TypeMap, STATIC_PATH, SESSION_PATH, \
    DEFAULT_CONTENT_TYPE, DEFAULT_HEADER
from unicorn.template_engine import replace_template
from unicorn.session import create_session_id, session


class Unicorn(object):

    def __init__(self):
        self.url_map = {}                   # URL与Endpoint的映射
        self.static_map = {}                # URL与静态资源的映射
        self.function_map = {}              # Endpoint与请求处理函数的映射（对象）
        self.route = Route(self)            # 路由装饰器
        self.headers = DEFAULT_HEADER

    def __call__(self, environ, start_response):
        """ WSGI调用框架应用实例的入口 """

        return wsgi_app(self, environ, start_response)

    def run(self, host="127.0.0.1", port=8888, **kwargs):
        """ web服务启动入口 """

        # 有参数传入时，把参数设为应用实例的属性
        for key, value in kwargs.items():
            if value:
                self.__setattr__(key, value)

        # 启动时自动添加静态资源路由映射
        self.function_map["static"] = ExceFunc(
            func=self.dispatch_static, func_type="_static"
        )

        if not os.path.exists(SESSION_PATH):
            os.mkdir(SESSION_PATH)
        session.set_storage_path(SESSION_PATH)
        session.load()

        # 把应用本身和其他的配置参数传给werkzeug启动
        run_simple(
            application=self, **kwargs, hostname=host, port=port
        )

    def bind_view(self, url, view_class, endpoint):
        """ 添加视图规则 """

        # 处理函数即为视图类的类方法，一个视图对应一条URL规则
        self.add_url_rule(
            func=view_class.get_func(endpoint), func_type="_view", url=url
        )

    def load_controller(self, controllers):
        """ 加载控制器 """

        for controller in controllers:
            name = controller.__name__()
            for rule in controller.url_map:
                # 节点名：控制器.节点
                self.bind_view(
                    url=rule["url"], view_class=rule["view"],
                    endpoint=name + "." + rule["endpoint"]
                )

    @exceptions.captcure
    def add_url_rule(
            self, url, func, func_type, endpoint=None, **kwargs
    ):
        """ 添加路由规则：URl --- 节点 --- 处理函数 """

        # 节点默认名称为文件名/函数名
        if not endpoint:
            endpoint = func.__name__

        # url已存在（重复添加路由规则报错）
        if url in self.url_map:
            raise exceptions.URLExistsError

        # 节点类型不是静态资源且节点已存在
        if endpoint in self.function_map \
                and func_type != "_static":
            raise exceptions.EndpointExistsError

        # 添加URL与节点映射和节点与处理函数映射
        self.url_map[url] = endpoint
        self.function_map[endpoint] = ExceFunc(
            func=func, func_type=func_type, **kwargs
        )

    @exceptions.captcure
    def dispatch_request(self, request):
        """ 路由追踪 """

        self.headers = {
            "Set-Cookie": "session_id={0}".format(
                create_session_id()
            ),
            "Server": "Unicorn Web 0.1"
        } if "session_id" not in request.cookies \
            else self.headers

        # 去除URL中的域名和参数的部分, 并用/连接
        url = "/{url}".format(
            url="/".join(
                request.url.split("/")[3:]
            ).split("?")[0]
        ).split(".")[0]

        # 通过URL获取节点名（以static开头则为静态资源，否则从URL映射中取）
        if url.find(STATIC_PATH) == 1 \
                and url.index(STATIC_PATH) == 1:
            endpoint = "static"
            url = url[1:]
        else:
            endpoint = self.url_map.get(url, None)

        # 找不到节点
        if not endpoint:
            raise exceptions.PageNotFoundError

        # 从处理函数映射中根据函数名取函数体并调用
        exec_function = self.function_map[endpoint]

        if hasattr(self, exec_function.func_type):
            func = getattr(self, exec_function.func_type)
            response = func(exec_function, url=url, request=request)
            if isinstance(response, Response):
                return response
            return Response(
                response=response,
                content_type=DEFAULT_CONTENT_TYPE,
                headers=self.headers,
                status=200
            )
        else:
            raise exceptions.UnknownFuncError

    @exceptions.captcure
    def dispatch_static(self, static_path):
        """ 静态资源路由：加载静态文件 """

        if os.path.exists(static_path):

            # 由静态文件后缀名取文件标识，读取内容并相应
            file_suffix = parse_static_key(static_path)
            doc_type = TypeMap.get(file_suffix, "text/plain")
            with open(static_path, "rb") as f:
                response = f.read()
            return Response(response=response, content_type=doc_type)
        else:
            raise exceptions.StaticLoadError

    def _route(self, func_obj, **kwargs):
        """ 路由处理 """

        request = kwargs.get("request")
        if request.method in func_obj.kwargs.get("methods"):

            # 判断路由的执行函数是否需要请求体进行内部处理
            argcount = func_obj.func.__code__.co_argcount
            response = func_obj.func(request) \
                if argcount > 0 else func_obj.func()
            return Response(
                response=response,
                content_type=DEFAULT_CONTENT_TYPE,
                headers=self.headers,
                status=200
            )

        else:
            raise exceptions.InvalidRequestMethodError

    def _view(self, func_obj, **kwargs):
        """ 视图处理 """

        request = kwargs.get("request")
        return func_obj.func(request)

    def _static(self, func_obj, **kwargs):
        """ 静态资源处理 """

        url = kwargs.get("url")
        return func_obj.func(url)

    @staticmethod
    def Response(
            response="",
            content_type=DEFAULT_CONTENT_TYPE,
            headers=DEFAULT_HEADER,
            mimetype="",
            status=200

    ):
        if mimetype:
            return Response(response=response, mimetype=mimetype)

        return Response(
            response=response, content_type=content_type,
            headers=headers, mimetype=mimetype, status=status
        )


class ExceFunc(object):
    """ 路由处理函数数据结构（函数体，参数，参数类型） """

    def __init__(self, func, func_type, **kwargs):
        self.func = func
        self.kwargs = kwargs
        self.func_type = func_type      # "_view", "_route", ...
