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
from fastapi import APIRouter, Depends
from hypertext import R, PagingResult, response_json
from apps.admin.schemas.setting import banner_schema as schema
from apps.admin.service.setting.banner_service import BannerService

router = APIRouter(prefix="/banner", tags=["轮播配置"])


@router.get("/sites", summary="轮播图位置", response_model=R[List[schema.BannerSiteVo]])
@response_json
async def sites():
    return await BannerService.sites()


@router.get("/lists", summary="轮播图列表", response_model=R[PagingResult[schema.BannerListVo]])
@response_json
async def lists(params: schema.BannerSearchIn = Depends()):
    return await BannerService.lists(params)


@router.get("/detail", summary="轮播图详情", response_model=R[schema.BannerDetailVo])
@response_json
async def detail(params: schema.BannerDetailIn = Depends()):
    return await BannerService.detail(params.id)


@router.post("/add", summary="轮播图新增", response_model=R)
@response_json
async def add(params: schema.BannerAddIn):
    return await BannerService.add(params)


@router.post("/edit", summary="轮播图编辑", response_model=R)
@response_json
async def edit(params: schema.BannerEditIn):
    return await BannerService.edit(params)


@router.post("/delete", summary="轮播图删除", response_model=R)
@response_json
async def delete(params: schema.BannerDeleteIn):
    return await BannerService.delete(params.id)
