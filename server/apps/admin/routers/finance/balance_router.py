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
from apps.admin.schemas.finance import balance_schema as schema
from apps.admin.service.finance.balance_service import BalanceService

router = APIRouter(prefix="/balance", tags=["余额明细"])


@router.get("/lists", summary="余额明细列表", response_model=R[schema.BalanceListVo])
@response_json
async def lists(params: schema.BalanceSearchIn = Depends()):
    return await BalanceService.lists(params)
