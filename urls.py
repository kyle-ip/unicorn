# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : url
# @Software: PyCharm

from unicorn.view import Controller
from unicorn.route import merge
from views.admin_view import LoginView, LogoutView, IndexView

index = Controller(
    "index",
    merge({
        "": [
            ("/", IndexView, "index"),
            ("/login", LoginView, "login"),
            ("/logout", LogoutView, "logout")
        ],
    })
)

api = Controller(
    "api",
    merge({
        "/api/test": [
            ("/user_info/?", LoginView, "test_user_info"),
        ],
        "/api/service": [
            ("/mac_info/?", LoginView, "mac_info"),
            ("/user_info/?", LoginView, "user_info"),
        ]
    })
)

controller_list = [
    index,
    api
]
