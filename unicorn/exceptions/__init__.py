# -*- coding: utf-8 -*-
# @Time    : 2017/8/21
# @Author  : ywh
# @Email   : yipwinghong@outlook.com
# @File    : __init__.py
# @Software: PyCharm

from werkzeug.wrappers import Response


content_type = 'text/html; charset=UTF-8'

# 服务异常响应对象
ErrorMap = {
    '2': Response(
        '<h1>E2 Not Found File</h1>', content_type=content_type, status=500
    ),
    '13': Response(
        '<h1>E13 No Read Permission</h1>', content_type=content_type, status=500
    ),
    '401': Response(
        '<h1>401 Unknown Or Unsupported Method</h1>', content_type=content_type, status=401
    ),
    '404': Response(
        '<h1>404 Source Not Found<h1>', content_type=content_type, status=404
    ),
    '503': Response(
        '<h1>503 Unknown Function Type</h1>', content_type=content_type, status=503
    )
}


def captcure(func):
    """ 异常捕获装饰器 """
    def decorator(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except NormalException as e:
            if e.code in ErrorMap and ErrorMap[e.code]:
                response = ErrorMap[e.code]
                status = int(e.code) if int(e.code) >= 100 else 500
                if isinstance(response, Response) or not response:
                    return response
                else:
                    return Response(
                        response(),
                        content_type=content_type,
                        status=status
                    )
            else:
                raise e
        return response
    return decorator


def reload(code):
    """ 异常重新加载装饰器， """
    def decorator(func):
        ErrorMap[str(code)] = func

    return decorator


class NormalException(Exception):
    """ 框架异常基类 """
    def __init__(self, code='', message='Error'):
        self.code = code            # 异常编号
        self.message = message      # 异常信息

    def __str__(self):
        return self.message         # 直接调用返回异常信息


class EndpointExistsError(NormalException):
    """ 节点已存在 """
    def __init__(self, message='Endpoint exists'):
        super(EndpointExistsError, self).__init__(message)


class URLExistsError(NormalException):
    """ URL已存在 """
    def __init__(self, message='URL exists'):
        super(URLExistsError, self).__init__(message)


class FileNotExistsError(NormalException):
    """ 文件不存在 """
    def __init__(self, code='2', message='File not found'):
        super(FileNotExistsError, self).__init__(code, message)


class RequirePermissionError(NormalException):
    """ 权限不足 """
    def __init__(self, code='13', message='Require permission'):
        super(RequirePermissionError, self).__init__(code, message)


class InvalidRequestMethodError(NormalException):
    """ 不支持的访问类型 """
    def __init__(self, code='401', message='Unknown or unsupported request method'):
        super(InvalidRequestMethodError, self).__init__(code, message)


class PageNotFoundError(NormalException):
    """ 找不到URL """
    def __init__(self, code='404', message='Source not found'):
        super(PageNotFoundError, self).__init__(code, message)


class StaticLoadError(NormalException):
    """ 静态资源加载失败 """
    def __init__(self, code='404', message='Source not found'):
        super(StaticLoadError, self).__init__(code, message)


class UnknownFuncError(NormalException):
    """ URL 未知处理类型 """
    def __init__(self, code='503', message='Unknown function type'):
        super(UnknownFuncError, self).__init__(code, message)


class SQLError(NormalException):
    """ SQL语句错误 """
    def __init__(self, message='SQL Error'):
        super(SQLError, self).__init__(message)


class UnknownDBError(NormalException):
    """ 未知的数据库错误 """
    def __init__(self, message='Unknown DataBase Error'):
        super(UnknownDBError, self).__init__(message)


class UploadError(NormalException):
    """ 上传失败 """
    def __init__(self, message='Failed to upload file'):
        super(UploadError, self).__init__(message)


class UnknownDataTypeError(NormalException):
    """ 未知的数据类型 """
    def __init__(self, message='Unknown DataType Error'):
        super(UnknownDataTypeError, self).__init__(message)


class InsertError(NormalException):
    """ 错误的插入语句 """
    def __init__(self, message='Insert Error'):
        super(InsertError, self).__init__(message)


class ConnectError(NormalException):
    """ 连接错误 """
    def __init__(self, message='Connect Error'):
        super(ConnectError, self).__init__(message)


class InvalidArgumentsError(NormalException):
    """ 非法参数 """
    def __init__(self, message='Invalid Arguments Error'):
        super(InvalidArgumentsError, self).__init__(message)