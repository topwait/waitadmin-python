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


class DevBannerModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    position = fields.SmallIntField(null=False, default=0, description="轮播位置")
    title = fields.CharField(null=False, max_length=200, default="", description="轮播标题")
    image = fields.CharField(null=False, max_length=250, default="", description="轮播图片")
    target = fields.CharField(null=False, max_length=250, default="", description="跳转方式")
    url = fields.CharField(null=False, max_length=250, default="", description="跳转链接")
    sort = fields.IntField(null=False, default=0, description="排序编号")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "轮播管理表"
        table = DbModel.table_prefix("dev_banner")


class DevLinksModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    title = fields.CharField(null=False, max_length=200, default="", description="友链名称")
    image = fields.CharField(null=False, max_length=250, default="", description="友链图标")
    target = fields.CharField(null=False, max_length=250, default="", description="跳转方式")
    url = fields.CharField(null=False, max_length=250, default="", description="跳转链接")
    sort = fields.IntField(null=False, default=0, description="排序编号")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "友链管理表"
        table = DbModel.table_prefix("dev_links")


class DevPayConfigModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    channel = fields.SmallIntField(null=False, default=0, description="渠道编号: [1=余额,2=微信,3=支付宝]")
    shorter = fields.CharField(null=False, max_length=32, default="", description="简写名称")
    name = fields.CharField(null=False, max_length=32, default="", description="渠道名称")
    logo = fields.CharField(null=False, max_length=250, default="", description="渠道图标")
    icon = fields.CharField(null=False, max_length=250, default="", description="支付图标")
    params = fields.TextField(default="", description="支付配置")
    sort = fields.IntField(null=False, default=0, description="排序编号")
    status = fields.SmallIntField(null=False, default=0, description="渠道状态: [0=禁用, 1=启用]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")

    class Meta:
        table_description = "支付配置表"
        table = DbModel.table_prefix("dev_pay_config")
