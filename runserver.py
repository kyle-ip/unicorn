# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : main.py
# @Software: PyCharm

from urls import controller_list
from unicorn import Unicorn


app = Unicorn()
app.load_controller(controllers=controller_list)
app.run()

