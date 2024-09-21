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


class AttachModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    uid = fields.IntField(null=False, default=0, description="用户ID")
    cid = fields.IntField(null=False, default=0, description="分类ID")
    file_type = fields.IntField(null=False, default=0, description="文件类型: [10=图片, 20=视频, 30=压缩, 40=文件]")
    file_name = fields.CharField(null=False, max_length=200, default="", description="文件名称")
    file_path = fields.CharField(null=False, max_length=200, default="", description="文件路径")
    file_ext = fields.CharField(null=False, max_length=100, default="", description="文件扩展")
    file_size = fields.IntField(null=False, default=0, description="文件大小")
    is_user = fields.SmallIntField(null=False, default=0, description="用户上传: [0=否, 1=是]")
    is_attach = fields.SmallIntField(null=False, default=0, description="仓库附件: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "附件文件表"
        table = DbModel.table_prefix("attach")


class AttachCateModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    type = fields.IntField(null=False, default=0, description="分类类型: [10=图片, 20=视频, 30=压缩, 40=文件]")
    name = fields.CharField(null=False, max_length=20, default="", description="分类名称")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "附件类目表"
        table = DbModel.table_prefix("attach_cate")

