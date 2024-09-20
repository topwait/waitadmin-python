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
import json
from typing import Optional
from common.utils.cache import RedisUtil


class WechatCache:
    # 缓存信息
    ttl: int = 120               # 过期时间
    prefix: str = "login:scan_"  # 扫码前缀

    # 扫码状态
    SCAN_STATUS_STAY: int = 0  # 等待扫码
    SCAN_STATUS_FAIL: int = 1  # 扫码失败
    SCAN_STATUS_ING: int = 2   # 扫码确认
    SCAN_STATUS_OK: int = 3    # 扫码成功

    @classmethod
    async def login_scan_get(cls, state: str) -> Optional[dict]:
        """
        获取扫码状态

        Args:
            state (str): 盐

        Returns:
            Optional[dict]: 包含扫码状态信息的字典,未找到返回None

        Author:
            zero
        """
        result = await RedisUtil.get(cls.prefix + state)
        if result is not None:
            data = json.loads(result)
            data["expire"] = await RedisUtil.ttl(cls.prefix + state)
            return data
        return None

    @classmethod
    async def login_scan_set(cls, state: str, status: int, token: str = None):
        """
        设置扫码状态

         Args:
            state (str): 盐
            status (int): 状态
            token (int): 登录令牌

        Author:
            zero
        """
        data = {"status": status}
        expire: int = cls.ttl
        if token:
            data["token"] = token

        if status != cls.SCAN_STATUS_STAY:
            ttl = await RedisUtil.ttl(cls.prefix + state)
            expire = 1 if ttl <= 0 else int(ttl)

        await RedisUtil.set(cls.prefix + state, json.dumps(data), expire)

    @classmethod
    async def login_scan_del(cls, state: str):
        """
        删除扫码记录

        Args:
            state (str): 盐

        Author:
            zero
        """
        await RedisUtil.delete(cls.prefix + state)
