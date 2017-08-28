# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : url
# @Software: PyCharm

from unicorn.model import RedisDB
from settings import REDIS_CONNECTIONS

local_redis = RedisDB(REDIS_CONNECTIONS["default"]["local_redis"])
