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
from apps.admin.schemas import attach_schema as schema
from apps.admin.service.attach_service import AttachService

router = APIRouter(prefix="/attach", tags=["附件管理"])


@router.get("/album_lists", summary="附件列表", response_model=R[schema.AlbumListVo])
@response_json
async def album_lists(params: schema.AlbumSearchIn = Depends()):
    return await AttachService.album_lists(params)


@router.post("/album_move", summary="附件移动", response_model=R)
@response_json
async def album_move(params: schema.AlbumMoveIn):
    return await AttachService.album_move(params)


@router.post("/album_rename", summary="附件命名", response_model=R)
@response_json
async def album_rename(params: schema.AlbumRenameIn):
    return await AttachService.album_rename(params)


@router.post("/album_delete", summary="附件删除", response_model=R)
@response_json
async def album_delete(params: schema.AlbumDeleteIn):
    return await AttachService.album_delete(params)


@router.get("/cate_lists", summary="分组列表", response_model=R[schema.AlbumCateListVo])
@response_json
async def cate_lists(params: schema.AlbumCateSearchIn = Depends()):
    return await AttachService.cate_lists(params)


@router.post("/cate_add", summary="分组创建", response_model=R)
@response_json
async def cate_add(params: schema.AlbumCateCreateIn):
    return await AttachService.cate_add(params)


@router.post("/cate_rename", summary="分组命名", response_model=R)
@response_json
async def cate_rename(params: schema.AlbumCateRenameIn):
    return await AttachService.cate_rename(params)


@router.post("/cate_delete", summary="分组删除", response_model=R)
@response_json
async def cate_delete(params: schema.AlbumCateDeleteIn):
    return await AttachService.cate_delete(params)
