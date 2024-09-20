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
from fastapi import APIRouter, Request, Depends
from hypertext import R, PagingResult, response_json
from apps.admin.schemas.auth import admin_schema as schema
from apps.admin.service.auth.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["权限用户"])


@router.get("/lists", summary="管理员列表", response_model=R[PagingResult[schema.AuthAdminListVo]])
@response_json
async def lists(params: schema.AuthAdminSearchIn = Depends()):
    return await AdminService.lists(params)


@router.get("/oneself", summary="管理员自身", response_model=R[schema.AuthAdminOneselfVo])
@response_json
async def oneself(request: Request):
    admin_id: int = request.state.admin_id
    return await AdminService.oneself(admin_id)


@router.get("/detail", summary="管理员详情", response_model=R[schema.AuthAdminDetailVo])
@response_json
async def detail(params: schema.AuthAdminDetailIn = Depends()):
    return await AdminService.detail(params.id)


@router.post("/add", summary="管理员新增", response_model=R)
@response_json
async def add(params: schema.AuthAdminAddIn):
    return await AdminService.add(params)


@router.post("/edit", summary="管理员编辑", response_model=R)
@response_json
async def edit(request: Request, params: schema.AuthAdminEditIn):
    admin_id: int = request.state.admin_id
    return await AdminService.edit(params, admin_id)


@router.post("/delete", summary="管理员删除", response_model=R)
@response_json
async def delete(request: Request, params: schema.AuthAdminDeleteIn):
    admin_id: int = request.state.admin_id
    return await AdminService.delete(params.id, admin_id)


@router.post("/set_info", summary="管理员设置", response_model=R)
@response_json
async def set_info(request: Request, params: schema.AuthAdminInfoIn):
    admin_id: int = request.state.admin_id
    return await AdminService.set_info(params, admin_id)
