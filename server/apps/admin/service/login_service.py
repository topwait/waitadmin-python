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
import time
from typing import List
from fastapi import Request
from exception import AppException
from common.utils.urls import UrlUtil
from common.utils.tools import ToolsUtil
from common.models.auth import AuthAdminModel
from plugins.captcha.src import b64_captcha
from apps.admin.cache.login_cache import LoginCache
from apps.admin.schemas import login_schema as schema
from apps.admin.config import AdminConfig


class LoginService:
    """ 登录服务类 """

    @classmethod
    async def captcha(cls, client_ip: str) -> schema.LoginCaptchaVo:
        """
        取登录验证码图

        Args:
            client_ip (str): 请求客户端的IP。

        Returns:
            LoginCaptchaVo: 验证码信息Vo。

        Author:
            zero
        """
        base64, code = b64_captcha()
        uuid = await LoginCache.captcha_set(client_ip, code)
        return schema.LoginCaptchaVo(
            uuid=uuid,
            image=base64
        )

    @classmethod
    async def check(cls, request: Request, post: schema.LoginCheckIn) -> schema.LoginSuccessVo:
        """
        登录系统

        Args:
            request (Request): 请求对象,包含客户端信息。
            post (LoginCheckIn): 登录验证输入对象,包含用户名和密码。

        Returns:
            LoginSuccessVo: 登录成功的响应对象,包含生成的令牌。

        Author:
            zero
        """
        # 检查验证码
        if AdminConfig.enable_captcha:
            client_ip = request.client.host
            code = await LoginCache.captcha_get(post.uuid, client_ip)
            await LoginCache.captcha_del(post.uuid, client_ip)
            if not code or code != post.code.lower():
                raise AppException("验证码错误")

        # 账户查询
        admin = await AuthAdminModel.filter(username=post.username, is_delete=0).first()

        # 账户验证
        if not admin:
            raise AppException("用户名或密码错误")

        # 账户密码
        password = ToolsUtil.make_md5_str(post.password, admin.salt)
        if admin.password != password:
            raise AppException("用户名或密码错误")

        # 账户禁用
        if admin.is_disable:
            raise AppException("账户已被禁止登录")

        # 账户更新
        admin.last_login_ip = request.client.host
        admin.last_login_time = int(time.time())
        await admin.save()

        # 返回信息
        token = await LoginCache.login(admin.id, admin.role_id)
        return schema.LoginSuccessVo(
            token=token,
            username=admin.username,
            nickname=admin.nickname,
            avatar=await UrlUtil.to_absolute_url(admin.avatar)
        )

    @classmethod
    async def logout(cls, token: str):
        """
        退出登录

        Args:
            token (str): 用户登录时生成的令牌字符串。

        Returns:
            None: 该函数不返回任何值,仅执行删除操作。

        Author:
            zero
        """
        _array: List[str] = token.split(" ")
        _token: str = _array[len(_array)-1]
        await LoginCache.logout(_token)
