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
from typing import Union, List
from fastapi import Query
from pydantic import BaseModel, Field


class AuthRoleSearchIn(BaseModel):
    """ 角色搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    name: Union[str, None] = Query(default=None, description="角色名称")


class AuthRoleDetailIn(BaseModel):
    """ 角色详情参数 """
    id: int = Query(..., gt=0, description="角色ID")


class AuthRoleAddIn(BaseModel):
    """ 角色新增参数 """
    name: str = Field(..., min_length=2, max_length=20, description="角色名称")
    describe: str = Field(max_length=200, default="", description="角色描述")
    sort: int = Field(ge=0, le=999999, default=0, description="角色排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")
    menu_ids: List[int] = Field(default=[], description="菜单权限")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "boss",
                "describe": "Super administrator",
                "sort:": 0,
                "is_disable": 0,
                "menu_ids": []
            }
        }


class AuthRoleEditIn(BaseModel):
    """ 角色编辑参数 """
    id: int = Field(..., gt=0, description="角色ID")
    name: str = Field(..., min_length=2, max_length=20, description="角色名称")
    describe: str = Field(max_length=200, description="角色描述")
    sort: int = Field(ge=0, le=999999, default=0, description="角色排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")
    menu_ids: List[int] = Field(default=[], description="菜单权限")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "boss",
                "describe": "Super administrator",
                "sort:": 0,
                "is_disable": 0,
                "menu_ids": []
            }
        }


class AuthRoleDeleteIn(BaseModel):
    """ 角色删除参数 """
    id: int = Field(..., gt=0, description="角色ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class AuthRoleWholeVo(BaseModel):
    """ 所有角色Vo """
    id: int = Field(description="角色ID")
    name: str = Field(description="角色名称")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "boss",
                "is_disable": 0
            }
        }


class AuthRoleListVo(BaseModel):
    """ 角色列表Vo """
    id: int = Field(description="角色ID")
    name: str = Field(description="角色名称")
    describe: str = Field(description="角色描述")
    admin_sum: int = Field(default=0, description="管理员数")
    sort: int = Field(description="角色排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "boss",
                "describe": "Super administrator",
                "admin_sum": 1,
                "sort:": 0,
                "is_disable": 0,
                "create_time": "2023-11:12 11:23:34",
                "update_time": "2023-11:12 11:23:34",
            }
        }


class AuthRoleDetailVo(BaseModel):
    """ 角色详情Vo """
    id: int = Field(description="角色ID")
    name: str = Field(description="角色名称")
    describe: str = Field(description="角色描述")
    sort: int = Field(description="角色排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    menu_ids: List[int] = Field(description="菜单权限")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "boss",
                "describe": "Super administrator",
                "sort:": 0,
                "is_disable": 0,
                "menu_ids": []
            }
        }
