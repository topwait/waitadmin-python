# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin_fastapi
# | github:  https://github.com/topwait/waitadmin_fastapi
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
from fastapi import APIRouter
from hypertext import R, response_json
from apps.admin.schemas import common_schema as schema
from apps.admin.service.index_service import IndexService

router = APIRouter(prefix="/index", tags=["公共接口"])


@router.get("/config", summary="后台配置", response_model=R[schema.SysConfigVo])
@response_json
async def config():
    return await IndexService.config()


@router.get("/workbench", summary="控制台", response_model=R[schema.WorkbenchVo])
@response_json
async def workbench():
    return await IndexService.workbench()