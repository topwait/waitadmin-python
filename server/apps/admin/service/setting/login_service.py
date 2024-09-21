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
from exception import AppException
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import login_schema as schema


class LoginService:
    """ 登录配置服务类 """

    @classmethod
    async def detail(cls) -> schema.LoginDetailVo:
        """
        登录配置详情。

        Returns:
            schema.LoginDetailVo: 登录配置详情Vo。

        Author:
            zero
        """
        conf = await ConfigUtil.get("login") or {}
        return schema.LoginDetailVo(
            is_agreement=int(conf.get("is_agreement", 0)),
            defaults=conf.get("defaults", "account"),
            registers=conf.get("registers", []),
            login_modes=conf.get("login_modes", []),
            login_other=conf.get("login_other", [])
        )

    @classmethod
    async def save(cls, post: schema.LoginDetailVo):
        """
        登录配置保存。

         Args:
            post (schema.LoginDetailVo): 登录配置参数。

        Author:
            zero
        """
        if post.defaults not in ["account", "mobile", "wx"]:
            raise AppException("不支持的默认登录方式: " + post.defaults)

        for item in post.registers:
            if item not in ["mobile", "email"]:
                raise AppException("不支持的允许注册方式: " + item)

        for item in post.login_modes:
            if item not in ["account", "mobile"]:
                raise AppException("不支持的通用登录方式: " + item)

        for item in post.login_other:
            if item not in ["wx"]:
                raise AppException("不支持的第三方登录: " + item)

        await ConfigUtil.set("login", "is_agreement", post.is_agreement)
        await ConfigUtil.set("login", "defaults", post.defaults)
        await ConfigUtil.set("login", "registers", json.dumps(post.registers))
        await ConfigUtil.set("login", "login_modes", json.dumps(post.login_modes))
        await ConfigUtil.set("login", "login_other", json.dumps(post.login_other))
