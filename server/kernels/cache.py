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
import importlib
from redis import asyncio
from fastapi_cache.backends.redis import RedisBackend

__all__ = ["redis_be"]


def __loading_redis_configs():
    """ Load Redis configuration """
    configs = {}
    try:
        package = importlib.import_module("config")
        clz = getattr(package, "GlobalSetting", None)
        if not clz:
            return configs

        obj = clz().dict()
        redis_config = obj.get("REDIS", {})
        return redis_config
    except ModuleNotFoundError:
        return configs


def register_redis():
    """ Connect Redis """
    c = __loading_redis_configs()
    host: str = c.get("host", "127.0.0.1")
    port: int = int(c.get("port", 6379))

    return asyncio.from_url(
        f"redis://{host}:{port}",
        db=int(c.get("db", 0)),
        encoding=c.get("encoding", "utf-8"),
        username=c.get("username", ""),
        password=c.get("password", ""),
        max_connections=c.get("max_connections"),
        decode_responses=c.get("decode_responses", True)
    )


redis_be: RedisBackend = RedisBackend(register_redis())
