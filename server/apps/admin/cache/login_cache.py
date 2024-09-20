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
from typing import List
from common.utils.cache import RedisUtil
from common.utils.tools import ToolsUtil
from common.models.auth import AuthMenuModel
from common.models.auth import AuthPermModel
from plugins.safe.driver import SecurityDriver


class LoginCache:
    captcha_ttl: int = 60 * 5                     # 验证码时长
    perms_prefix: str = "login:roles_perms"       # 权限的前缀
    captcha_prefix: str = "login:admin_captcha_"  # 验证码前缀

    @classmethod
    async def login(cls, admin_id: int, role_id: int):
        """ 登录系统 """
        return await (SecurityDriver
                      .module("admin")
                      .login(uid=admin_id, data={"role_id": role_id}))

    @classmethod
    async def logout(cls, token: str):
        """ 退出系统 """
        return await (SecurityDriver
                      .module("admin")
                      .logout_by_token(token))

    @classmethod
    async def role_perms_get(cls, role_id: int = None) -> List[str]:
        """ 角色权限缓存获取 """
        if not role_id:
            return []

        # 缓存中查找角色权限
        perms = await RedisUtil.hGet(cls.perms_prefix, str(role_id))

        # 如权限不存在则获取
        if perms is None:
            menu_ids = await AuthPermModel.filter(role_id=role_id).all().values("menu_id")
            menu_ids = [item["menu_id"] for item in menu_ids]
            if menu_ids:
                _menus = await AuthMenuModel.filter(id__in=menu_ids).all().values("perms")
                _auths = [item["perms"] for item in _menus]
                _perms = [item.replace("/", ":") for item in _auths]
                # {"1": "["index:console"]", "2": []}
                await RedisUtil.hSet(cls.perms_prefix, str(role_id), json.dumps(_perms))
                return _perms
            return []
        else:
            return json.loads(perms)

    @classmethod
    async def role_perms_del(cls, role_id: int = None):
        """ 角色权限缓存删除 """
        if role_id:
            await RedisUtil.hDel(cls.perms_prefix, str(role_id))
        else:
            await RedisUtil.delete(cls.perms_prefix)

    @classmethod
    async def captcha_get(cls, uuid: str, ip: str) -> str:
        """ 验证码缓存读取 """
        key = cls.captcha_prefix + ToolsUtil.make_md5_str(uuid, ip)
        return await RedisUtil.get(key)

    @classmethod
    async def captcha_set(cls, ip: str, code: str):
        """ 验证码缓存写入 """
        uuid = ToolsUtil.make_token(ip)
        key = cls.captcha_prefix + ToolsUtil.make_md5_str(uuid, ip)
        await RedisUtil.set(key, code.lower(), cls.captcha_ttl)
        return uuid

    @classmethod
    async def captcha_del(cls, ip: str, code: str):
        """ 验证码缓存删除 """
        uuid = ToolsUtil.make_token(ip)
        key = cls.captcha_prefix + ToolsUtil.make_md5_str(uuid, ip)
        await RedisUtil.delete(key, code)
