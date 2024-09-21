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
from fastapi import APIRouter, Request
from hypertext import R, response_json
from apps.api.schemas import recharge_schema as schema
from apps.api.service.recharge_service import RechargeService

router = APIRouter(prefix="/recharge", tags=["充值管理"])


@router.get("/package", summary="充值套餐", response_model=R[schema.RechargePackageVo])
@response_json
async def package():
    return await RechargeService.package()


@router.post("/place", summary="发起充值", response_model=R[schema.RechargePlaceVo])
@response_json
async def place(request: Request, params: schema.RechargeIn):
    user_id: int = request.state.user_id
    terminal: int = request.state.terminal
    return await RechargeService.place(user_id, terminal, params)
