# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : url
# @Software: PyCharm

from unicorn.view import Controller
from unicorn.route import merge
from views.index_view import Index, Login, Message, Stream

index = Controller(
    "index",
    merge({
        "/": [
            ("", Index, "index"),
            ("login", Login, "login"),
            ("stream", Stream, "stream"),
            ("message", Message, "message"),
        ],
    })
)

controller_list = [
    index,
]
