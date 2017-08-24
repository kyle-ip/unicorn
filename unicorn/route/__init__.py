# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm


class Route(object):
    """ 路由装饰器 """

    def __init__(self, app):
        self.app = app

    def __call__(self, url, **kwargs):              # kwargs为装饰器的参数，即url路径

        if "methods" not in kwargs:
            kwargs["methods"] = ["GET"]             # 默认只处理GET请求

        def decorator(func):                        # 添加路由规则
            self.app.add_url_rule(
                url, func, "_route", **kwargs
            )
            return func

        return decorator


def merge(item_list):
    """ 组装controller参数 """

    url_list = []
    for prefix, suffix_list in item_list.items():
        for item in suffix_list:
            url_list.append({
                "url": prefix + item[0],
                "view": item[1],
                "endpoint": item[2]
            })
    return url_list

# 使用装饰器添加路由：每个函数表示一个业务逻辑，修改处理逻辑时整个函数都要被修改
# @app.route("/", methods=["GET"])          # 即调用Route的call方法
# def index():
#     return """
#         <div style='text-align:center'>
#             <h1>Welcome to Unicorn!</h1>
#             If you see this page,
#             the Unicorn is successfully installed and working.</br>
#         </div>
#     """
