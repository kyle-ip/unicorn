# -*- coding: utf-8 -*-
# @Time    : 2017/8/23
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import redis
import pymysql


class DBResult(object):
    success = False
    result = None
    error = None
    rows = None

    def index_of(self, index):
        if self.success \
                and isinstance(index, int) \
                and self.rows > index >= -self.rows:
            return self.result[index]
        return

    def get_first(self):
        return self.index_of(0)

    def get_last(self):
        return self.index_of(-1)

    @staticmethod
    def handler(func):
        def decorator(*args, **kwargs):
            res = DBResult()
            try:
                res.result, res.rows = func(*args, **kwargs)
                res.success = True
            except Exception as e:
                res.error = e
            return res
        return decorator

    def res_to_dict(self):
        return {
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "rows": self.rows
        }


class MySQLDB(object):
    """ 
    MySQL连接模块 
        host = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'passwd': '123456',
            'db': 'mysql',
            'charset': 'utf8',
            'cursorclass': pymysql.cursors.DictCursor,
            ...
        }
    """

    def __init__(self, host):
        self.conn = pymysql.connect(**host)

    def close(self):
        self.conn.close()

    @DBResult.handler
    def execute(self, sql, params=None):
        """ 执行sql语句 """
        with self.conn as cursor:
            rows = cursor.execute(sql, params) \
                if params and isinstance(params, dict) \
                else cursor.execute(sql)
            result = cursor.fetchall()
        return rows, result

    def executemany(self, sql, params):
        """ 批量执行sql语句 """
        with self.conn as cursor:
            rows = cursor.executemany(sql, params)
            result = cursor.fetchall()
        return rows, result

    def insert(self, sql, params=None):
        """ 插入数据 """
        res = self.execute(sql, params)
        res.result = self.conn.insert_id()
        return res

    @DBResult.handler
    def process(self, func, params=None):
        """ 存储过程调用 """
        with self.conn as cursor:
            rows = cursor.callproc(func, params) \
                if params and isinstance(params, dict) \
                else cursor.callproc(func)
            result = cursor.fetchall()
        return rows, result

    def create_db(self, database, charset="utf8"):
        """ 创建数据库 """
        sql = """
            CREATE DATABASE {database}
            DEFAULT CHARACTER SET {charset}
        """.format(database=database, charset=charset)
        return self.execute(sql)

    def drop_db(self, database):
        sql = """
            DROP DATABASE {database}
        """.format(database=database)
        return self.execute(sql)

    @DBResult.handler
    def select_db(self, database):
        """ 选择数据库 """
        self.conn.select_db(database)
        return None, None

    def get_cur(self, host, cursor_class):
        """ 获取句柄 """

        try:
            self.conn.ping(True)
        except Exception:
            self.conn = pymysql.connect(**host)
        return self.conn.cursor(cursorclass=pymysql.cursors.DictCursor) \
            if cursor_class == "dict" else self.conn.cursor()

    def get_last_insert_id(self):
        """ 返回插入id """
        with self.conn as cursor:
            return cursor.lastrowid


class RedisDB(object):
    """
        Redis连接模块
            host = {
                'host': '172.16.2.50',
                'port': '6379',
                'password': '123456',
                'db': 1
            }
    """

    def __init__(self, host):
        self.conn = redis.Redis(**host)
        self.subscribe_channel = ""
        self.publish_channel = ""

    def set_channel(self, pub, sub):
        setattr(self, "publish_channel", pub)
        setattr(self, "subscribe_channel", sub)

    def get(self, key):
        return self.conn.get(key)

    def set(self, key, value):
        return self.conn.set(key, value)

    def set_ex(self, key, value, expire):
        return self.conn.set(name=key, value=value, ex=expire)

    def keys(self, pattern='*'):
        return self.conn.keys(pattern)

    def delete(self, key):
        return self.conn.delete(key)

    def publish(self, msg):
        return self.conn.publish(self.publish_channel, msg)

    def subscribe(self):
        pub = self.conn.pubsub()
        pub.subscribe(self.subscribe_channel)
        pub.parse_response()
        return pub

    '''
        pub = conn.pubsub()
        pub.subscribe('87.7')
        pub.parse_response()
        while True:
            pub.parse_response()
    '''
