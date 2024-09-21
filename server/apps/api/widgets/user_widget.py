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
from typing import Dict
from exception import AppException
from common.utils.tools import ToolsUtil
from common.models.users import UserModel
from common.models.users import UserAuthModel
from plugins.safe.driver import SecurityDriver


class UserWidget:

    @classmethod
    async def create_user(cls, response: Dict[str, str]) -> int:
        """
        创建用户

        Args:
            response (Dict[str, str]): 用户资料

        Returns:
            int: 用户ID

        Author:
            zero
        """
        # 接收参数
        sn_code: str = await ToolsUtil.make_rand_sn(UserModel, "sn", 8)
        terminal: int = int(response.get("terminal", 0))
        avatar: str = response.get("avatarUrl", "static/images/avatar.png")
        account: str = response.get("account", "u"+sn_code)
        nickname: str = response.get("nickname", sn_code)
        password: str = response.get("password", "")
        email: str = response.get("email", "")
        mobile: str = response.get("mobile", "")
        openid: str = response.get("openid", "")
        unionid: str = response.get("unionid", "")
        gender: int = int(response.get("gender", 0))

        # 验证账号
        if account and await UserModel.filter(account=account, is_delete=0).first():
            raise AppException("账号已被占用")

        # 验证手机
        if mobile and await UserModel.filter(mobile=mobile, is_delete=0).first():
            raise AppException("手机已被占用")

        # 验证邮箱
        if email and await UserModel.filter(email=email, is_delete=0).first():
            raise AppException("邮箱已被占用")

        # 密码信息
        salt: str = ToolsUtil.make_rand_char(6)
        if password:
            password = ToolsUtil.make_md5_str(password, salt)

        try:
            # 创建用户
            user = await UserModel.create(
                sn=sn_code,
                avatar=avatar,
                mobile=mobile,
                email=email,
                account=account,
                password=password,
                nickname=nickname,
                gender=gender,
                salt=salt,
                last_login_ip="",
                last_login_time=int(time.time()),
                create_time=int(time.time()),
                update_time=int(time.time())
            )

            # 创建授权
            if openid or unionid:
                await UserAuthModel.create(
                    user_id=user.id,
                    openid=openid,
                    unionid=unionid,
                    terminal=terminal,
                    create_time=int(time.time()),
                    update_time=int(time.time())
                )

            return user.id
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def update_user(cls, response: Dict[str, str]) -> int:
        """
        更新用户

        Args:
            response (Dict[str, str]): 用户资料

        Returns:
            int: 用户ID

        Author:
            zero
        """
        # 接收参数
        user_id: int = int(response.get("user_id"))
        terminal: int = int(response.get("terminal"))
        mobile: str = response.get("mobile", "")
        openid: str = response.get("openid", "")
        unionid: str = response.get("unionid", "")

        # 查询用户
        user_info = await UserModel.filter(id=user_id, is_delete=0).first()
        user_auth = await UserAuthModel.filter(user_id=user_id, terminal=terminal).first()

        # 验证手机
        if mobile and UserModel.filter(mobile=mobile, is_delete=0, id__ne=user_id).first():
            raise AppException("手机已被占用")

        try:
            # 绑定手机
            if mobile and not user_info.mobile:
                await UserModel.filter(id=user_id).update(mobile=mobile, update_time=int(time.time()))

            # 创建授权
            if not user_auth and (openid or unionid):
                await UserAuthModel.create(
                    user_id=user_id,
                    openid=openid,
                    unionid=unionid,
                    terminal=terminal,
                    create_time=int(time.time()),
                    update_time=int(time.time())
                )

            # 更新关联
            if (user_auth and not user_auth.unionid) and unionid:
                await UserAuthModel.filter(id=user_auth.id).update(unionid=unionid, update_time=int(time.time()))

            return user_id
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def openid_user(cls, openid: str):
        """
        根据openid获取用户信息

        Args:
            openid (str): 微信的openid

        Returns:
            User: 用户信息

        Author:
            zero
        """
        auth = (await UserAuthModel
                .filter(openid=openid)
                .order_by("-id")
                .first()
                .values("id", "user_id") or {})

        user = (await UserModel
                .filter(id=auth.get("user_id", 0), is_delete=0)
                .order_by("-id")
                .first())

        if auth and not user:
            await UserAuthModel.delete(auth["id"])

        return user

    @classmethod
    async def gran_token(cls, user_id: int, terminal: int) -> str:
        """
        生成登录令牌

        Args:
            user_id (int): 用户ID
            terminal (int): 来源客户端

        Returns:
            str: token

        Author:
            zero
        """
        return await SecurityDriver.module("api").login(user_id, terminal)
