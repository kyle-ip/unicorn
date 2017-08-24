# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : url
# @Software: PyCharm

CONNECTIONS = {
    "default": {
        "data_center": {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "123456",
            "db": "mysql",
            "charset": "utf8",
            # "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True,
            "no_delay": True,
            "read_timeout": None,
            "write_timeout": None,
            "max_allowed_packet": 16 * 1024 * 1024,
        },
        "housekeeper": {
            "host": "127.0.0.1",
            "port": 3306,
            "user": "root",
            "passwd": "123456",
            "db": "mysql",
            "charset": "utf8",
            # "cursorclass": pymysql.cursors.DictCursor,
            "autocommit": True,
            "no_delay": True,
            "read_timeout": None,
            "write_timeout": None,
            "max_allowed_packet": 16 * 1024 * 1024,
        },
    }
}


