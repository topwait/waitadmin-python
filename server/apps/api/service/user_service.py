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
from tortoise import Tortoise
from pydantic import TypeAdapter
from exception import AppException
from hypertext import PagingResult
from apps.api.schemas import user_schema as schema
from apps.api.cache.wechat_cache import WechatCache
from common.models.users import UserModel, UserAuthModel
from common.models.article import ArticleCollectModel, ArticleModel
from common.utils.urls import UrlUtil
from common.utils.times import TimeUtil
from common.utils.tools import ToolsUtil
from common.enums.notice import NoticeEnum
from common.enums.client import ClientEnum
from plugins.msg.driver import MsgDriver
from plugins.wechat.service import WechatService


class UserService:
    """ 用户服务类 """

    @classmethod
    async def center(cls, id_: int) -> schema.UserCenterVo:
        """
        用户个人中心。

        Args:
            id_ (int): 用户ID。

        Returns:
            schema.UserCenterVo: 用户资料Vo。

        Author:
            zero
        """
        user = await UserModel.filter(id=id_, is_delete=0).get()
        auth = await UserAuthModel.filter(
            user_id=user.id,
            terminal__in=[ClientEnum.MNP, ClientEnum.OA]
        ).first()

        collect = await ArticleCollectModel.filter(user_id=user.id, is_delete=0).count()

        d = user.__dict__
        d["avatar"] = await UrlUtil.to_absolute_url(user.avatar)
        d["collect"] = collect
        d["is_wechat"] = 1 if auth else 0
        d["is_password"] = 1 if user.password else 0
        d["create_time"] = TimeUtil.timestamp_to_date(user.create_time)
        d["last_login_time"] = TimeUtil.timestamp_to_date(user.last_login_time)
        return TypeAdapter(schema.UserCenterVo).validate_python(d)

    @classmethod
    async def collect(cls, user_id: int, params: schema.UserCollectSearchIn):
        offset: int = (params.page - 1) * 15

        COUNT_SQL = f"""__SELECT COUNT(*)
                        FROM `{ArticleCollectModel.Meta.table}` AS ac
                        JOIN `{ArticleModel.Meta.table}` AS a ON a.id=ac.article_id
                        WHERE ac.user_id={user_id} AND ac.is_delete=0 AND a.is_delete=0;
                    """.replace("__", "")

        QUERY_SQL = f"""__SELECT ac.`id`, a.`image`, a.`title`, a.`browse`, a.`collect`, ac.`create_time`
                       FROM `{ArticleCollectModel.Meta.table}` AS ac
                       JOIN `{ArticleModel.Meta.table}` AS a ON a.id=ac.article_id
                       WHERE ac.user_id={user_id} AND ac.is_delete=0 AND a.is_delete=0
                       ORDER BY ac.id DESC
                       LIMIT {offset}, 15;
                   """.replace("__", "")

        count = await Tortoise.get_connection("mysql").execute_query_dict(COUNT_SQL)
        lists = await Tortoise.get_connection("mysql").execute_query_dict(QUERY_SQL)

        for item in lists:
            item["image"] = await UrlUtil.to_absolute_url(item["image"])
            item["create_time"] = TimeUtil.timestamp_to_date(item["create_time"])

        _lists = [TypeAdapter(schema.UserCollectVo).validate_python(item) for item in lists]
        return PagingResult.create(_lists, count[0]["COUNT(*)"], params.page, 15)

    @classmethod
    async def edit(cls, field: str, value: str, user_id: int):
        """
        编辑用户资料。

        Args:
            field (str): 建。
            value (str): 值。
            user_id (int): 用户ID。

        Author:
            zero
        """
        if field == "account":
            user = await UserModel.filter(id__not=user_id, account=value, is_delete=0).first()
            if user:
                raise AppException("该账号已被占用")
            if len(value) < 4:
                raise AppException("账号长度不能少于4个字符")
            if len(value) > 20:
                raise AppException("账号长度不能大于20个字符")

            await UserModel.filter(id=user_id).update(account=value, update_time=int(time.time()))
        elif field == "nickname":
            user = await UserModel.filter(id__not=user_id, nickname=value, is_delete=0).first()
            if user:
                raise AppException("该昵称已被占用")
            if len(value) < 3:
                raise AppException("昵称长度不能少于4个字符")
            if len(value) > 20:
                raise AppException("昵称长度不能大于20个字符")

            await UserModel.filter(id=user_id).update(nickname=value, update_time=int(time.time()))
        elif field == "gender":
            if int(value) not in [0, 1, 2]:
                raise AppException("请正确选择您的性别")
            await UserModel.filter(id=user_id).update(gender=value, update_time=int(time.time()))
        elif field == "avatar":
            user = await UserModel.filter(id=user_id, is_delete=0).first()
            if not user:
                raise AppException("账号异常请刷新页面")
            avatar = UrlUtil.to_relative_url(value)
            await UserModel.filter(id=user_id).update(avatar=avatar, update_time=int(time.time()))
        else:
            raise AppException("不支持的场景")

    @classmethod
    async def forget_pwd(cls, code: str, mobile: str, new_pwd: str):
        """
        找回登录密码 (找回后强退账号)。

        Args:
            code (str): 验证码。
            mobile (str): 手机好。
            new_pwd (str): 新密码。

        Author:
            zero
        """
        # 短信验证
        if not MsgDriver.check_code(NoticeEnum.FORGET_PWD, code):
            raise AppException("验证码错误")

        # 查询账户
        user = await UserModel.filter(mobile=mobile, is_delete=0).first()

        # 验证账户
        if not user:
            raise AppException("账号不存在")

        # 设置密码
        salt, password = ToolsUtil.make_md5_pwd(new_pwd)
        user.salt = salt
        user.password = password
        user.update_time = int(time.time())
        await user.save()

    @classmethod
    async def change_pwd(cls, old_pwd: str, new_pwd: str, user_id: int):
        """
        修改登录密码 (修改后强退账号)。

        Args:
            old_pwd (str): 旧密码。
            new_pwd (str): 新密码。
            user_id (int): 用户ID。

        Author:
            zero
        """
        # 查询账户
        user = await UserModel.filter(id=user_id, is_delete=0).first()

        # 验证账户
        if not user:
            raise AppException("账号不存在")

        # 验证密码
        org_pwd: str = ToolsUtil.make_md5_pwd(old_pwd, user.salt)
        if org_pwd != user.password:
            raise AppException("原始密码不正确")

        # 更新密码
        salt, password = ToolsUtil.make_md5_pwd(new_pwd)
        user.salt = salt
        user.password = password
        user.update_time = int(time.time())
        await user.save()

        # 退出登录
        # todo

    @classmethod
    async def bind_wechat(cls, state: str, code: str, user_id: int, terminal: int):
        """
        绑定微信。

        Args:
            state (str): 验证密钥。
            code (str): 微信code。
            user_id (int): 用户ID。
            terminal (int): 来源终端。

        Author:
            zero
        """
        if state:
            # 扫码的状态
            cache_res = await WechatCache.login_scan_get(state)
            if cache_res is None or int(cache_res["status"]) != WechatCache.SCAN_STATUS_ING:
                raise AppException("二维码已失效,请重新扫码")
            # 公众号授权
            try:
                response = await WechatService.oa_auth2_session(code)
                openid: str = response.get("openid", "")
                unionid: str = response.get("unionid", "")
            except Exception as e:
                await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_FAIL)
                raise AppException(str(e))
        else:
            # 小程序授权
            try:
                response = await WechatService.wx_code2_session(code)
                openid: str = response.get("openid", "")
                unionid: str = response.get("unionid", "")
            except Exception as e:
                raise AppException(str(e))

        # 验证账户
        auth = await UserAuthModel.filter(
            id=user_id,
            terminal=terminal
        ).first()

        # 更新授权
        if auth.__dict__:
            await UserAuthModel.filter(id=auth.id, terminal=terminal).update(
                openid=openid,
                unionid=unionid,
                update_time=int(time.time())
            )
        else:
            await UserAuthModel.create(
                user_id=user_id,
                openid=openid,
                unionid=unionid,
                terminal=terminal,
                create_time=int(time.time()),
                update_time=int(time.time())
            )

        # 更新状态
        if state:
            await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_OK)

    @classmethod
    async def bind_mobile(cls, scene: str, mobile: str, code: str, user_id: int):
        """
        绑定手机。

        Args:
            scene (str): 操作场景: [change=变更, bind=绑定]。
            mobile (str): 手机号。
            code (str): 验证码。
            user_id (int): 用户ID。

        Author:
            zero
        """
        n_code = 0
        if scene == "code":
            # 微信验证
            result = await WechatService.wx_phone_number(code)
            mobile = result.get("phoneNumber")
        else:
            # 短信验证
            n_code = NoticeEnum.MOBILE_CHANGE if scene == "change" else NoticeEnum.MOBILE_BIND
            if not MsgDriver.check_code(n_code, code):
                raise AppException("验证码错误")

        # 查询用户
        user = await UserModel.filter(id=user_id, is_delete=0).first()

        # 验证用户
        if not user:
            raise AppException("用户不存在")

        # 验证手机
        check_mobile = await UserModel.filter(id__eq=user_id, mobile=mobile, is_delete=0).first()
        if check_mobile:
            raise AppException("手机号已被占用")

        # 更新手机
        await UserModel.filter(id=user_id).update(mobile=mobile, update_time=int(time.time()))

        # 核销验证码
        if n_code:
            await MsgDriver.verify_code(n_code, code)

    @classmethod
    async def bind_email(cls, scene: str, email: str, code: str, user_id: int):
        """
        绑定邮箱。

        Args:
            scene (str): 操作场景: [change=变更, bind=绑定]。
            email (str): 邮箱号。
            code (str): 验证码。
            user_id (int): 用户ID。

        Author:
            zero
        """
        # 验证邮箱
        n_code: int = NoticeEnum.EMAIL_CHANGE if scene == "change" else NoticeEnum.EMAIL_BIND
        if not await MsgDriver.check_code(n_code, code):
            raise AppException("验证码错误")

        # 验证用户
        user = await UserModel.filter(id=user_id, is_delete=0).first()
        if not user:
            raise AppException("用户不存在")

        # 验证邮箱
        check_email = await UserModel.filter(id__not=user_id, email=email, is_delete=0).first()
        if check_email:
            raise AppException("邮箱号已被占用")

        # 更新邮箱
        await UserModel.filter(id=user_id).update(email=email, update_time=int(time.time()))

        # 核销验证码
        await MsgDriver.verify_code(n_code, code)
