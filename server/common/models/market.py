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
from tortoise import fields
from kernels.model import DbModel


class RechargeOrderModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    user_id = fields.IntField(null=False, default=0, description="用户ID")
    order_sn = fields.CharField(null=False, max_length=64, default="", description="订单编号")
    terminal = fields.SmallIntField(null=False, default=0, description="来源平台: [1=微信小程序, 2=微信公众号, 3=H5, 4=PC, 5=安卓, 5=苹果]")
    pay_way = fields.SmallIntField(null=False, default=0, description="支付方式: [2=微信支付，3=支付宝支付]")
    pay_status = fields.SmallIntField(null=False, default=0, description="支付状态: [0=待支付，1=已支付]")
    package_id = fields.IntField(null=False, default=0, description="充值套餐")
    transaction_id = fields.CharField(null=False, max_length=64, default="", description="支付流水号")
    paid_amount = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="充值金额")
    give_amount = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="赠送金额")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    pay_time = fields.IntField(null=False, default=0, description="支付时间")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "充值订单表"
        table = DbModel.table_prefix("recharge_order")


class RechargePackageModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    name = fields.CharField(null=False, max_length=100, default="", description="套餐名称")
    money = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="充值金额")
    give_money = fields.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, description="赠送金额")
    sort = fields.IntField(null=False, default=0, description="排序编号")
    is_show = fields.SmallIntField(null=False, default=0, description="是否显示: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "充值套餐表"
        table = DbModel.table_prefix("recharge_package")
