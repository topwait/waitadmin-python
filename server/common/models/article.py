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


class ArticleModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    cid = fields.IntField(null=False, default=0, description="类目")
    title = fields.CharField(null=False, max_length=100, default="", description="标题")
    image = fields.CharField(null=False, max_length=200, default="", description="封面")
    intro = fields.CharField(null=False, max_length=200, default="", description="简介")
    content = fields.TextField(description="内容")
    browse = fields.IntField(null=False, default=0, description="浏览")
    collect = fields.IntField(null=False, default=0, description="收藏")
    sort = fields.IntField(null=False, default=0, description="排序")
    is_topping = fields.SmallIntField(null=False, default=0, description="是否置顶: [0=否, 1=是]")
    is_recommend = fields.SmallIntField(null=False, default=0, description="是否推荐: [0=否, 1=是]")
    is_show = fields.SmallIntField(null=False, default=0, description="是否显示: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "文章内容表"
        table = DbModel.table_prefix("article")


class ArticleCategoryModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    name = fields.CharField(null=False, max_length=20, default="", description="类目名称")
    sort = fields.IntField(null=False, default=0, description="类目排序")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "文章分类表"
        table = DbModel.table_prefix("article_category")


class ArticleCollectModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    user_id = fields.IntField(null=False, default=0, description="用户ID")
    article_id = fields.IntField(null=False, default=0, description="文章ID")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "文章收藏表"
        table = DbModel.table_prefix("article_collect")
