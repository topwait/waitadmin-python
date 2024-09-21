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


class UserGroupSearchIn(BaseModel):
    """ 用户分组搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    name: Union[str, None] = Query(default=None, description="分组名称")


class UserGroupDetailIn(BaseModel):
    """ 用户分组详情参数 """
    id: int = Query(..., gt=0, description="分组ID")


class UserGroupAddIn(BaseModel):
    """ 用户分组新增参数 """
    name: str = Field(..., max_length=30, description="名称")
    remarks: str = Field(..., max_length=200, description="备注")
    sort: int = Field(ge=0, le=999999, default=0, description="排序")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Gentleman",
                "remarks": "a gentleman of wealth and position",
                "sort": 0
            }
        }


class UserGroupEditIn(BaseModel):
    """ 用户分组编辑参数 """
    id: int = Field(..., gt=0, description="分组ID")
    name: str = Field(..., max_length=30, description="名称")
    remarks: str = Field(..., max_length=200, description="备注")
    sort: int = Field(ge=0, le=999999, default=0, description="排序")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Gentleman",
                "remarks": "a gentleman of wealth and position",
                "sort": 0
            }
        }


class UserGroupDeleteIn(BaseModel):
    """ 用户分组删除参数 """
    id: int = Field(..., gt=0, description="文章分类ID")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class UserGroupWholeVo(BaseModel):
    """ 所有用户分组Vo """
    id: int = Field(description="分组ID")
    name: str = Field(description="分组名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Gentleman"
            }
        }


class UserGroupListVo(BaseModel):
    """ 用户分组列表Vo """
    id: int = Field(description="分组ID")
    name: str = Field(description="分组名称")
    remarks: str = Field(description="备注")
    sort: int = Field(description="排序")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Gentleman",
                "remarks": "a gentleman of wealth and position",
                "sort": 0,
                "create_time": "2024-04-18 11:22:33",
                "update_time": "2024-04-18 11:22:33"
            }
        }


class UserGroupDetailVo(BaseModel):
    """ 用户分组详情Vo """
    id: int = Field(description="分组ID")
    name: str = Field(description="名称")
    remarks: str = Field(description="备注")
    sort: int = Field(description="排序")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Gentleman",
                "remarks": "a gentleman of wealth and position",
                "sort": 0
            }
        }
