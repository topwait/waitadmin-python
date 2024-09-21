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
from apps.admin.schemas.auth import role_schema as schema
from apps.admin.service.auth.role_service import RoleService

router = APIRouter(prefix="/role", tags=["权限角色"])


@router.get("/whole", summary="全部角色", response_model=R[schema.AuthRoleWholeVo])
@response_json
async def whole():
    return await RoleService.whole()


@router.get("/lists", summary="角色列表", response_model=R[schema.AuthRoleListVo])
@response_json
async def lists(params: schema.AuthRoleSearchIn = Depends()):
    return await RoleService.lists(params)


@router.get("/detail", summary="角色详情", response_model=R[schema.AuthRoleDetailIn])
@response_json
async def detail(params: schema.AuthRoleDetailIn = Depends()):
    return await RoleService.detail(params.id)


@router.post("/add", summary="角色新增", response_model=R)
@response_json
async def add(params: schema.AuthRoleAddIn):
    return await RoleService.add(params)


@router.post("/edit", summary="角色编辑", response_model=R)
@response_json
async def edit(params: schema.AuthRoleEditIn):
    return await RoleService.edit(params)


@router.post("/delete", summary="角色删除", response_model=R)
@response_json
async def delete(params: schema.AuthRoleDeleteIn):
    return await RoleService.delete(params.id)
