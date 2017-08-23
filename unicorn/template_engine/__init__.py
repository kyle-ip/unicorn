# -*- coding: utf-8 -*-
# @Time    : 2017/8/22
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import re
import os


pattern = r"{{(.*?)}}"


def parse_args(obj):
    """ 取模板匹配的对象 """
    comp = re.compile(pattern)
    res = comp.findall(obj)

    return res if res else ()


def replace_template(app, path, **kwargs):

    content = "<h1>Not Found Template</h1>"

    path = os.path.join(app.template_folder, path)

    if os.path.exists(path):

        with open(path, "rb") as f:
            content = f.read().decode()
            # content = f.read()

        args = parse_args(content)
        if kwargs:
            for arg in args:
                content = content.replace(
                    "{{%s}}" % arg, str(kwargs.get(arg.strip(), ""))
                )
    return content
