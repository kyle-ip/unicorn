# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

from werkzeug.wrappers import Request


def wsgi_app(app, environ, start_response):
    """
    :param app: 应用实例
    :param environ: 服务器传来的请求
    :param start_response: 响应载体
    :return: 响应
    """

    request = Request(environ=environ)          # 把请求头解析为request对象
    response = app.dispatch_request(request)    # 把请求传递给路由处理
    return response(environ, start_response)