# -*- coding: utf-8 -*-
# @Time    : 2017/8/24
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : admin_view
# @Software: PyCharm

import datetime

from unicorn import Unicorn
from unicorn.session import session
from unicorn.view import BaseView, SessionView
from models import local_redis


def event_stream():
    local_redis.set_channel(sub="chat", pub="chat")
    pubsub = local_redis.subscribe()
    for message in pubsub.listen():
        yield "data: {message}\n\n".format(
            message=message["data"].decode()
        )


class Index(BaseView):

    def get(self):
        user = session.get(self.request, "user")
        if not user:
            return self.redirect("/login")
        return self.render_template("index.html", user=user)


class Login(BaseView):

    def get(self):
        return self.render_template("login.html")

    def post(self):
        user = self.get_arg("user")
        session.push(self.request, "user", user)
        return self.redirect("/")
        # return self.render_template("login.html")


class Message(BaseView):

    def post(self):
        message = self.get_arg("message")
        user = session.get(self.request, "user", "anonymous")
        now = datetime.datetime.now().replace(microsecond=0).time()
        local_redis.publish(
            "[{now}] {user}: {message}".format(
                now=now, user=user, message=message
            )
        )
        return Unicorn.Response(status=204)


class Stream(BaseView):

    def get(self):
        return Unicorn.Response(
            response=event_stream(),
            mimetype="text/event-stream"
        )

