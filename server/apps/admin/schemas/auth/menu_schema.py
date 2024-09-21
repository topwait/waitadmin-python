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
from typing import List, Union
from fastapi import Query
from pydantic import BaseModel, Field


class AuthMenuDetailIn(BaseModel):
    """ 菜单详情参数 """
    id: int = Query(gt=0, description="菜单ID")


class AuthMenuAddIn(BaseModel):
    """ 菜单新增参数 """
    pid: int = Field(..., ge=0, description="上级菜单")
    type: str = Field(..., min_length=1, max_length=1, description="权限类型: [M,C,A]")
    name: str = Field(..., max_length=100, description="菜单名称")
    icon: str = Field(max_length=100, default="", description="菜单图标")
    sort: int = Field(ge=0, default=0, description="排序编号")
    perms: str = Field(max_length=200, default="", description="权限标识")
    params: str = Field(max_length=200, default="", description="路由参数")
    component: str = Field(max_length=200, default="", description="组件路径")
    path: str = Field(..., max_length=200, description="路由地址")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "pid": 1,
                "type": "C",
                "name": "菜单管理",
                "icon": "el-icon-lock",
                "sort": 0,
                "perms": "",
                "params": "",
                "component": "auth/menu/index",
                "path": "auth/menu/index",
                "is_show": 1,
                "is_disable": 0
            }
        }


class AuthMenuEditIn(BaseModel):
    """ 菜单编辑参数 """
    id: int = Field(..., gt=0, description="ID")
    pid: int = Field(..., ge=0, description="上级菜单")
    type: str = Field(..., min_length=1, max_length=1, description="权限类型: [M,C,A]")
    name: str = Field(..., max_length=100, description="菜单名称")
    icon: str = Field(max_length=100, default="", description="菜单图标")
    sort: int = Field(ge=0, default=0, description="排序编号")
    perms: str = Field(max_length=200, default="", description="权限标识")
    params: str = Field(max_length=200, default="", description="路由参数")
    component: str = Field(max_length=200, default="", description="组件路径")
    path: str = Field(..., max_length=200, description="路由地址")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 1,
                "type": "C",
                "name": "菜单管理",
                "icon": "el-icon-lock",
                "sort": 0,
                "perms": "",
                "params": "",
                "component": "auth/menu/index",
                "path": "auth/menu/index",
                "is_show": 1,
                "is_disable": 0
            }
        }


class AuthMenuDeleteIn(BaseModel):
    """ 菜单删除参数 """
    id: int = Field(..., gt=0, description="菜单ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class AuthMenuWholeVo(BaseModel):
    """ 所有菜单Vo """
    id: int = Field(description="菜单ID")
    pid: int = Field(description="父级ID")
    name: str = Field(description="权限类型: [M=目录, C=菜单, A=按钮]")
    children: Union["AuthMenuWholeVo", List, None] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "name": "Index",
                "children": []
            }
        }


class AuthMenuRoutesVo(BaseModel):
    """ 菜单路由Vo """
    id: int = Field(description="菜单ID")
    pid: int = Field(description="父级ID")
    type: str = Field(description="权限类型: [M=目录, C=菜单, A=按钮]")
    name: str = Field(description="菜单名称")
    icon: str = Field(description="菜单图标")
    perms: str = Field(description="菜单权限")
    params: str = Field(description="路由参数")
    component: str = Field(description="组件路径")
    path: str = Field(description="页面路径")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    children: Union["AuthMenuRoutesVo", List, None] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "type": "C",
                "name": "Index",
                "icon": "el-icon-house",
                "perms": "index:console",
                "params": "",
                "component": "workbench",
                "path": "workbench",
                "is_show": 1,
                "is_disable": 0,
                "children": []
            }
        }


class AuthMenuListVo(BaseModel):
    """ 菜单列表Vo """
    id: int = Field(description="菜单ID")
    pid: int = Field(description="父级ID")
    type: str = Field(description="权限类型: [M=目录, C=菜单, A=按钮]")
    name: str = Field(description="菜单名称")
    icon: str = Field(description="菜单图标")
    sort: int = Field(description="菜单排序")
    perms: str = Field(description="路由参数")
    path: str = Field(description="路径地址")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")
    children: Union["AuthMenuListVo", List, None] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "type": "C",
                "name": "Index",
                "icon": "el-icon-house",
                "sort": 9900,
                "perms": "index:console",
                "is_disable": 0,
                "create_time": "2022-03-31 11:18:15",
                "update_time": "2024-06-30 17:40:07",
                "children": []
            }
        }


class AuthMenuDetailVo(BaseModel):
    """ 菜单详情Vo """
    id: int = Field(description="菜单ID")
    pid: int = Field(description="父级ID")
    type: str = Field(description="权限类型: [M=目录, C=菜单, A=按钮]")
    name: str = Field(description="菜单名称")
    icon: str = Field(description="菜单图标")
    perms: str = Field(description="菜单权限")
    params: str = Field(description="路由参数")
    component: str = Field(description="组件路径")
    path: str = Field(description="页面路径")
    sort: int = Field(description="菜单排序")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "type": "C",
                "name": "Index",
                "icon": "el-icon-house",
                "perms": "index:console",
                "params": "",
                "component": "workbench",
                "path": "workbench",
                "sort": 9900,
                "is_show": 1,
                "is_disable": 0
            }
        }
