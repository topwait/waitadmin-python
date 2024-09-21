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
from tortoise.queryset import Q
from pydantic import TypeAdapter
from exception import AppException
from apps.api.schemas import login_schema as schema
from apps.api.widgets.user_widget import UserWidget
from apps.api.cache.wechat_cache import WechatCache
from common.enums.notice import NoticeEnum
from common.models.users import UserModel
from common.utils.tools import ToolsUtil
from plugins.msg.driver import MsgDriver
from plugins.safe.driver import SecurityDriver
from plugins.wechat.service import WechatService


class LoginService:
    """ 登录服务类 """

    @classmethod
    async def register(cls, post: schema.RegisterIn, terminal: int) -> schema.LoginTokenVo:
        """
        注册账号

        Args:
            post (schema.RegisterIn): 注册的参数
            terminal (int): 终端号

        Returns:
            schema.LoginTokenVo: 登录令牌Vo

        Author:
            zero
        """
        notice_code: int = NoticeEnum.MOBILE_REG if post.scene == "mobile" else NoticeEnum.EMAIL_REG
        field_value: str = "mobile" if post.scene == "mobile" else "email"

        # 验证编码
        if not await MsgDriver.check_code(notice_code, post.code):
            raise AppException("验证码错误")

        # 创建账号
        user_id: int = await UserWidget.create_user({
            f"{field_value}": post.account,
            "password": post.password,
            "terminal": terminal
        })

        # # 授权令牌
        token: str = await UserWidget.gran_token(user_id, terminal)
        return schema.LoginTokenVo(token=token)

    @classmethod
    async def account_login(cls, account: str, password: str, terminal: int) -> schema.LoginTokenVo:
        """
        账号登录

        Args:
            account (str): 登录账号
            password (str): 登录密码
            terminal (int): 终端号

        Returns:
            schema.LoginTokenVo: 登录令牌Vo

        Author:
            zero
        """
        # 查询账号
        user = await (UserModel
                      .filter(Q(account=account) | Q(mobile=account) | Q(email=account))
                      .filter(is_delete=0)
                      .first())

        # 验证账号
        if user is None:
            raise AppException("账号不存在")

        # 验证密码
        password = ToolsUtil.make_md5_str(password, user.salt)
        if user.password != password:
            raise AppException("账号或密码错误")

        # 验证状态
        if user.is_disable:
            raise AppException("账号已被禁用")

        # 授权令牌
        token: str = await UserWidget.gran_token(user.id, terminal)
        return schema.LoginTokenVo(token=token)

    @classmethod
    async def mobile_login(cls, mobile: str, code: str, terminal: int) -> schema.LoginTokenVo:
        """
        短信登录

        Args:
            mobile (str): 登录的手机号
            code (str): 短信验证码
            terminal (int): 终端号

        Returns:
            schema.LoginTokenVo: 登录令牌Vo

        Author:
            zero
        """
        # 短信验证
        if not MsgDriver.check_code(NoticeEnum.LOGIN, code):
            raise AppException("验证码错误")

        # 查询账号
        user = await UserModel.filter(mobile=mobile, is_delete=0).first()

        # 验证账号
        if not user:
            raise AppException("账号不存在")

        # 验证状态
        if user.is_disable:
            raise AppException("账号已被禁用")

        # 授权令牌
        token: str = await UserWidget.gran_token(user.id, terminal)
        return schema.LoginTokenVo(token=token)

    @classmethod
    async def oa_login(cls, state: str, code: str, terminal: int) -> schema.LoginTokenVo:
        """
        微信公众号登录

        Returns:
            schema.LoginTokenVo: 登录令牌Vo

        Author:
            zero
        """
        # 密钥检测
        result = await WechatCache.login_scan_get(state)
        if not result or result.get("status") != WechatCache.SCAN_STATUS_ING:
            await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_FAIL)
            raise AppException("登录信息已失效")

        # 获取授权
        try:
            response = await WechatService.oa_auth2_session(code)
        except Exception as e:
            raise AppException(str(e))

        # 验证账号
        user = await UserWidget.openid_user(response["openid"])
        if not user:
            user_id = await UserWidget.create_user(response)
        else:
            user_id = await UserWidget.update_user(response)

        # 授权令牌
        token: str = await UserWidget.gran_token(user_id, terminal)
        await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_OK, token)
        return schema.LoginTokenVo(token=token)

    @classmethod
    async def qrcode(cls, event: str) -> schema.LoginQrcodeVo:
        """
        微信公众号登录二维码

        Returns:
            schema.LoginQrcodeVo: 公众号登录二维码Vo

        Author:
            zero
        """
        try:
            state: str = ToolsUtil.make_token()
            await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_STAY)
            result = await WechatService.oa_build_qr_code(code=state, event=event)
            return TypeAdapter(schema.LoginQrcodeVo).validate_python(result)
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def ticket(cls, state: str) -> schema.LoginTicketVo:
        """
        检测是否扫码成功

        Args:
            state (str): key

        Returns:
            schema.LoginTicketVo: 扫码信息Vo

        Author:
            zero
        """
        result = await WechatCache.login_scan_get(state)
        if result is None:
            return schema.LoginTicketVo(status=-1)
        elif (
                result.get("status") == WechatCache.SCAN_STATUS_FAIL or
                result.get("status") == WechatCache.SCAN_STATUS_OK
        ):
            await WechatCache.login_scan_del(state)

        return schema.LoginTicketVo(
            status=int(result.get("status")),
            expire=int(result.get("expire")),
            token=result.get("token", "")
        )

    @classmethod
    async def logout(cls, token: str):
        """
        退出登录

        Args:
            token (str): 令牌

        Author:
            zero
        """
        await SecurityDriver.module("api").logout_by_token(token)
