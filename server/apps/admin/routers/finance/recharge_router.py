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
from apps.admin.schemas.finance import recharge_schema as schema
from apps.admin.service.finance.recharge_service import RechargeService

router = APIRouter(prefix="/recharge", tags=["余额明细"])


@router.get("/lists", summary="充值记录列表", response_model=R[schema.RechargeListVo])
@response_json
async def lists(params: schema.RechargeSearchIn = Depends()):
    return await RechargeService.lists(params)
