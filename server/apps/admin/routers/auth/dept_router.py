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
from apps.admin.schemas.auth import dept_schema as schema
from apps.admin.service.auth.dept_service import DeptService

router = APIRouter(prefix="/dept", tags=["权限部门"])


@router.get("/whole", summary="所有部门", response_model=R[schema.AuthDeptWholeVo])
@response_json
async def whole():
    return await DeptService.whole()


@router.get("/lists", summary="部门列表", response_model=R[schema.AuthDeptListVo])
@response_json
async def lists(params: schema.AuthDeptSearchIn = Depends()):
    return await DeptService.lists(params)


@router.get("/detail", summary="部门详情", response_model=R[schema.AuthDeptDetailVo])
@response_json
async def detail(params: schema.AuthDeptDetailIn = Depends()):
    return await DeptService.detail(params.id)


@router.post("/add", summary="部门新增", response_model=R)
@response_json
async def add(params: schema.AuthDeptAddIn):
    return await DeptService.add(params)


@router.post("/edit", summary="部门编辑", response_model=R)
@response_json
async def edit(params: schema.AuthDeptEditIn):
    return await DeptService.edit(params)


@router.post("/delete", summary="部门删除", response_model=R)
@response_json
async def delete(params: schema.AuthDeptDeleteIn):
    return await DeptService.delete(params.id)
