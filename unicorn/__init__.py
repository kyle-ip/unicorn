# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import os
import json

from werkzeug.serving import run_simple
from werkzeug.wrappers import Response

import unicorn.exceptions as exceptions
from unicorn.wsgi_adapter import wsgi_app
from unicorn.utils import parse_static_key
from unicorn.route import Route
from unicorn.settings import TypeMap
from unicorn.template_engine import replace_template
from unicorn.session import create_session_id, session


def render(path, **kwargs):
    """ 返回模板 """
    return replace_template(Unicorn, path, **kwargs)


def redirect(url, status_code=302):
    """ URL重定向 """
    response = Response("", status=status_code)
    response.headers["Location"] = url
    return response


def render_json(data):
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

@exceptions.captcure
def render_file(file_path, file_name=None):
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


class Unicorn(object):

    def __init__(
            self, static_folder="static", session_path=".session",
            template_folder="template",
    ):
        self.host = "127.0.0.1"                         # 默认主机
        self.port = 8888                                # 默认端口
        self.url_map = {}                               # URL与Endpoint的映射
        self.static_map = {}                            # URL与静态资源的映射
        self.function_map = {}                          # Endpoint与请求处理函数的映射（对象）

        self.route = Route(self)                        # 路由装饰器

        self.session_path = session_path                # 会话记录
        self.static_folder = static_folder              # 静态资源
        self.template_folder = template_folder          # 模板文件
        Unicorn.template_folder = self.template_folder

        self.headers = {"Server": "Unicorn Web 0.1"}
        self.content_type = "text/html; charset=UTF-8"

    def __call__(self, environ, start_response):
        """ WSGI调用框架应用实例的入口 """

        return wsgi_app(self, environ, start_response)

    def run(self, host=None, port=None, **kwargs):
        """ web服务启动入口 """

        # 有参数传入时，把参数设为应用实例的属性
        for key, value in kwargs.items():
            if value:
                self.__setattr__(key, value)

        if host:
            self.host = host
        if port:
            self.port = port

        # 启动时自动添加静态资源路由映射
        self.function_map["static"] = ExceFunc(
            func=self.dispatch_static, func_type="_static"
        )

        if not os.path.exists(self.session_path):
            os.mkdir(self.session_path)
        session.set_storage_path(self.session_path)
        session.load()

        # 把应用本身和其他的配置参数传给werkzeug启动
        run_simple(
            application=self, **kwargs, hostname=self.host, port=self.port
        )

    def bind_view(self, url, view_class, endpoint):
        """ 添加视图规则 """

        # 处理函数即为视图类的类方法，一个视图对应一条URL规则
        self.add_url_rule(
            func=view_class.get_func(endpoint), func_type="_view", url=url
        )

    def load_controller(self, controller):
        """ 加载控制器 """

        name = controller.__name__()
        for rule in controller.url_map:
            self.bind_view(
                url=rule["url"], view_class=rule["view"],
                endpoint=name + "." + rule["endpoint"]      # 节点名为：控制器.节点
            )

    @exceptions.captcure
    def add_url_rule(
            self, url, func, func_type, endpoint=None, **kwargs
    ):
        """ 添加路由规则：URl --- 节点 --- 处理函数 """

        if not endpoint:                                # 节点默认名称为文件名/函数名
            endpoint = func.__name__

        if url in self.url_map:                         # url已存在（重复添加路由规则报错）
            raise exceptions.URLExistsError

        if endpoint in self.function_map \
                and func_type != "_static":             # 节点类型不是静态资源且节点已存在
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
            "Server": "Unicorn Framework"
        } if "session_id" not in request.cookies \
            else {"Server": "Unicorn Framework"}

        # 去除URL中的域名和参数的部分, 并用/连接
        url = "/{url}".format(
            url="/".join(
                request.url.split("/")[3:]
            ).split("?")[0]
        )

        # 通过URL获取节点名（以static开头则为静态资源，否则从URL映射中取）
        if url.find(self.static_folder) == 1 \
                and url.index(self.static_folder) == 1:
            endpoint = "static"
            url = url[1:]
        else:
            endpoint = self.url_map.get(url, None)

        if not endpoint:        # 找不到节点
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
                content_type=self.content_type,
                headers=self.headers,
                status=200
            )
        else:
            raise exceptions.UnknownFuncError

    @exceptions.captcure
    def dispatch_static(self, static_path):
        """ 静态资源路由：加载静态文件 """

        if os.path.exists(static_path):
            file_suffix = parse_static_key(static_path)         # 静态文件后缀名
            doc_type = TypeMap.get(file_suffix, "text/plain")   # 由后缀名取文件标识
            with open(static_path, "rb") as f:                  # 读取静态文件内容并响应
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
                content_type=self.content_type,
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


class ExceFunc(object):
    """ 路由处理函数数据结构（函数体，参数，参数类型） """

    def __init__(self, func, func_type, **kwargs):
        self.func = func
        self.kwargs = kwargs
        self.func_type = func_type      # "_view", "_route", ...
