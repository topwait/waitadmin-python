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
from typing import List
from fastapi import APIRouter, Request, Depends
from hypertext import R, response_json, PagingResult
from apps.api.schemas import article_schema as schema
from apps.api.service.article_service import ArticleService

router = APIRouter(prefix="/article", tags=["文章管理"])


@router.get("/category", summary="文章分类", response_model=R[List[schema.ArticleCategoryVo]])
@response_json
async def category():
    return await ArticleService.category()


@router.get("/lists", summary="文章列表", response_model=PagingResult[schema.ArticleListsVo])
@response_json
async def lists(params: schema.ArticleSearchIn = Depends()):
    return await ArticleService.lists(params)


@router.get("/detail", summary="文章详情", response_model=schema.ArticleDetailVo)
@response_json
async def detail(request: Request, params: schema.ArticleDetailIn = Depends()):
    user_id: int = request.state.user_id
    return await ArticleService.detail(params.id, user_id)


@router.get("/pages", summary="文章页面", response_model=schema.ArticlePagesVo)
@response_json
async def pages():
    return await ArticleService.pages()


@router.post("/collect", summary="文章收藏", response_model=R)
@response_json
async def collect(request: Request, params: schema.ArticleCollectIn):
    user_id: int = request.state.user_id
    return await ArticleService.collect(params.id, user_id)
