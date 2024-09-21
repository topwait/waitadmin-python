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
from decimal import Decimal
from pydantic import TypeAdapter
from exception import AppException
from hypertext import PagingResult
from tortoise.transactions import in_transaction
from apps.admin.schemas.users import user_schema as schema
from common.enums.client import ClientEnum
from common.enums.gender import GenderEnum
from common.enums.wallet import WalletEnum
from common.utils.urls import UrlUtil
from common.utils.times import TimeUtil
from common.utils.tools import ToolsUtil
from common.utils.valid import ValidUtils
from common.models.users import UserModel
from common.models.users import UserGroupModel
from common.models.users import UserWalletModel
from common.models.auth import AuthAdminModel
from plugins.safe.driver import SecurityDriver


class UserService:
    """ 用户服务类 """

    @classmethod
    async def sessions(cls, params: schema.UserSessionIn) -> PagingResult[schema.UserSessionListVo]:
        """
        会话列表。

        Args:
            params (schema.UserSessionIn): 会话搜索参数。

        Author:
            zero
        """
        init_sessions = await SecurityDriver.module("api").get_token_list(params.user_id)

        start_index = (params.page_no - 1) * params.page_size
        end_index = start_index + params.page_size
        if start_index < 0:
            start_index = 0
        if end_index > len(init_sessions):
            end_index = len(init_sessions)

        sessions = init_sessions[start_index:end_index]

        _data = []
        for item in sessions:
            tips = "在线"
            status = 1
            if item.get("kick_out"):
                tips = "踢出"
                status = 3
            elif item.get("expire_time") <= int(time.time()):
                tips = "过期"
                status = 2

            surplus_time = item.get("expire_time", 0) - int(time.time())
            surplus_time = "0(s)" if surplus_time <= 0 else str(surplus_time) + "(s)"

            _data.append(schema.UserSessionListVo(
                uuid=item["key"],
                tips=tips,
                status=status,
                device=ClientEnum.get_msg_by_code(item.get("device")),
                login_host=item["login_host"],
                surplus_time=surplus_time,
                create_time=TimeUtil.timestamp_to_date(item.get("create_time")) if item.get("create_time") else "-",
                expire_time=TimeUtil.timestamp_to_date(item.get("expire_time")) if item.get("expire_time") else "-",
                last_op_time=TimeUtil.timestamp_to_date(item.get("last_op_time")) if item.get("last_op_time") else "-",
                last_ip_address=item.get("last_ip_address", ""),
                last_ua_browser=item.get("last_ua_browser", "")
            ))

        return PagingResult.create(
            data=_data,
            total=len(init_sessions),
            page_no=params.page_no,
            page_size=params.page_size
        )

    @classmethod
    async def wallet_logs(cls, params: schema.UserWalletLogIn) -> PagingResult[schema.UserWalletLogsVo]:
        """
        余额日志。

        Args:
            params (schema.UserWalletLogIn): 余额日志搜索参数。

        Author:
            zero
        """
        _model = UserWalletModel.filter(user_id=params.user_id).order_by("-id")
        _pager = await UserWalletModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size
        )

        admins_ = {}
        admin_ids = [item["admin_id"] for item in _pager.lists if item["admin_id"]]
        if admin_ids:
            admins = await AuthAdminModel.filter(id__in=list(set(admin_ids))).all().values_list("id", "nickname")
            admins_ = {k: v for k, v in admins}

        _data = []
        for item in _pager.lists:
            _data.append(schema.UserWalletLogsVo(
                id=item["id"],
                op_user=admins_.get(item["admin_id"], ""),
                action=item["action"],
                log_sn=item["log_sn"],
                source_type=WalletEnum.get_source_type_msg(item["source_type"]),
                source_sn=item["source_sn"],
                change_amount=item["change_amount"],
                before_amount=item["before_amount"],
                after_amount=item["after_amount"],
                remarks=item["remarks"],
                create_time=item["create_time"]
            ))
        _pager.lists = _data
        return _pager

    @classmethod
    async def lists(cls, params: schema.UserSearchIn) -> PagingResult[schema.UserListVo]:
        """
        用户列表。

        Args:
            params (UserSearchIn): 用户查询参数。

        Returns:
            PagingResult[schema.UserListVo]: 用户分页列表Vo。

        Author:
            zero
        """
        fields = [
            "id", "group_id", "sn", "nickname", "avatar", "mobile",
            "email", "is_disable", "create_time", "update_time"
        ]

        where = UserModel.build_search({
            "=": ["is_disable"],
            "%like%": ["keyword@sn|nickname|mobile"],
        }, params.__dict__)

        _model = UserModel.filter(is_delete=0).filter(*where).order_by("-id")
        _pager = await UserModel.paginate(
            model=_model,
            page_no=params.page_no,
            page_size=params.page_size,
            fields=fields,
            datetime_field=["create_time", "update_time"]
        )

        groups_ = {}
        group_ids = [item["group_id"] for item in _pager.lists if item["group_id"]]
        if group_ids:
            groups = await UserGroupModel.filter(id__in=group_ids).all().values_list("id", "name")
            groups_ = {k: v for k, v in groups}

        list_vo = []
        for item in _pager.lists:
            item["group"] = groups_.get(item["group_id"], "-")
            item["email"] = item["email"] if item["email"] else "-"
            item["mobile"] = item["mobile"] if item["mobile"] else "-"
            item["avatar"] = await UrlUtil.to_absolute_url(item["avatar"])

            vo = TypeAdapter(schema.UserListVo).validate_python(item)
            list_vo.append(vo)

        _pager.lists = list_vo
        return _pager

    @classmethod
    async def detail(cls, id_: int) -> schema.UserDetailVo:
        """
        用户详情。

        Args:
            id_ (int): 用户ID。

        Returns:
            schema.UserDetailVo: 用户详情Vo。

        Author:
            zero
        """
        data = await UserModel.get(id=id_)
        result = data.__dict__
        result["gender"] = GenderEnum.get_msg_by_code(result["gender"])
        result["create_time"] = TimeUtil.timestamp_to_date(data.create_time)
        result["last_login_time"] = TimeUtil.timestamp_to_date(data.last_login_time)
        return TypeAdapter(schema.UserDetailVo).validate_python(data.__dict__)

    @classmethod
    async def edit(cls, user_id: int, field: str, value: str):
        """
        用户编辑。

        Args:
            user_id (int): 用户ID。
            field (str): 要更新的字段名。
            value (str): 要更新的字段值。

        Author:
            zero
        """
        await UserModel.filter(id=user_id, is_delete=0).get()
        if field in ["account", "nickname"]:
            await cls._update_user_field(user_id, field, value)
        elif field == "gender":
            if value not in ["0", "1", "2"]:
                raise AppException("请正确选择您的性别")
            await cls._update_user_field(user_id, field, value)
        elif field == "mobile":
            if not ValidUtils.is_mobile(value):
                raise AppException("不是合法的手机号")
            await cls._update_user_field(user_id, field, value)
        elif field == "email":
            if not ValidUtils.is_email(value):
                raise AppException("不是合法的邮箱号")
            await cls._update_user_field(user_id, field, value)
        else:
            raise AppException("字段不支持场景: [account,nickname,gender,mobile,email]")

    @classmethod
    async def blacklist(cls, user_id: int):
        """
        拉黑名单

        Args:
            user_id (int): 用户ID。

        Author:
            zero
        """
        user = await UserModel.filter(id=user_id, is_delete=0).get()
        user.is_disable = 0 if user.is_disable else 1
        user.update_time = int(time.time())
        await user.save()
        await cls.kick_out(user_id, "all")

    @classmethod
    async def change_group(cls, user_id: int, group_id: int):
        """
        分组修改。

        Args:
            user_id (int): 用户ID。
            group_id (int): 分组ID。

        Author:
            zero
        """
        user = await UserModel.filter(id=user_id, is_delete=0).get()
        if group_id:
            group = await UserGroupModel.filter(id=group_id, is_delete=0).first()
            if not group:
                raise AppException("分组不存在")

        user.group_id = group_id
        user.update_time = int(time.time())
        await user.save()

    @classmethod
    async def reset_password(cls, user_id: int, new_password: str):
        """
        重置密码。

        Args:
            user_id (int): 用户ID。
            new_password (str): 新密码。

        Author:
            zero
        """
        await UserModel.filter(id=user_id, is_delete=0).get()

        salt, password = ToolsUtil.make_md5_pwd(new_password)
        await UserModel.filter(id=user_id).update(
            salt=salt,
            password=password,
            update_time=int(time.time())
        )
        await cls.kick_out(user_id, "all")

    @classmethod
    async def adjust_account(cls, user_id: int, action: str, amount: Decimal):
        """
        调整账户。

        Args:
            user_id (int): 用户ID。
            action (str): 变动类型: [inc,dec,final]。
            amount (Decimal): 变动金额。

        Author:
            zero
        """
        user = await UserModel.filter(id=user_id, is_delete=0).get()

        async with in_transaction("mysql"):
            if action == "inc":
                await UserModel.filter(id=user_id).update(balance=(user.balance + amount))
                await UserWalletModel.inc(user_id=user_id, source_type=WalletEnum.UM_INC_ADMIN, change_amount=amount)
            elif action == "dec":
                if not (user.balance - amount):
                    raise AppException("当前余额不足以扣减")
                await UserModel.filter(id=user_id).update(balance=(user.balance - amount))
                await UserWalletModel.dec(user_id=user_id, source_type=WalletEnum.UM_DEC_ADMIN, change_amount=amount)
            elif action == "final":
                if user.balance == amount:
                    raise AppException("金额没有任何变动哦")
                elif user.balance < amount:
                    await UserModel.filter(id=user_id).update(balance=(user.balance - amount))
                    await UserWalletModel.inc(user_id=user_id, source_type=WalletEnum.UM_INC_ADMIN, change_amount=amount)
                elif user.balance > amount:
                    await UserModel.filter(id=user_id).update(balance=(user.balance - amount))
                    await UserWalletModel.dec(user_id=user_id, source_type=WalletEnum.UM_DEC_ADMIN, change_amount=amount)

    @classmethod
    async def kick_out(cls, user_id: int, uuid_: str):
        """
        强制下线。

        Args:
            user_id (int): 用户ID。
            uuid_ (str): 登录标识。

        Author:
            zero
        """
        if uuid_ == "all":
            await SecurityDriver.module("api").logout(user_id)
        else:
            sessions = await SecurityDriver.module("api").get_token_list(user_id)
            for item in sessions:
                if item["key"] == uuid_:
                    await SecurityDriver.module("api").logout_by_token(item["value"])
                    break

    @classmethod
    async def _update_user_field(cls, user_id: int, field: str, value: str):
        """
        更新用户字段的通用方法。

        Args:
            user_id (int): 用户ID。
            field (str): 要更新的字段名。
            value (str): 要更新的字段值。

        Author:
            zero
        """
        _lang = {"account": "登录账号", "nickname": "用户昵称", "mobile": "手机号", "email": "邮箱号"}
        if field == "account" or field == "nickname":
            if len(value) < 4:
                raise AppException(f"{_lang[field]}长度不能少于4个字符")
            if len(value) > 20:
                raise AppException(f"{_lang[field]}长度不能大于20个字符")

            user = await UserModel.filter(id__not=user_id, **{field: value}, is_delete=0).first()
            if user:
                raise AppException(f"该{_lang[field]}已被占用了")

        await UserModel.filter(id=user_id).update(**{field: value, "update_time": int(time.time())})
