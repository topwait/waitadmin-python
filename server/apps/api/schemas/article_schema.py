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
from typing import Union, List, Dict, Any
from pydantic import BaseModel, Field
from fastapi import Query


class ArticleSearchIn(BaseModel):
    """ 文章搜索参数 """
    page: int = Query(gt=0, default=1, description="当前页码")
    cid: Union[int, None] = Query(default=None, description="所属分类")
    keyword: Union[str, None] = Query(default=None, description="搜索关键词")


class ArticleDetailIn(BaseModel):
    """ 文章详情参数 """
    id: int = Query(..., gt=0, description="文章ID")


class ArticleCollectIn(BaseModel):
    """ 文章收藏参数 """
    id: int = Field(..., gt=0, description="文章ID")


"""---------------❤︎华丽分割线❤︎---------------"""


class ArticleCategoryVo(BaseModel):
    """ 分类列表VO """
    id: int = Field(description="分类ID")
    name: str = Field(description="分类名称")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "news"
            }
        }


class ArticleListsVo(BaseModel):
    """ 文章列表Vo """
    id: int = Field(description="文章ID")
    category: str = Field(default="", description="所属类目")
    image: str = Field(description="文章图片")
    title: str = Field(description="文章标题")
    intro: str = Field(description="文章简介")
    browse: int = Field(description="访问数量")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "category": "news",
                "image": "https://www.xx.com/images/article.jpg",
                "title": "this is article title",
                "intro": "this is intro...",
                "browse": 10,
                "create_time": "2023-03-08 21:28:28",
                "update_time": "2023-03-08 21:28:28",
            }
        }


class ArticlePagesVo(BaseModel):
    """ 文章页面Vo """
    adv: List[Dict[str, str]] = Field(description="轮播广告")
    topping: List[ArticleListsVo] = Field(description="推荐文章")
    ranking: List[ArticleListsVo] = Field(description="排名文章")

    class Config:
        json_schema_extra = {
            "example": {
                "adv": [
                    {
                        "title": "this is banner title",
                        "image": "https://www.xxx.com/ad.jpg",
                        "target": "_blank",
                        "url": "https://www.xxx.com"
                    }
                ],
                "topping": ArticleListsVo.model_config["json_schema_extra"]["example"],
                "everyday": ArticleListsVo.model_config["json_schema_extra"]["example"]
            }
        }


class ArticleDetailVo(BaseModel):
    """ 文章详情Vo """
    id: int = Field(description="文章ID")
    category: str = Field(description="所属类目")
    image: str = Field(description="文章图片")
    title: str = Field(description="文章标题")
    intro: str = Field(description="文章简介")
    content: str = Field(description="文章内容")
    browse: int = Field(description="访问数量")
    is_collect: int = Field(default="是否收藏: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")
    prev: Dict[str, Any] = Field(description="上一条记录")
    next: Dict[str, Any] = Field(description="下一条记录")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "image": "https://www.xx.com/images/article.jpg",
                "title": "this is article title",
                "intro": "this is intro...",
                "content": "this is content...",
                "browse": 10,
                "create_time": "2023-03-08 21:28:28"
            }
        }
