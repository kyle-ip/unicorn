# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

from functools import wraps
import datetime
import logging


def parse_static_key(filename):
    return filename.split(".")[-1]


# def request_log(level=logging.DEBUG, name='request_trace'):
#
#     _logger = logging.getLogger(name)
#
#     def decorator(application):
#
#         @wraps(application)
#         def wrapper(request, *args, **kwargs):
#             # token = request_handler.get_argument_by_name('token')
#             # user_id = r.hget(token, 'user_id')
#             # user_name = r.hget(token, 'username')
#             now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             url = request.url
#             args = request.args


