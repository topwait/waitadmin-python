# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin-python
# | github:  https://github.com/topwait/waitadmin-python
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
import os
import importlib
import typing
from typing import List
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from kernels.utils import RequestUtil

__all__ = ["configure_middleware"]


def __get_configs():
    """ Get Configuration """
    configs = {"APPS_NAME": "apps"}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        configs["APPS_NAME"] = obj.get("APPS_NAME", "apps")
        return configs
    except ModuleNotFoundError:
        return configs


def __get_directories(path) -> List[str]:
    """ Get application modules """
    directories = []
    for item in os.listdir(path):
        if item.startswith("__") or item.startswith("."):
            continue
        item_path = os.path.join(path, item)
        if os.path.isdir(item_path):
            directories.append(item)
    return directories


def configure_middleware(app: FastAPI):
    """ Configure middleware """
    config: dict = __get_configs()
    apps_name: str = config.get("APPS_NAME", "apps")
    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep

    root_middleware = root_path + "middleware.py"
    if os.path.exists(root_middleware):
        module = importlib.import_module("middleware")
        function = getattr(module, "init_middlewares", None)
        if function:
            function(app)

    single_apps = root_path + apps_name + "/routers"
    if os.path.exists(single_apps):
        if os.path.exists(single_apps + "/middleware.py"):
            module = ".".join([apps_name, "middleware"])
            function = getattr(module, "init_middlewares", None)
            if function:
                function(app)
    else:
        multiple_apps: List[str] = __get_directories(root_path + apps_name)
        for app_module in multiple_apps:
            pack_a = "/".join([apps_name, app_module, "middleware.py"])
            pack_s = ".".join([apps_name, app_module, "middleware"])
            if os.path.exists(root_path + pack_a):
                module = importlib.import_module(pack_s)
                function = getattr(module, "init_middlewares", None)
                if function:
                    function(app)

    basis_middleware: typing.Type[any] = BasisMiddleware
    app.add_middleware(basis_middleware)


def to_user_agent(ua: str):
    ua_dict = {
        "wechat": "MicroMessenger",
        "chrome": "Chrome",
        "firefox": "Firefox",
        "safari": "Safari",
        "opera": "Opera",
        "edge": "Edge"
    }

    ua = ua.lower()
    for key, value in ua_dict.items():
        if value in ua:
            return key

    if "msie" in ua or "trident/" in ua:
        return "ie"

    return "other"


class BasisMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        user_agent: str = str(request.headers.get("User-Agent", ""))
        user_token: str = str(request.headers.get("Authorization", "").split(" ")[-1])
        req_module: str = str(request.url.path.strip("/").split("/")[0])
        request.state.module = req_module
        RequestUtil.ua = to_user_agent(user_agent)
        RequestUtil.port = request.url.port
        RequestUtil.host = request.client.host
        RequestUtil.token = user_token
        RequestUtil.module = req_module
        RequestUtil.scheme = request.scope.get("scheme")
        RequestUtil.method = request.method
        RequestUtil.userAgent = user_agent
        RequestUtil.remotePort = request.client.port
        RequestUtil.url = str(request.url)
        RequestUtil.path = str(request.url.path)
        RequestUtil.domain = str(request.base_url).rstrip("/")
        RequestUtil.rootDomain = str(request.base_url.netloc)
        RequestUtil.pathParams = request.path_params
        RequestUtil.queryParams = request.query_params
        RequestUtil.state = request.state
        RequestUtil.headers = request.headers
        RequestUtil.cookies = request.cookies
        return await call_next(request)
