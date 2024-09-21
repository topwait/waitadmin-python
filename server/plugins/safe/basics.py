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
import hashlib
import json
import random
import string
import time
import uuid
from typing import List, Union
from kernels.utils import RequestUtil
from common.utils.cache import RedisUtil


class SecurityBase:
    # 令牌数量限制
    token_limit: int = 100
    # 令牌过期时间
    token_timeout: int = 300
    # 令牌续签期限
    token_renewal: int = 60 * 30
    # 支持并发登录
    is_concurrent: bool = True
    # 用户缓存Key
    cache_user_key: str = "login:api_user_"
    # 令牌缓存Key
    cache_token_key: str = "login:api_token_"

    @classmethod
    async def _query_uid_by_token(cls, token: str):
        """ 根据令牌查UID """
        key: str = cls.cache_token_key + token
        val = await RedisUtil.get(key)
        return val if val else 0

    @classmethod
    async def _query_session_by_uid(cls, uid: Union[int, str], scene: str = "all"):
        """ 根据UID查会话 """
        session = None
        for i in range(3):
            results = await RedisUtil.get(cls.cache_user_key + str(uid))
            if results is not None:
                session = results
                break

        if session is None:
            session = {
                "id": uid,
                "data": {},
                "create_time": int(time.time()),
                "update_time": int(time.time()),
                "token_lists": []
            }
        else:
            session = json.loads(session)

        token_lists = []
        for item in session["token_lists"]:
            if scene == "online" and not item.get("kick_out"):
                token_lists.append(item)
            elif scene == "kick" and item.get("kick_out"):
                token_lists.append(item)
            else:
                token_lists.append(item)

        session["token_lists"] = token_lists
        return session

    @classmethod
    async def _write_users_cache(cls, uid: Union[int, str], value: dict):
        """
        写入用户缓存信息

        Example:
            login:api_user_1 = [{"token_lists": []}]

        Args:
            uid (Union[int, str]): 登录用户ID
            value (str): json字符串,登录令牌信息

        Author:
            zero
        """
        key: str = cls.cache_user_key + str(uid)
        ttl: int = cls.token_timeout + 60 if cls.token_timeout else None
        if value:
            await RedisUtil.set(key, json.dumps(value), ttl)
        else:
            await RedisUtil.delete(key)

    @classmethod
    async def _write_token_cache(cls, uid: Union[int, str], token: str):
        """
        写入令牌缓存信息

        Example:
            login:api_token_c95622552786c5 = 1

        Args:
            uid (Union[int, str]): 登录用户ID
            token (str): 令牌字符串

        Author:
            zero
        """
        key: str = cls.cache_token_key + token
        ttl: int = cls.token_timeout + 60 if cls.token_timeout else None
        await RedisUtil.set(key, uid, ttl)

    @classmethod
    async def _delete_users_cache(cls, uid: Union[int, str]):
        """
        删除用户缓存

        Args:
            uid (Union[int, str]): 用户ID

        Author:
            zero
        """
        key: str = cls.cache_user_key + str(uid)
        await RedisUtil.delete(key)

    @classmethod
    async def _delete_token_cache(cls, tokens: List[str]):
        """
        删除令牌缓存

        Args:
            tokens (List[str]): 令牌

        Author:
            zero
        """
        if not tokens:
            return
        for token in tokens:
            key: str = cls.cache_token_key + token
            await RedisUtil.delete(key)

    @classmethod
    async def _refresh_token(cls, uid: int, token: str, expire_time: int):
        """
        刷新令牌信息

        Args:
            uid (Union[int, str]): 登录用户ID
            token (str): 令牌字符串
            expire_time (int): 失效时间

        Author:
            zero
        """
        session = await cls._query_session_by_uid(uid)
        session['update_time'] = int(time.time())
        for item in session["token_lists"]:
            if item.get("value") == token:
                surplus_time: int = expire_time - int(time.time())
                if cls.token_renewal and surplus_time and (surplus_time <= cls.token_renewal):
                    item["expire_time"] = int(time.time()) + cls.token_timeout
                item["last_op_time"] = int(time.time())
                item["last_ip_address"] = RequestUtil.host
                item["last_ua_browser"] = RequestUtil.ua
                await cls._write_users_cache(uid, session)
                await cls._write_token_cache(uid, token)
                break

    @classmethod
    def _make_build_token(cls) -> str:
        """
        构建令牌字符串

        Returns:
            str: 令牌字符串

        Author:
            zero
        """
        ms = str(time.time())
        mu = str(uuid.uuid4().hex)
        mt = "".join(random.sample(string.digits + string.ascii_letters, 8))
        mk = "".join(random.sample(string.digits + string.ascii_letters, 4))
        m = hashlib.md5()
        m.update(f"{mu}{ms}{mt}".encode("utf-8"))
        return m.hexdigest() + mk
