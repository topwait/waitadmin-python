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
from typing import Union
from fastapi import Query
from pydantic import BaseModel, Field


class AuthPostSearchIn(BaseModel):
    """ 岗位搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    code: Union[str, None] = Query(default=None, description="岗位编号")
    name: Union[str, None] = Query(default=None, description="岗位名称")
    is_disable: Union[int, str, None] = Query(default=None, description="是否禁用: [0=正常, 1=禁用]")


class AuthPostDetailIn(BaseModel):
    """ 岗位详情参数 """
    id: int = Query(..., gt=0, description="岗位ID")


class AuthPostAddIn(BaseModel):
    """ 岗位新增参数 """
    code: str = Field(..., max_length=30, description="岗位编号")
    name: str = Field(..., max_length=30, description="岗位名称")
    remarks: str = Field(..., max_length=200, description="岗位备注")
    sort: int = Field(ge=0, default=0, description="岗位排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "286427",
                "name": "Programmer",
                "remarks": "负责维护Java项目和功能迭代",
                "sort": 0,
                "is_disable": 0
            }
        }


class AuthPostEditIn(BaseModel):
    """ 岗位编辑参数 """
    id: int = Field(..., gt=0, description="管理员ID")
    code: str = Field(..., max_length=30, description="岗位编号")
    name: str = Field(..., max_length=30, description="岗位名称")
    remarks: str = Field(..., max_length=200, description="岗位备注")
    sort: int = Field(ge=0, default=0, description="岗位排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "code": "286427",
                "name": "Programmer",
                "remarks": "Development and Maintenance",
                "sort": 0,
                "is_disable": 0
            }
        }


class AuthPostDeleteIn(BaseModel):
    """ 岗位删除参数 """
    id: int = Field(..., gt=0, description="岗位ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class AuthPostWholeVo(BaseModel):
    """ 所有岗位Vo """
    id: int = Field(description="岗位ID")
    code: str = Field(description="岗位编号")
    name: str = Field(description="岗位名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "code": "2685469",
                "name": "Programmer"
            }
        }


class AuthPostListVo(BaseModel):
    """ 岗位列表Vo """
    id: int = Field(description="岗位ID")
    code: str = Field(description="岗位编号")
    name: str = Field(description="岗位名称")
    remarks: str = Field(description="岗位备注")
    sort: int = Field(description="岗位排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "code": "2685469",
                "name": "Programmer",
                "remarks": "Development and Maintenance",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2024-03-26 11:20:00",
                "update_time": "2024-03-26 11:20:00"
            }
        }


class AuthPostDetailVo(BaseModel):
    """ 岗位详情Vo """
    id: int = Field(description="岗位ID")
    code: str = Field(description="岗位编号")
    name: str = Field(description="岗位名称")
    remarks: str = Field(description="岗位备注")
    sort: int = Field(description="岗位排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "code": "2685469",
                "name": "Programmer",
                "remarks": "Development and Maintenance",
                "sort": 0,
                "is_disable": 0
            }
        }
