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


class AuthAdminModel(DbModel):
    id = fields.IntField(pk=True, unsigned=True, description="主键")
    role_id = fields.IntField(null=False, default=0, description="角色主键")
    dept_id = fields.IntField(null=False, default=0, description="部门主键")
    post_id = fields.IntField(null=False, default=0, description="岗位主键")
    nickname = fields.CharField(null=False, max_length=32, default="", description="账号昵称")
    username = fields.CharField(null=False, max_length=32, default="", description="登录账号")
    password = fields.CharField(null=False, max_length=32, default="", description="登录密码")
    salt = fields.CharField(null=False, max_length=32, default="", description="加密盐巴")
    avatar = fields.CharField(null=False, max_length=200, default="", description="用户头像")
    mobile = fields.CharField(null=False, max_length=100, default="", description="用户电话")
    email = fields.CharField(null=False, max_length=100, default="", description="电子邮箱")
    last_login_ip = fields.CharField(null=False, max_length=100, default="", description="登录地址")
    last_login_time = fields.IntField(null=False, default=0, description="登录时间")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "管理员的表"
        table = DbModel.table_prefix("auth_admin")


class AuthRoleModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    name = fields.CharField(null=False, max_length=20, default="", description="角色名称")
    describe = fields.CharField(null=False, max_length=200, default="", description="角色描述")
    sort = fields.IntField(null=False, default=0, description="角色排序")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "角色管理表"
        table = DbModel.table_prefix("auth_role")


class AuthMenuModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    pid = fields.IntField(null=False, default=0, description="菜单父级")
    type = fields.CharField(null=False, max_length=1, default="", description="权限类型: [M=目录, C=菜单, A=按钮]")
    name = fields.CharField(null=False, max_length=100, default="", description="菜单名称")
    icon = fields.CharField(null=False, max_length=100, default="", description="菜单图标")
    sort = fields.IntField(null=False, default=0, description="菜单排序")
    perms = fields.CharField(null=False, max_length=100, default="", description="菜单权限")
    params = fields.CharField(null=False, max_length=200, default="", description="路由参数")
    component = fields.CharField(null=False, max_length=200, default="", description="组件路径")
    path = fields.CharField(null=False, max_length=200, default="", description="页面路径")
    is_show = fields.SmallIntField(null=False, default=0, description="是否显示: [0=否, 1=是]")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "菜单管理表"
        table = DbModel.table_prefix("auth_menu")


class AuthPermModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    role_id = fields.IntField(null=False, default=0, description="角色主键")
    menu_id = fields.IntField(null=False, default=0, description="菜单主键")

    class Meta:
        table_description = "权限管理表"
        table = DbModel.table_prefix("auth_perm")


class AuthDeptModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    pid = fields.IntField(null=False, default=0, description="上级主键")
    name = fields.CharField(null=False, max_length=100, default="", description="部门名称")
    duty = fields.CharField(null=False, max_length=30, default="", description="负责人名")
    mobile = fields.CharField(null=False, max_length=30, default="", description="部门电话")
    sort = fields.IntField(null=False, default=0, description="排序编号")
    level = fields.IntField(null=False, default=0, description="关系层级")
    relation = fields.CharField(null=False, max_length=500, default="", description="关系链条")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "部门管理表"
        table = DbModel.table_prefix("auth_dept")


class AuthPostModel(DbModel):
    id = fields.IntField(pk=True, description="主键")
    code = fields.CharField(null=False, max_length=30, default="", description="岗位编码")
    name = fields.CharField(null=False, max_length=30, default="", description="岗位名称")
    remarks = fields.CharField(null=False, max_length=200, default="", description="岗位备注")
    sort = fields.IntField(null=False, default=0, description="岗位排序")
    is_disable = fields.SmallIntField(null=False, default=0, description="是否禁用: [0=否, 1=是]")
    is_delete = fields.SmallIntField(null=False, default=0, description="是否删除: [0=否, 1=是]")
    create_time = fields.IntField(null=False, default=0, description="创建时间")
    update_time = fields.IntField(null=False, default=0, description="更新时间")
    delete_time = fields.IntField(null=False, default=0, description="删除时间")

    class Meta:
        table_description = "岗位管理表"
        table = DbModel.table_prefix("auth_post")

