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
from hypertext import R, response_json
from apps.admin.schemas.auth import menu_schema as schema
from apps.admin.service.auth.menu_service import MenuService

router = APIRouter(prefix="/menu", tags=["权限菜单"])


@router.get("/whole", summary="所有菜单", response_model=R[List[schema.AuthMenuWholeVo]])
@response_json
async def whole():
    return await MenuService.whole()


@router.get("/routes", summary="菜单路由", response_model=R[List[schema.AuthMenuRoutesVo]])
@response_json
async def routes(request: Request):
    admin_id: int = request.state.admin_id
    role_id: int = request.state.role_id
    return await MenuService.routes(admin_id, role_id)


@router.get("/lists", summary="菜单列表", response_model=R[List[schema.AuthMenuListVo]])
@response_json
async def lists():
    return await MenuService.lists()


@router.get("/detail", summary="菜单详情", response_model=R[schema.AuthMenuDetailVo])
@response_json
async def detail(params: schema.AuthMenuDetailIn = Depends()):
    return await MenuService.detail(params.id)


@router.post("/add", summary="菜单新增", response_model=R)
@response_json
async def add(params: schema.AuthMenuAddIn):
    return await MenuService.add(params)


@router.post("/edit", summary="菜单编辑", response_model=R)
@response_json
async def edit(params: schema.AuthMenuEditIn):
    return await MenuService.edit(params)


@router.post("/delete", summary="菜单删除", response_model=R)
@response_json
async def delete(params: schema.AuthMenuDeleteIn):
    return await MenuService.delete(params.id)
