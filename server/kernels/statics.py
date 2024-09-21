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
from typing import List
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

__all__ = ["configure_static"]


def __loading_static_configs():
    """ Load Static configuration """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        static_config = obj.get("STATIC_DIR", [])
        return static_config
    except ModuleNotFoundError:
        return configs


def configure_static(app: FastAPI):
    """ Configure static resources """
    statics: List[tuple] = __loading_static_configs()
    for t in statics:
        directory: str = os.path.join(os.getcwd(), t[1])
        app.mount(t[0], StaticFiles(directory=directory), name=t[2])
