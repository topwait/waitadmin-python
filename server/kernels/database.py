# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin_fastapi
# | github:  https://github.com/topwait/waitadmin_fastapi
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
import os
import importlib
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

__all__ = ["register_db"]


def __loading_db_configs():
    """ Load Db configuration """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        db_config = obj.get("DATABASES", {})

        if db_config.get("apps"):
            for k, v in db_config.get("apps").items():
                if v and v.get("models") and isinstance(v.get("models"), str):
                    db_config["apps"][k]["models"] = __loading_model_files(v.get("models"))

        return db_config
    except ModuleNotFoundError:
        return configs


def __loading_model_files(path: str):
    """ Load Db models """
    root_path: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep
    mode_path: str = root_path + path.replace(".", os.sep)

    all_files = []
    for root, dirs, filenames in os.walk(mode_path):
        dirs[:] = [d for d in dirs if not d.startswith("__")]
        path_parts = os.path.relpath(root, mode_path).split(os.sep)
        path_parts = [p for p in path_parts if not p.startswith("__")]
        file_base_path = ".".join(path_parts) if path_parts else ""
        for filename in filenames:
            if not filename.startswith("__"):
                filename_without_ext = os.path.splitext(filename)[0]
                if file_base_path and file_base_path.endswith("."):
                    file_base_path = file_base_path[:-1]
                file_path = f"{file_base_path}.{filename_without_ext}" if file_base_path else filename_without_ext
                if not (file_path.startswith(".") and file_path != "."):
                    all_files.append(path + "." + file_path)

    return all_files


def register_db(app: FastAPI):
    """ Connect Databases """
    register_tortoise(
        app,
        config=__loading_db_configs(),
        generate_schemas=False,
        add_exception_handlers=False,
    )
