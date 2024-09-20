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
from apps.admin.schemas.users import group_schema as schema
from apps.admin.service.users.group_service import UserGroupService

router = APIRouter(prefix="/group", tags=["用户分组"])


@router.get("/whole", summary="全部用户分组", response_model=R[schema.UserGroupWholeVo])
@response_json
async def whole():
    return await UserGroupService.whole()


@router.get("/lists", summary="用户分组列表", response_model=R[schema.UserGroupListVo])
@response_json
async def lists(params: schema.UserGroupSearchIn = Depends()):
    return await UserGroupService.lists(params)


@router.get("/detail", summary="用户分组详情", response_model=R[schema.UserGroupDetailVo])
@response_json
async def detail(params: schema.UserGroupDetailIn = Depends()):
    return await UserGroupService.detail(params.id)


@router.post("/add", summary="用户分组新增", response_model=R)
@response_json
async def add(params: schema.UserGroupAddIn):
    return await UserGroupService.add(params)


@router.post("/edit", summary="用户分组编辑", response_model=R)
@response_json
async def add(params: schema.UserGroupEditIn):
    return await UserGroupService.edit(params)


@router.post("/delete", summary="用户分组删除", response_model=R)
@response_json
async def delete(params: schema.UserGroupDeleteIn):
    return await UserGroupService.delete(params.id)
