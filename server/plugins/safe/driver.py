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
import time
import uuid
from typing import Union
from .basics import SecurityBase
from kernels.utils import RequestUtil


class SecurityDriver(SecurityBase):
    configs = {}

    @classmethod
    def module(cls, name: str = "api", config: dict = None):
        if config:
            cls.configs[name] = config
        else:
            if cls.configs.get(name) is not None:
                config = cls.configs.get(name)
            else:
                try:
                    config = {}
                    package = f"apps.{name}.config"
                    module = importlib.import_module(package)
                    obstruction = getattr(module, f"{name.capitalize()}Config", None)
                    config = obstruction.__dict__.get("security") or {} if obstruction else {}
                    cls.configs[name] = config
                except ModuleNotFoundError:
                    pass

        cls.token_limit = int(config.get("token_limit", 100))
        cls.token_timeout = int(config.get("token_timeout", 7200))
        cls.token_renewal = int(config.get("token_renewal", 300))
        cls.is_concurrent = bool(config.get("is_concurrent", True))
        cls.cache_user_key = config.get("cache_prefix", f"login:{name}_") + "user_"
        cls.cache_token_key = config.get("cache_prefix", f"login:{name}_") + "token_"
        return cls

    @classmethod
    async def login(cls, uid: Union[str, int], device: Union[str, int] = "", data: dict = None):
        """ 会话登录 """

        # 获取登录信息
        session = await cls._query_session_by_uid(uid)

        # 更新登录数据
        session["data"] = data or {}

        # 禁止多处登录
        if not cls.is_concurrent:
            for item in session["token_lists"]:
                if device and device != item["device"]:
                    continue
                item["kick_out"] = 1

        # 令牌数量限制
        if cls.token_limit and len(session["token_lists"]) > cls.token_limit:
            num = len(session["token_lists"]) - cls.token_limit
            session["token_lists"] = session["token_lists"][num:]

        # 令牌登录追加
        token: str = cls._make_build_token()
        session["token_lists"].append({
            "uid": uid,
            "key": str(uuid.uuid4()),
            "value": token,
            "device": device,
            "kick_out": 0,
            "login_host": RequestUtil.host,
            "expire_time": int(time.time()) + cls.token_timeout,
            "create_time": int(time.time()),
            "last_op_time": int(time.time()),
            "last_ip_address": RequestUtil.host,
            "last_ua_browser": RequestUtil.ua
        })

        # 写入缓存信息
        await cls._write_token_cache(uid, token)
        await cls._write_users_cache(uid, session)
        return token

    @classmethod
    async def logout(cls, uid: Union[str, int], device: Union[str, int] = ""):
        """ 指定账号注销 """
        session = await cls._query_session_by_uid(uid)
        if not device:
            token_lists = []
            for item in session["token_lists"]:
                token_lists.append(item["value"])
            await cls._delete_users_cache(uid)
            await cls._delete_token_cache(token_lists)
        else:
            token_lists = []
            stay_delete = []
            for item in session["token_lists"]:
                if item["device"] == device:
                    stay_delete.append(item["value"])
                else:
                    token_lists.append(item)

            session["token_lists"] = token_lists
            await cls._write_users_cache(uid, session)
            await cls._delete_token_cache(stay_delete)

    @classmethod
    async def logout_by_token(cls, token: str):
        """ 指定令牌注销 """
        uid = await cls._query_uid_by_token(token)
        session = await cls._query_session_by_uid(uid)

        token_lists = []
        stay_delete = []
        for item in session["token_lists"]:
            if item["value"] == token:
                stay_delete.append(item["value"])
            else:
                token_lists.append(item)

        session["token_lists"] = token_lists
        await cls._write_users_cache(uid, session)
        await cls._delete_token_cache(stay_delete)

    @classmethod
    async def kick_out_by_id(cls, uid: Union[str, int]):
        """ 指定账号踢下线 """
        session = await cls._query_session_by_uid(uid)
        for item in session["token_lists"]:
            item["kick_out"] = 1
        await cls._write_users_cache(uid, session)

    @classmethod
    async def kick_out_by_token(cls, token: str):
        """ 指定令牌踢下线 """
        uid = await cls._query_uid_by_token(token)
        session = await cls._query_session_by_uid(uid)
        for item in session:
            if item["value"] == token:
                item["kick_out"] = 1
        await cls._write_users_cache(uid, session)

    @classmethod
    async def check_login(cls, token: str = "", device: Union[str, int] = ""):
        """ 验证登录状态 """
        if not token:
            token = RequestUtil.token

        uid = await cls._query_uid_by_token(token)
        session = await cls._query_session_by_uid(uid)

        # 找出有效的
        valid_session = [
            item for item in session["token_lists"]
            if item["value"] == token and int(item.get("expire_time", 0)) >= int(time.time())
        ]

        # 没有有效的
        if not valid_session:
            return "invalid"

        # 指定设备的
        if device:
            valid_session = [item for item in valid_session if item["device"] == device]

        # 校验状态值
        if valid_session:
            item = valid_session[0]
            if item.get("kick_out"):
                await cls.logout_by_token(token)
                return "kick"
            elif item.get("is_disable"):
                await cls._refresh_token(uid, token, int(item.get("expire_time", 0)))
                return "disable"
            else:
                await cls._refresh_token(uid, token, int(item.get("expire_time", 0)))
                return "success"

        return "invalid"

    @classmethod
    async def get_login_id(cls, token: str = ""):
        """ 获取登录ID """
        if not token:
            token = RequestUtil.token
        return await cls._query_uid_by_token(token)

    @classmethod
    async def get_login_data(cls, token: str = ""):
        """ 获取登录数据 """
        if not token:
            token = RequestUtil.token

        uid = await cls._query_uid_by_token(token)
        session = await cls._query_session_by_uid(uid)
        return session.get("data") or {}

    @classmethod
    async def get_token_list(cls, uid: Union[str, int], scene: str = "all"):
        """ 获取令牌列表 """
        session = await cls._query_session_by_uid(uid, scene)
        return session["token_lists"]
