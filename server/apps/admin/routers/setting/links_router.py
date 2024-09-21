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
from apps.admin.schemas.setting import links_schema as schema
from apps.admin.service.setting.links_service import LinksService

router = APIRouter(prefix="/links", tags=["友链配置"])


@router.get("/lists", summary="友情链接列表", response_model=R[PagingResult[schema.LinksListVo]])
@response_json
async def lists(params: schema.LinksSearchIn = Depends()):
    return await LinksService.lists(params)


@router.get("/detail", summary="友情链接详情", response_model=R[schema.LinksDetailVo])
@response_json
async def detail(params: schema.LinksDetailIn = Depends()):
    return await LinksService.detail(params.id)


@router.post("/add", summary="友情链接新增", response_model=R)
@response_json
async def add(params: schema.LinksAddIn):
    return await LinksService.add(params)


@router.post("/edit", summary="友情链接编辑", response_model=R)
@response_json
async def edit(params: schema.LinksEditIn):
    return await LinksService.edit(params)


@router.post("/delete", summary="友情链接删除", response_model=R)
@response_json
async def delete(params: schema.LinksDeleteIn):
    return await LinksService.delete(params.id)
