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


class LinksSearchIn(BaseModel):
    """ 友情链接搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    title: Union[str, None] = Query(default=None, description="友链名称")
    is_disable: Union[str, None] = Query(default=None, description="友链状态: [0=正常, 1=禁用]")


class LinksDetailIn(BaseModel):
    """ 友情链接详情参数 """
    id: int = Query(..., gt=0, description="友链ID")


class LinksAddIn(BaseModel):
    """ 友情链接新增参数 """
    title: str = Field(..., min_length=1, max_length=200, description="友链名称")
    image: str = Field(max_length=250, description="友链图标")
    target: str = Field(..., min_length=1, pattern=r"^(_self|_blank|_parent|_top)$", description="跳转方式")
    url: str = Field(max_length=250, default="", description="跳转链接")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "title.min_length": "请填写友链名称",
            "title.max_length": "友链名称不能超出200个字符",
            "image.max_length": "友链图标不能超出250个字符",
            "target.min_length": "请选择跳转方式",
            "target.pattern": "不支持的跳转方式",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999",
            "is_disable.ge": "轮播图状态非合法值: [0, 1]",
            "is_disable.le": "轮播图状态非合法值: [0, 1]"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "title": "ThinkPHP",
                "image": "https://xx.com/tp.png",
                "target": "_blank",
                "url": "https://www.thinkphp.cn",
                "sort": 0,
                "is_disable": 0
            }
        }


class LinksEditIn(BaseModel):
    """ 友情链接编辑参数 """
    id: int = Field(..., gt=0, description="友链ID")
    title: str = Field(..., min_length=1, max_length=200, description="友链名称")
    image: str = Field(max_length=250, description="友链图标")
    target: str = Field(..., min_length=1, pattern=r"^(_self|_blank|_parent|_top)$", description="跳转方式")
    url: str = Field(max_length=250, default="", description="跳转链接")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "title.min_length": "请填写友链名称",
            "title.max_length": "友链名称不能超出200个字符",
            "image.max_length": "友链图标不能超出250个字符",
            "target.min_length": "请选择跳转方式",
            "target.pattern": "不支持的跳转方式",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999",
            "is_disable.ge": "友链状态非合法值: [0, 1]",
            "is_disable.le": "友链状态非合法值: [0, 1]"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "ThinkPHP",
                "image": "https://xx.com/tp.png",
                "target": "_blank",
                "url": "https://www.thinkphp.cn",
                "sort": 0,
                "is_disable": 0
            }
        }


class LinksDeleteIn(BaseModel):
    """ 友情链接删除参数 """
    id: int = Field(gt=0, description="友链ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class LinksListVo(BaseModel):
    """ 友情链接列表Vo """
    id: int = Field(description="友链ID")
    title: str = Field(description="友链名称")
    image: str = Field(description="友链图标")
    target: str = Field(description="跳转方式")
    url: str = Field(description="跳转链接")
    sort: int = Field(description="排序编号")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "ThinkPHP",
                "image": "https://xx.com/tp.png",
                "target": "_blank",
                "url": "https://www.thinkphp.cn",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2023-03-12 00:32:13",
                "update_time": "2023-03-18 15:29:50"
            }
        }


class LinksDetailVo(BaseModel):
    """ 友情链接详情Vo """
    id: int = Field(description="友链ID")
    title: str = Field(description="友链名称")
    image: str = Field(description="友链图标")
    target: str = Field(description="跳转方式")
    url: str = Field(description="跳转链接")
    sort: int = Field(description="排序号")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "ThinkPHP",
                "image": "https://xx.com/tp.png",
                "target": "_blank",
                "url": "https://www.thinkphp.cn",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2023-03-12 00:32:13",
                "update_time": "2023-03-18 15:29:50"
            }
        }
