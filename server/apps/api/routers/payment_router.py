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
import json
from typing import List
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from hypertext import R, response_json
from apps.api.schemas import payment_schema as schema
from apps.api.service.payment_service import PaymentService
from apps.api.service.payNotify_service import PayNotifyService
from common.models.market import RechargeOrderModel
from common.enums.pay import PayEnum
from plugins.paid.wxpay import WxpayService
from plugins.paid.ailpay import AlipayService

router = APIRouter(prefix="/payment", tags=["支付管理"])


@router.get("/pay_way", summary="支付方式", response_model=R[List[schema.PayWayListVo]])
@response_json
async def pay_way():
    return await PaymentService.pay_way()


@router.get("/listen", summary="支付监听", response_model=R)
@response_json
async def listen(request: Request, params: schema.PayListenIn = Depends()):
    user_id: int = request.state.user_id
    return await PaymentService.listen(params.attach, params.order_id, user_id)


@router.post("/prepay", summary="预支付下单", response_model=R)
@response_json
async def prepay(request: Request, params: schema.PayPrepayIn):
    terminal: int = request.state.terminal
    return await PaymentService.prepay(terminal, params)


@router.api_route("/notify_mnp", summary="微信支付回调")
async def notify_mnp(request: Request):
    headers = request.headers
    data = await request.json()

    _wxpay = await WxpayService.wxpay()
    result = _wxpay.callback(headers, json.dumps(data))
    if result and result.get("event_type") == "TRANSACTION.SUCCESS":
        # 回调数据
        resp = result.get("resource")
        attach: str = resp.get("attach")
        out_trade_no: str = resp.get("out_trade_no")
        transaction_id: str = resp.get("transaction_id")

        # 查找订单
        status = False
        if attach == "recharge":
            order = await RechargeOrderModel.filter(order_sn=out_trade_no).first()
            if not order or order.pay_status == PayEnum.PAID_OK:
                status = True
        elif attach == "order":
            pass

        # 处理订单
        if not status:
            await PayNotifyService.handle(attach, out_trade_no, transaction_id)
        return JSONResponse(content={"code": "SUCCESS", "message": "成功"})
    else:
        return JSONResponse(content={"code": "FAILED", "message": "失败"})


@router.api_route("/notify_ali", summary="支付宝的回调")
async def notify_ali(request: Request):
    data = await request.json()
    signature = data.pop("sign")

    _alipay = await AlipayService.alipay()
    success = _alipay.verify(data, signature)
    if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        # 回调数据
        attach: str = data.get("passback_params")
        out_trade_no: str = data.get("out_trade_no")
        transaction_id: str = data.get("trade_no")

        # 查找订单
        status = False
        if attach == "order":
            pass
        elif attach == "recharge":
            order = await RechargeOrderModel.filter(order_sn=out_trade_no).first()
            if not order or PayEnum.PAID_OK == order.pay_status:
                status = True

        # 处理订单
        if not status:
            await PayNotifyService.handle(attach, out_trade_no, transaction_id)
        return "success"
    else:
        return "fail"