
from django.http.response import HttpResponse


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.method == "OPTIONS":
           # post 请求有个options 请求 用来校验允不允许跨域的机制
            response = HttpResponse("")
            response["Access-Control-Allow-Origin"] = "*" # 设置允许的跨域请求来源
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
            response["Access-Control-Max-Age"] = 1000
            response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, " \
                                                       "WG-App-Version, WG-Device-Id, WG-Network-Type, WG-Vendor," \
                                                       " WG-OS-Type, WG-OS-Version, WG-Device-Model, WG-CPU, WG-Sid," \
                                                       " WG-App-Id, WG-Token"
            response["Access-Control-Allow-Credentials"] = "true"
            return response
        """
        响应头要加新的字段
        """
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
        response["Access-Control-Max-Age"] = 1000
        response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept, " \
                                                   "WG-App-Version, WG-Device-Id, WG-Network-Type, WG-Vendor, " \
                                                   "WG-OS-Type, WG-OS-Version, WG-Device-Model, WG-CPU," \
                                                   " WG-Sid, WG-App-Id, WG-Token"
        response["Access-Control-Allow-Credentials"] = "true"

        # Code to be executed for each request/response after
        # the view is called.

        return response