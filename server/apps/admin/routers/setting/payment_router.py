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
from fastapi import APIRouter, Depends
from hypertext import R, response_json
from apps.admin.schemas.setting import payment_schema as schema
from apps.admin.service.setting.payment_service import PaymentService


router = APIRouter(prefix="/payment", tags=["支付配置"])


@router.get("/lists", summary="支付配置列表", response_model=R[List[schema.PaymentListVo]])
@response_json
async def lists():
    return await PaymentService.lists()


@router.get("/detail", summary="支付配置详情", response_model=R[schema.PaymentDetailVo])
@response_json
async def detail(params: schema.PaymentDetailIn = Depends()):
    return await PaymentService.detail(params.id)


@router.post("/save", summary="支付配置保存", response_model=R)
@response_json
async def save(params: schema.PaymentDetailVo):
    return await PaymentService.save(params)
