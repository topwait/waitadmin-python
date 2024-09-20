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
from tortoise import fields
from kernels.model import DbModel
from common.utils.tools import ToolsUtil


class UserModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    group_id = fields.IntField(null=False, default=0, description="用户分组")
    sn = fields.CharField(null=False, max_length=20, default="", description="用户编号")
    account = fields.CharField(null=False, max_length=32, default="", description="用户账号")
    password = fields.CharField(null=False, max_length=32, default="", description="登录密码")
    nickname = fields.CharField(null=False, max_length=32, default="", description="用户名称")
    avatar = fields.CharField(null=False, max_length=200, default="", description="用户头像")
    salt = fields.CharField(null=False, max_length=32, default="", description="加密盐巴")
    gender = fields.IntField(null=False, default=0, description="用户性别")
    mobile = fields.CharField(null=False, max_length=20, default="", description="手机号码")
    email = fields.CharField(null=False, max_length=100, default="", description="电子邮箱")
    balance = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="钱包余额")
    last_login_ip = fields.CharField(null=False, max_length=100, default="", description="最后登录IP")
    last_login_time = fields.IntField(null=False, default=0, description="最后登录时间")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "用户管理表"
        table = DbModel.table_prefix("user")


class UserAuthModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    user_id = fields.IntField(null=False, default=0, description="用户ID")
    openid = fields.CharField(null=False, max_length=32, default="", description="openid")
    unionid = fields.CharField(null=False, max_length=32, default="", description="unionid")
    terminal = fields.IntField(null=False, default=0, description="客户端[1=微信小程序, 2=微信公众号, 3=安卓, 4=苹果]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")

    class Meta:
        table_description = "用户授权表"
        table = DbModel.table_prefix("user_auth")


class UserGroupModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    name = fields.CharField(null=False, max_length=30, default="", description="名称")
    remarks = fields.CharField(null=False, max_length=200, default="", description="备注")
    sort = fields.IntField(null=False, default=0, description="排序")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "用户分组表"
        table = DbModel.table_prefix("user_group")


class UserWalletModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    admin_id = fields.IntField(null=False, default=0, description="管理ID")
    user_id = fields.IntField(null=False, default=0, description="用户ID")
    log_sn = fields.CharField(null=False, max_length=64, default="", description="日志编号")
    action = fields.IntField(null=False, default=0, description="变动类型: [1=增加， 2=减少]")
    source_type = fields.IntField(null=False, default=0, description="来源类型")
    source_id = fields.IntField(null=False, default=0, description="来源主键")
    source_sn = fields.CharField(null=False, max_length=64, default="", description="来源单号")
    change_amount = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="变动金额: [增加多少钱 / 减少多少钱]")
    before_amount = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="变动前金额")
    after_amount = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="变动后金额")
    remarks = fields.CharField(null=False, max_length=200, default="", description="备注")
    create_time = fields.IntField(null=False, default=0, description="创建时间")

    class Meta:
        table_description = "用户余额表"
        table = DbModel.table_prefix("user_wallet")

    @classmethod
    async def inc(cls, user_id: int, source_type: int, change_amount: Decimal, **kwargs):
        user = await UserModel.filter(id=user_id).first()
        left_amount = user.balance
        await cls.create(
            action=1,
            log_sn=await ToolsUtil.make_order_sn(cls, "log_sn"),
            admin_id=kwargs.get("admin_id", 0),
            user_id=user_id,
            source_type=source_type,
            source_id=kwargs.get("source_id", 0),
            source_sn=kwargs.get("source_sn", ""),
            change_amount=change_amount,
            before_amount=left_amount - change_amount,
            after_amount=left_amount,
            remarks=kwargs.get("remarks", ""),
            create_time=int(time.time())
        )

    @classmethod
    async def dec(cls, user_id: int, source_type: int, change_amount: Decimal, **kwargs):
        user = await UserModel.filter(id=user_id).first()
        left_amount = user.balance
        await cls.create(
            action=2,
            log_sn=await ToolsUtil.make_order_sn(cls, "log_sn"),
            admin_id=kwargs.get("admin_id", 0),
            user_id=user_id,
            source_type=source_type,
            source_id=kwargs.get("source_id", 0),
            source_sn=kwargs.get("source_sn", ""),
            change_amount=change_amount,
            before_amount=left_amount + change_amount,
            after_amount=left_amount,
            remarks=kwargs.get("remarks", ""),
            create_time=int(time.time())
        )


class UserVisitorModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    user_id = fields.IntField(null=False, default=0, description="用户ID")
    terminal = fields.SmallIntField(null=False, default=0, description="客户端")
    summary = fields.CharField(null=False, max_length=100, default="", description="摘要信息")
    endpoint = fields.CharField(null=False, max_length=300, default="", description="请求函数")
    method = fields.CharField(null=False, max_length=30, default="", description="请求方法: [GET,POST]")
    url = fields.CharField(null=False, max_length=100, default="", description="请求路由")
    ip = fields.CharField(null=False, max_length=100, default="", description="请求IP")
    ua = fields.CharField(null=False, max_length=100, default="", description="请求UA")
    user_agent = fields.CharField(null=False, max_length=900, default="", description="UA详情")
    params = fields.TextField(default="", description="请求参数")
    error = fields.TextField(default="", description="错误信息")
    status = fields.SmallIntField(null=False, default=1, description="执行状态: [1=成功, 2=失败]")
    start_time = fields.CharField(null=False, default="0", max_length=20, description="开始时间: 毫秒")
    end_time = fields.CharField(null=False, default="0", max_length=20, description="结束时间: 毫秒")
    task_time = fields.CharField(null=False, default="0", max_length=20, description="耗时时间: 毫秒")
    create_time = fields.IntField(null=False, default=0, description="操作时间")

    class Meta:
        table_description = "用户浏览表"
        table = DbModel.table_prefix("user_visitor")
