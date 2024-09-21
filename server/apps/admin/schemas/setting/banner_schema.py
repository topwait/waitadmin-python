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


class BannerSearchIn(BaseModel):
    """ 轮播图搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    title: Union[str, None] = Query(default=None, description="登录账号")
    is_disable: Union[str, None] = Query(default=None, description="联系电话")


class BannerDetailIn(BaseModel):
    """ 轮播图详情参数 """
    id: int = Query(..., gt=0, description="轮播图ID")


class BannerAddIn(BaseModel):
    """ 轮播图新增参数 """
    position: int = Field(ge=0, default=0, description="轮播位置")
    title: str = Field(..., min_length=1, max_length=20, description="轮播标题")
    image: str = Field(..., min_length=1, max_length=250, description="轮播图片")
    target: str = Field(..., min_length=1, pattern=r"^(_self|_blank|_parent|_top)$", description="跳转方式")
    url: str = Field(max_length=250, default="", description="跳转链接")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "position.missing": "请选择轮播位置",
            "position.ge": "轮播位置选择异常",
            "title.min_length": "请填写轮播标题",
            "title.max_length": "轮播标题不能超出200个字符",
            "image.min_length": "请上传轮播图片",
            "image.max_length": "图片链接不能超出250个字符",
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
                "position": 10,
                "title": "WaitAdmin welcome you",
                "image": "https://xx.com/banner.png",
                "target": "_blank",
                "url": "",
                "sort": 0,
                "is_disable": 0
            }
        }


class BannerEditIn(BaseModel):
    """ 轮播图编辑参数 """
    id: int = Field(..., gt=0, description="轮播ID")
    position: int = Field(ge=0, default=0, description="轮播位置")
    title: str = Field(..., min_length=1, max_length=200, description="轮播标题")
    image: str = Field(..., min_length=1, max_length=250, description="轮播图片")
    target: str = Field(..., min_length=1, pattern=r"^(_self|_blank|_parent|_top)$", description="跳转方式")
    url: str = Field(max_length=250, default="", description="跳转链接")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: int = Field(ge=0, le=1, default=0, description="是否禁用: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "position.missing": "请选择轮播位置",
            "position.ge": "轮播位置选择异常",
            "title.min_length": "请填写轮播标题",
            "title.max_length": "轮播标题不能超出200个字符",
            "image.min_length": "请上传轮播图片",
            "image.max_length": "图片链接不能超出250个字符",
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
                "id": 1,
                "position": 10,
                "title": "WaitAdmin welcome you",
                "image": "https://xx.com/banner.png",
                "target": "_blank",
                "url": "",
                "sort": 0,
                "is_disable": 0
            }
        }


class BannerDeleteIn(BaseModel):
    """ 轮播图删除参数 """
    id: int = Field(gt=0, description="轮播图ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class BannerSiteVo(BaseModel):
    id: int = Field(description="位置坐标")
    name: str = Field(description="位置名称")


class BannerListVo(BaseModel):
    """ 轮播图列表Vo """
    id: int = Field(description="轮播ID")
    position: str = Field(description="轮播位置")
    title: str = Field(description="轮播标题")
    image: str = Field(description="轮播图片")
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
                "position": "home",
                "title": "WaitAdmin welcome you",
                "image": "https://xx.com/banner.png",
                "target": "_blank",
                "url": "",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2023-03-12 00:32:13",
                "update_time": "2023-03-18 15:29:50",
                "location": [
                    {}
                ]
            }
        }


class BannerDetailVo(BaseModel):
    """ 轮播图详情Vo """
    id: int = Field(description="轮播ID")
    position: int = Field(description="轮播位置")
    title: str = Field(description="轮播标题")
    image: str = Field(description="轮播图片")
    target: str = Field(description="跳转方式")
    url: str = Field(description="跳转链接")
    sort: int = Field(description="轮播排序")
    is_disable: int = Field(description="是否禁用: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "position": 1,
                "title": "WaitAdmin welcome you",
                "image": "https://xx.com/banner.png",
                "target": "_blank",
                "url": "/",
                "sort": 0,
                "is_disable": 0,
                "create_time": "2023-03-12 00:32:13",
                "update_time": "2023-03-18 15:29:50"
            }
        }
