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
from fastapi import APIRouter, Depends
from hypertext import R, PagingResult, response_json
from apps.admin.schemas.content import article_schema as schema
from apps.admin.service.content.article_service import ArticleService

router = APIRouter(prefix="/article", tags=["文章内容"])


@router.get("/lists", summary="文章列表", response_model=R[PagingResult[schema.ArticleListVo]])
@response_json
async def lists(params: schema.ArticleSearchIn = Depends()):
    return await ArticleService.lists(params)


@router.get("/detail", summary="文章详情", response_model=R[schema.ArticleDetailVo])
@response_json
async def detail(params: schema.ArticleDetailIn = Depends()):
    return await ArticleService.detail(params.id)


@router.post("/add", summary="文章新增", response_model=R)
@response_json
async def add(params: schema.ArticleAddIn):
    await ArticleService.add(params)


@router.post("/edit", summary="文章编辑", response_model=R)
@response_json
async def edit(params: schema.ArticleEditIn):
    await ArticleService.edit(params)


@router.post("/delete", summary="文章删除", response_model=R)
@response_json
async def delete(params: schema.ArticleDeleteIn):
    await ArticleService.delete(params.id)
