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
from hypertext import R, response_json
from apps.admin.schemas.content import category_schema as schema
from apps.admin.service.content.category_service import ArticleCateService

router = APIRouter(prefix="/category", tags=["文章分类"])


@router.get("/whole", summary="所有文章分类", response_model=R[schema.ArticleCateWholeVo])
@response_json
async def whole():
    return await ArticleCateService.whole()


@router.get("/lists", summary="文章分类列表", response_model=R[schema.ArticleCateListVo])
@response_json
async def lists(params: schema.ArticleCateSearchIn = Depends()):
    return await ArticleCateService.lists(params)


@router.get("/detail", summary="文章分类详情", response_model=R[schema.ArticleCateDetailVo])
@response_json
async def detail(params: schema.ArticleCateDetailIn = Depends()):
    return await ArticleCateService.detail(params.id)


@router.post("/add", summary="文章分类新增", response_model=R)
@response_json
async def add(params: schema.ArticleCateAddIn):
    await ArticleCateService.add(params)


@router.post("/edit", summary="文章分类编辑", response_model=R)
@response_json
async def add(params: schema.ArticleCateEditIn):
    await ArticleCateService.edit(params)


@router.post("/delete", summary="文章分类删除", response_model=R)
@response_json
async def delete(params: schema.ArticleCateDeleteIn):
    await ArticleCateService.delete(params.id)
