# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : url
# @Software: PyCharm

from unicorn.view import Controller
from unicorn.route import merge
from views.admin_view import LoginView, LogoutView


service_controller = Controller(
    "service",
    merge({
        "/service/online": [
            ("/login/?", LoginView, "login"),
            ("/logout/?", LogoutView, "logout"),
        ],
        "/service/log": [
            ("/upload_file/?", LoginView, "upload"),
        ]
    })
)

controller_list = [
    service_controller,
]
