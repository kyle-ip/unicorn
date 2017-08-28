# -*- coding: utf-8 -*-
# @Time    : 2017/8/22
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

import re
import os

from unicorn.settings import TEMPLATE_PATH, INDENT_STEP

pattern = r"{{(.*?)}}"


def parse_args(obj):
    """ 取模板匹配的对象 """
    comp = re.compile(pattern)
    res = comp.findall(obj)
    return res if res else ()


def replace_template(path, **kwargs):

    content = "<h1>Not Found Template</h1>"

    path = os.path.join(TEMPLATE_PATH, path)

    if os.path.exists(path):

        with open(path, "rb") as f:
            content = f.read().decode()
            # content = f.read()

        args = parse_args(content)
        if kwargs:
            for arg in args:
                content = content.replace(
                    "{{%s}}" % arg, str(kwargs.get(arg.strip(), ""))
                )
    return content


class Template(object):
    pass


class CodeBuider(object):

    def __init__(self, indent=0):
        self.code = []
        self.indent_level = indent

    def add_line(self, line):
        self.code.extend([
            " " * self.indent_level, line, "\n"
        ])

    def indent(self):
        self.indent_level += INDENT_STEP

    def dedent(self):
        self.indent_level -= INDENT_STEP

    def add_section(self):
        section = CodeBuider(self.indent_level)
        self.code.append(section)
        return section

    def get_globals(self):
        assert self.indent_level == 0
        python_source = str(self)
        global_namespace = {}

        # 执行存储在字符串中的代码，存放在global_namespace中
        exec(python_source, global_namespace)
        return global_namespace

    def __str__(self):
        return "".join(str(char) for char in self.code)


# class Templite(object):
#
#     def __init__(self, text, *contexts):
#         self.context = {}
#         for context in contexts:
#             self.context.update(context)
#         self.all_vars = set()
#         self.loop_vars = set()
#
#         code = CodeBuider()
#         code.add_line("def render_function(context, do_dots): ")
#         code.indent()
#         vars_code = code.add_section()
#         code.add_line("result = []")
#         code.add_line("append_result = result.append")
#         code.add_line("extend_result = result.extend")
#         code.add_line("to_str = str")
#
#         buffered = []
#
#         def flush_output():
#             if len(buffered) == 1:
#                 code.add_line("append_result({0})".format(buffered[0]))
#             elif len(buffered) > 1:
#                 code.add_line("extend_result({0})".format(",".join(buffered)))
#             del buffered[:]
#
#         ops_stack = []
#
#         # 取{{...}}、{%...%}、{#...#}
#         tokens = re.split(r"(?s)({{.*?}}|{%.*?%}|{#.*?#})", text)
#         for token in tokens:
#             if token.startswith("{#"):
#                 continue
#             elif token.startswith("{{"):
#                 expr = self._expr_code(token[2:-2].strip())
#                 buffered.append("to_str({})".format(expr))
#             elif token.startswith("{%"):
#                 flush_output()
#                 words = token[2:-2].strip().split()
#                 if words[0] == "if":
#                     if len(words) != 2:
#                         self._syntax_error("Dont't, understand if", token)
#                     ops_stack.app("if")
#                     code.add_line("if {0}:".format(self._expr_code(words[1])))
#                     code.indent()
#                 elif words[0] == "for":
#                     if len(words) != 4 or words[2] != "in":
#                         self._syntax_error("Don't understand for", token)
#                     ops_stack.append("for")
#                     self._variable(words[1], self.loop_vars)
#                     code.add_line(
#                         "for c_{0} in {1}".format(
#                             words[1],
#                             self._expr_code(words[3])
#                         )
#                     )
#                     code.indent()
#                 elif words[0].startswith("end"):
#                     if len(words) != 1:
#                         self._syntax_error("Don't understand end", token)
#                     end_what = words[0][3:]
#                     if not ops_stack:
#                         self._syntax_error("Too many ends", token)
#                     start_what = ops_stack.pop()
#                     if start_what != end_what:
#                         self._syntax_error("Mismatched end tag", end_what)
#                     code.dedent()
#                 else:
#                     self._syntax_error("Don't understand tag", words[0])
#             else:
#                 if token:
#                     buffered.append(repr(token))
#         if ops_stack:
#             self._syntax_error("Unmatched action tag", ops_stack[-1])
#         flush_output()



