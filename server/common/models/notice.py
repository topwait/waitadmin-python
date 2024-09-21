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


class NoticeSetting(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    scene = fields.IntField(null=False, default=0, description="场景编码")
    name = fields.CharField(null=False, max_length=100, default="", description="场景名称")
    remarks = fields.CharField(null=False, max_length=32, default="", description="场景描述")
    variable = fields.TextField(null=False, description="场景变量")
    sys_template = fields.TextField(null=False, description="系统通知模板")
    sms_template = fields.TextField(null=False, description="短信通知模板")
    ems_template = fields.TextField(null=False, description="邮件通知模板")
    get_client = fields.SmallIntField(null=False, default=0, description="接收端口: [1=用户, 2=平台]")
    is_captcha = fields.SmallIntField(null=False, default=0, description="是验证码: [0=否的, 1=是的]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "通知设置表"
        table = DbModel.table_prefix("notice_setting")


class NoticeRecord(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    scene = fields.IntField(null=False, default=0, description="场景编码")
    user_id = fields.IntField(null=False, default=0, description="接收用户")
    account = fields.CharField(null=False, max_length=100, default="", description="接收账号")
    title = fields.CharField(null=False, max_length=100, default="", description="通知标题")
    code = fields.CharField(null=False, max_length=10, default="", description="验证编码")
    content = fields.TextField(null=False, description="通知内容")
    error = fields.TextField(null=False, description="失败原因")
    sender = fields.SmallIntField(null=False, default=0, description="发送类型: [1=系统, 2=邮件, 3=短信, 4=公众号, 5=小程序]")
    receiver = fields.SmallIntField(null=False, default=0, description="接收对象: [1=用户, 2=平台]")
    status = fields.SmallIntField(null=False, default=0, description="通知状态: [0=等待, 1=成功, 2=失败]")
    is_read = fields.SmallIntField(null=False, default=0, description="已读状态: [0=未读, 1=已读]")
    is_captcha = fields.SmallIntField(null=False, default=0, description="是验证码: [0=否的, 1=是的]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    expire_time = fields.IntField(null=False, default=0, description="失效时间")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "通知记录表"
        table = DbModel.table_prefix("notice_record")
