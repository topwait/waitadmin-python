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
from exception import AppException
from common.enums.pay import PayEnum
from common.utils.urls import UrlUtil
from common.models.dev import DevPayConfigModel
from common.models.market import RechargeOrderModel
from plugins.paid.wxpay import WxpayService
from plugins.paid.ailpay import AlipayService
from apps.api.schemas import payment_schema as schema


class PaymentService:
    """ 支付服务类 """

    @classmethod
    async def pay_way(cls):
        """ 支付方式 """
        ways = await DevPayConfigModel.filter(status=1).order_by("-sort", "-id").all()
        _data = []
        for item in ways:
            _data.append(schema.PayWayListVo(
                channel=item.channel,
                shorter=item.shorter,
                icon=await UrlUtil.to_absolute_url(item.icon)
            ))
        return _data

    @classmethod
    async def listen(cls, attach: str, order_id: int, user_id: int) -> schema.PayListenVo:
        order = None
        if attach == "recharge":
            order = await RechargeOrderModel\
                .filter(id=order_id, user_id=user_id)\
                .first()\
                .values("id", "pay_status")

        # 状态定义: [-1=订单不存在, 0=未支付, 1=已支付, 2=已过期]
        data = schema.PayListenVo(status=0, message="订单未支付")

        # 订单丢失
        if not order:
            schema.PayListenVo(status=0, message="订单未支付")
            data.status = -1
            data.message = "订单异常"

        # 支付成功
        if order["pay_status"] == PayEnum.PAID_OK:
            data.status = 1
            data.message = "订单已支付"

        return data

    @classmethod
    async def prepay(cls, terminal: int, post: schema.PayPrepayIn):
        """ 预支付下单 """
        order = None
        description: str = ""
        if post.attach == "recharge":
            description = "充值积分"
            order = await RechargeOrderModel.filter(id=post.order_id).first()
        elif post.attach == "order":
            pass

        if not order:
            raise AppException("订单不存在")

        # 更新支付方式
        order.pay_pay = post.pay_way
        order.terminal = terminal
        await order.save()

        # 发起支付请求
        if post.pay_way == PayEnum.WAY_MNP:
            return await WxpayService.unify_order(terminal, post.attach, {
                "out_trade_no": order.order_sn,
                "order_amount": order.paid_amount,
                "description": description,
                "redirect_url": post.redirect_url
            })
        elif post.pay_way == PayEnum.WAY_ALI:
            return await AlipayService.unify_order(terminal, post.attach, {
                "out_trade_no": order.order_sn,
                "order_amount": order.paid_amount,
                "description": description,
                "redirect_url": post.redirect_url
            })

    @classmethod
    async def notify_mnp(cls):
        pass

    @classmethod
    async def notify_ali(cls):
        pass
