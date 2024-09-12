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
from apps.admin.schemas.setting import policy_schema as schema
from apps.admin.service.setting.policy_service import PolicyService

router = APIRouter(prefix="/policy", tags=["协议配置"])


@router.get("/detail", summary="协议配置详情", response_model=R[schema.PolicyDetailVo])
@response_json
async def detail():
    return await PolicyService.detail()


@router.post("/save", summary="协议配置保存", response_model=R)
@response_json
async def save(params: schema.PolicyDetailVo):
    return await PolicyService.save(params)
