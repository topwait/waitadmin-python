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
from fastapi import FastAPI

__all__ = ["configure_event"]


async def __dynamic_events(app: FastAPI, event: str):
    """ Dynamic execution events """
    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    if os.path.exists(root_path + "events.py"):
        module = importlib.import_module("events")
        clz = getattr(module, "AppEvents", None)
        if clz:
            function = getattr(clz, event, None)
            if function:
                await function(app)


def configure_event(app: FastAPI):
    """ Configure events """
    @app.on_event("startup")
    async def startup():
        await __dynamic_events(app, "startup")

    @app.on_event("shutdown")
    async def shutdown():
        await __dynamic_events(app, "shutdown")
