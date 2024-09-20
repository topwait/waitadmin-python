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


class ArticleCateSearchIn(BaseModel):
    """ 文章分类搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    name: Union[str, None] = Query(default=None, description="分类名称")
    is_disable: Union[int, str, None] = Query(default=None, description="是否禁用: [0=否, 1=是]")


class ArticleCateDetailIn(BaseModel):
    """ 文章分类详情参数 """
    id: int = Query(..., gt=0, description="文章分类ID")


class ArticleCateAddIn(BaseModel):
    """ 文章分类新增参数 """
    name: str = Field(..., min_length=1, max_length=20, description="分类名称")
    sort: int = Field(ge=0, le=999999, default=0, description="分类排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "name.min_length": "请填写分类名称",
            "name.max_length": "分类名称不能超出20个字符",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Technology",
                "sort": 0,
                "is_disable": 0
            }
        }


class ArticleCateEditIn(BaseModel):
    """ 文章分类编辑参数 """
    id: int = Field(..., gt=0, description="文章分类ID")
    name: str = Field(..., max_length=20, description="类目名称")
    sort: int = Field(ge=0, le=999999, default=0, description="类目排序")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "name.min_length": "请填写分类名称",
            "name.max_length": "分类名称不能超出20个字符",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Technology",
                "sort": 0,
                "is_disable": 0
            }
        }


class ArticleCateDeleteIn(BaseModel):
    """ 文章分类删除参数 """
    id: int = Field(..., gt=0, description="文章分类ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class ArticleCateWholeVo(BaseModel):
    """ 所有文章分类Vo """
    id: int = Field(description="分类ID")
    name: str = Field(description="分类名称")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Technology",
                "is_disable": 0
            }
        }


class ArticleCateListVo(BaseModel):
    """ 文章分类列表Vo """
    id: int = Field(description="分类ID")
    name: str = Field(description="分类名称")
    sort: int = Field(description="分类排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Technology",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2024-04-18 11:22:33",
                "update_time": "2024-04-18 11:22:33"
            }
        }


class ArticleCateDetailVo(BaseModel):
    """ 文章分类详情Vo """
    id: int = Field(description="分类ID")
    name: str = Field(description="分类名称")
    sort: int = Field(description="分类排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Technology",
                "sort": 0,
                "is_disable": 0
            }
        }
