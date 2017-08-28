# -*- coding: utf-8 -*-
# @Time    : 2017/8/23
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import os
import base64
import time
import pickle


def create_session_id():
    return base64.encodebytes(
        str(time.time()).encode()
    ).decode().replace("=", '')[:-2][::-1]

# 规则：首先获取当前时间戳，转换为字符串并编码为字节流，
# 再 Base64 编码、解码为字符串，然后去掉 Base64 编码会出现的“=”号，取到倒数第二位，最后再进行倒序排列


def get_session_id(request):
    return request.cookies.get("session_id", "")


class Session(object):

    __instance = None

    def __init__(self):
        self.__session_map__ = {}

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Session, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def set_storage_path(self, path):
        """ 设置会话保存目录 """
        self.__storage_path__ = path

    def storage(self, session_id):
        """ 保存会话记录到本地 """
        session_path = os.path.join(self.__storage_path__, session_id)
        if self.__storage_path__:
            with open(session_path, "wb") as f:
                pickle.dump(self.__session_map__[session_id], f)
                # content = json.dumps(self.__session_map__[session_id])
                # f.write(base64.encodebytes(content.encode()))

    def load(self):
        """ 加载本地会话记录 """
        if self.__storage_path__:
            session_path_list = os.listdir(self.__storage_path__)
            for session_id in session_path_list:
                path = os.path.join(self.__storage_path__, session_id)
                with open(path, "rb") as f:
                    self.__session_map__[session_id] = pickle.load(f)
                    # content = f.read()
                # self.__session_map__[session_id] = json.loads(content.decode())

    def push(self, request, item, value):
        """ 更新或添加记录 """

        print("OK")
        session_id = get_session_id(request)
        if session_id in self.__session_map__:
            self.__session_map__[get_session_id(request)][item] = value
        else:
            self.__session_map__[session_id] = {}
            self.__session_map__[session_id][item] = value
        self.storage(session_id)

    def pop(self, request, item, value=True):
        """ 删除记录 """
        session_id = get_session_id(request)
        current_session = self.__session_map__.get(session_id, {})
        if item in current_session:
            current_session.pop(item, value)
            self.storage(session_id)

    def map(self, request):
        """ 获取当前会话记录 """
        return self.__session_map__.get(get_session_id(request), {})

    def get(self, request, item, value=""):
        """ 获取当前会话某个项 """
        item = self.__session_map__.get(get_session_id(request), {}).get(item)
        return item if item else value


class AuthSession(object):

    @classmethod
    def auth_session(cls, f, *args, **kwargs):
        def decorator(obj, request):
            if cls.auth_logic(request, *args, **kwargs):
                return f(obj, request)
            else:
                return cls.auth_fail_callback(request, *args, **kwargs)
        return decorator

    @staticmethod
    def auth_logic(request, *args, **kwargs):
        raise NotImplementedError

    @staticmethod
    def auth_fail_callback(request, *args, **kwargs):
        raise NotImplementedError

session = Session()


