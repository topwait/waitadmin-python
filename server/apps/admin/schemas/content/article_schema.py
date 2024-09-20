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


class ArticleSearchIn(BaseModel):
    """ 文章搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    title: Union[str, None] = Query(default=None, description="文章标题")
    status: Union[int, str, None] = Query(default=None, description="文章状态")
    start_time: Union[int, str, None] = Query(default=None, description="开始时间")
    end_time: Union[int, str, None] = Query(default=None, description="结束时间")


class ArticleDetailIn(BaseModel):
    """ 文章详情参数 """
    id: int = Query(..., gt=0, description="文章ID")


class ArticleAddIn(BaseModel):
    """ 文章新增参数 """
    cid: int = Field(..., gt=0, description="类目")
    title: str = Field(..., min_length=1, max_length=100, description="标题")
    image: str = Field(max_length=200, default="", description="封面")
    intro: str = Field(max_length=200, default="", description="简介")
    content: str = Field(max_length=65535, default="", description="内容")
    sort: int = Field(ge=0, le=999999, default=0, description="排序")
    is_topping: int = Field(ge=0, le=1, default=0, description="是否置顶: [0=否, 1=是]")
    is_recommend: int = Field(ge=0, le=1, default=0, description="是否推荐: [0=否, 1=是]")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "cid.missing": "请选择所属类目",
            "cid.gt": "选择所属类目异常",
            "title.min_length": "请填写文章标题",
            "title.max_length": "文章标题不能超出100个字符",
            "content.max_length": "文章内容不能超出65535个字符",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "cid": 1,
                "title": "WaitAdmin welcome you",
                "image": "https://www.xxx.com/wa.png",
                "intro": "",
                "content": "",
                "sort": 0,
                "is_topping": 0,
                "is_recommend": 0,
                "is_show": 0
            }
        }


class ArticleEditIn(BaseModel):
    """ 文章编辑参数 """
    id: int = Field(..., gt=0, description="文章ID")
    cid: int = Field(..., gt=0, description="类目")
    title: str = Field(..., min_length=1, max_length=100, description="标题")
    image: str = Field(max_length=200, description="封面")
    intro: str = Field(max_length=200, description="简介")
    content: str = Field(max_length=65535, default="", description="内容")
    sort: int = Field(ge=0, le=999999, default=0, description="排序")
    is_topping: int = Field(ge=0, le=1, default=0, description="是否置顶: [0=否, 1=是]")
    is_recommend: int = Field(ge=0, le=1, default=0, description="是否推荐: [0=否, 1=是]")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "cid.missing": "请选择所属类目",
            "cid.gt": "选择所属类目异常",
            "title.min_length": "请填写文章标题",
            "title.max_length": "文章标题不能超出100个字符",
            "content.max_length": "文章内容不能超出65535个字符",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "cid": 1,
                "title": "WaitAdmin welcome you",
                "image": "https://www.xxx.com/wa.png",
                "intro": "",
                "content": "",
                "sort": 0,
                "is_topping": 0,
                "is_recommend": 0,
                "is_show": 0
            }
        }


class ArticleDeleteIn(BaseModel):
    """ 文章删除参数 """
    id: int = Field(gt=0, description="文章ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class ArticleListVo(BaseModel):
    """ 文章列表Vo """
    id: int = Field(description="文章ID")
    image: str = Field(description="封面")
    title: str = Field(description="标题")
    category: str = Field(default="", description="类目")
    browse: int = Field(description="浏览")
    collect: int = Field(description="收藏")
    sort: int = Field(description="排序")
    is_topping: int = Field(description="是否置顶: [0=否, 1=是]")
    is_recommend: int = Field(description="是否推荐: [0=否, 1=是]")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "image": "https://www.xxx.com/wa.png",
                "title": "WaitAdmin welcome you",
                "category": "Technology",
                "browse": 10,
                "collect": 5,
                "sort": 0,
                "is_topping": 0,
                "is_recommend": 0,
                "is_show": 1,
                "create_time": "2024-04-18 11:22:33",
                "update_time": "2024-04-18 11:22:33"
            }
        }


class ArticleDetailVo(BaseModel):
    """ 文章详情Vo """
    id: int = Field(description="文章ID")
    cid: int = Field(description="类目")
    image: str = Field(description="封面")
    title: str = Field(description="标题")
    intro: str = Field(description="简介")
    content: str = Field(description="内容")
    browse: int = Field(description="浏览")
    collect: int = Field(description="收藏")
    sort: int = Field(description="排序")
    is_topping: int = Field(description="是否置顶: [0=否, 1=是]")
    is_recommend: int = Field(description="是否推荐: [0=否, 1=是]")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "cid": 1,
                "image": "https://www.xxx.com/wa.png",
                "title": "WaitAdmin welcome you",
                "intro": "this is intro",
                "content": "this is content",
                "browse": 10,
                "collect": 5,
                "sort": 0,
                "is_topping": 0,
                "is_recommend": 0,
                "is_show": 1
            }
        }
