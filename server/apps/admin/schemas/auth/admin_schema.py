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
from typing import Union, List, Any
from fastapi import Query
from pydantic import BaseModel, Field


class AuthAdminSearchIn(BaseModel):
    """ 管理员搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    username: Union[str, None] = Query(default=None, description="登录账号")
    mobile: Union[str, None] = Query(default=None, description="联系电话")
    role: Union[int, str, None] = Query(default=None, description="所属角色")


class AuthAdminDetailIn(BaseModel):
    """ 管理员详情参数 """
    id: int = Query(..., gt=0, description="管理员ID")


class AuthAdminAddIn(BaseModel):
    """ 管理员新增参数 """
    role_id: int = Field(..., gt=0, description="所属角色")
    dept_id: int = Field(ge=0, default=0, description="所属部门")
    post_id: int = Field(ge=0, default=0, description="所属岗位")
    nickname: str = Field(..., min_length=2, max_length=20, description="用户昵称")
    username: str = Field(..., min_length=4, max_length=20, description="登录账号")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")
    avatar: str = Field(..., min_length=1, max_length=250, description="用户头像")
    mobile: str = Field(default="", description="联系电话")
    email: str = Field(default="", description="电子邮箱")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "role_id.missing": "请选择所属角色",
            "role_id.gt": "所属角色选择异常",
            "dept_id.ge": "所属部门选择异常",
            "post_id.ge": "所属岗位选择异常",
            "nickname.min_length": "用户昵称不能少于2个字符",
            "nickname.max_length": "用户昵称不能超出20个字符",
            "username.min_length": "登录账号不能少于4个字符",
            "username.max_length": "登录账号不能超出20个字符",
            "password.min_length": "登录密码不能少于6位数",
            "password.max_length": "登录密码不能大于20位数",
            "avatar.min_length": "请上传用户头像",
            "avatar.max_length": "用户头像链接不能超出250个字符",
            "is_disable.ge": "管理员状态非合法值: [0, 1]",
            "is_disable.le": "管理员状态非合法值: [0, 1]"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "role_id": 1,
                "dept_id": 0,
                "post_id": 0,
                "nickname": "admin",
                "username": "admin",
                "password": "123456",
                "avatar": "https://www.xxx.com/avatar.png",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "is_disable": 0
            }
        }


class AuthAdminEditIn(BaseModel):
    """ 管理员编辑参数 """
    id: int = Field(..., gt=0, description="管理员ID")
    role_id: int = Field(..., gt=0, description="所属角色")
    dept_id: int = Field(ge=0, default=0, description="所属部门")
    post_id: int = Field(ge=0, default=0, description="所属岗位")
    nickname: str = Field(..., min_length=2, max_length=10, description="用户昵称")
    username: str = Field(..., min_length=4, max_length=20, description="登录账号")
    password: str = Field(max_length=20, default="", description="登录密码")
    avatar: str = Field(..., min_length=1, max_length=250, description="用户头像")
    mobile: str = Field(default="", description="联系电话")
    email: str = Field(default="", description="电子邮箱")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return AuthAdminAddIn.messages()

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "role_id": 0,
                "dept_id": 0,
                "post_id": 0,
                "nickname": "admin",
                "username": "admin",
                "password": "123456",
                "avatar": "https://www.xxx.com/avatar.png",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "is_disable": 0
            }
        }


class AuthAdminDeleteIn(BaseModel):
    """ 管理员删除参数 """
    id: int = Field(gt=0, description="管理员ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


class AuthAdminInfoIn(BaseModel):
    """ 管理员信息参数 """
    avatar: str = Field(..., min_length=1, max_length=250, description="头像")
    nickname: str = Field(..., min_length=2, max_length=10, description="用户昵称")
    mobile: str = Field(pattern=r"^(1[3-9]\d{9})?$", default="", description="联系电话")
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$", default="", description="电子邮箱")
    password: str = Field(max_length=20, default="", description="新密码")
    password_old: str = Field(max_length=20, default="", description="旧密码")

    @classmethod
    def messages(cls):
        return {
            "avatar.min_length": "请设置头像",
            "avatar.max_length": "头像链接不能超出250个字符",
            "nickname.min_length": "用户昵称不能少于2个字符",
            "nickname.max_length": "用户昵称不能超出10个字符",
            "password.max_length": "新密码不能超出20个字符",
            "password_old.max_length": "旧密码错误了",
            "mobile.pattern": "联系电话格式不正确",
            "email.pattern": "电子邮箱格式不正确"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "avatar": "https://xx.cn/avatar.png",
                "nickname": "wait",
                "password": "123456",
                "password_old": "025365",
                "mobile": "13800138000",
                "email": "13800138000@163.com"
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class AuthAdminListVo(BaseModel):
    """ 管理员列表Vo """
    id: int = Field(description="管理员ID")
    role: str = Field(description="所属角色")
    dept: str = Field(description="所属部门")
    avatar: str = Field(description="用户头像")
    nickname: str = Field(description="用户昵称")
    username: str = Field(description="登录账号")
    mobile: str = Field(description="联系电话")
    email: str = Field(description="电子邮箱")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    last_login_ip: str = Field(description="最后登录IP")
    last_login_time: str = Field(description="最后登录时间")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "role": "auditor",
                "dept": "microsoft",
                "avatar": "https://xx.cn/avatar.png",
                "nickname": "admin",
                "username": "admin",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "is_disable": 0,
                "last_login_time": "2024-07-02 11:02:00",
                "create_time": "2023-11-08 10:19:19",
                "update_time": "2024-06-30 17:35:24"
            }
        }


class AuthAdminDetailVo(BaseModel):
    """ 管理员详情Vo """
    id: int = Field(description="管理员ID")
    role_id: int = Field(description="所属角色")
    dept_id: int = Field(description="所属部门")
    post_id: int = Field(description="所属岗位")
    avatar: str = Field(description="用户头像")
    nickname: str = Field(description="用户昵称")
    username: str = Field(description="登录账号")
    mobile: str = Field(description="联系电话")
    email: str = Field(description="电子邮箱")
    role: str = Field(default="", description="角色名称")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "role_id": 1,
                "dept_id": 0,
                "post_id": 0,
                "avatar": "https://xx.cn/avatar.png",
                "nickname": "admin",
                "username": "admin",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "role": "super",
                "is_disable": 0
            }
        }


class AuthAdminOneselfVo(BaseModel):
    """ 管理员自身Vo """
    user: AuthAdminDetailVo = Field(description="管理员信息")
    perms: List[str] = Field(description="权限集合: [['*']=>所有权限, ['article:add']=>部分权限]")
    menus: Any = Field(default=[], description="权限菜单")

    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "id": 1,
                    "role_id": 1,
                    "dept_id": 0,
                    "post_id": 0,
                    "avatar": "https://xx.cn/avatar.png",
                    "nickname": "admin",
                    "username": "admin",
                    "mobile": "13800138000",
                    "email": "13800138000@163.com",
                    "is_disable": 0
                },
                "perms": ["*"],
                "menus": []
            }
        }
