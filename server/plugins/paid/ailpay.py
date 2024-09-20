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
from alipay import AliPay
from alipay.utils import AliPayConfig
from kernels.utils import RequestUtil
from exception import AppException
from common.enums.pay import PayEnum
from common.enums.client import ClientEnum
from common.models.dev import DevPayConfigModel


class AlipayService:

    @classmethod
    async def unify_order(cls, terminal: int, attach: str, order: dict):
        order_params = {
            "out_trade_no": order.get("out_trade_no", ""),
            "description": order.get("description", ""),
            "order_amount": order.get("order_amount", 0),
            "redirect_url": order.get("redirect_url", "")
        }

        if terminal == ClientEnum.PC:
            return await cls.page_pay(attach, order_params)
        elif terminal == ClientEnum.H5:
            return await cls.wap_pay(attach, order_params)
        elif terminal == ClientEnum.IOS or terminal == ClientEnum.ANDROID:
            return await cls.app_pay(attach, order_params)
        else:
            return await cls.mnp_pay(attach, order_params)

    @classmethod
    async def alipay(cls):
        try:
            config = await cls.options()
            return AliPay(
                appid=config.get("app_id"),
                app_notify_url=config.get("notify_url"),
                app_private_key_string=config.get("private_key"),
                alipay_public_key_string=config.get("public_key"),
                sign_type="RSA2",  # RSA或RSA2
                debug=False,       # 默认为False
                verbose=False,     # 输出调试数据
                config=AliPayConfig(timeout=15)
            )
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def options(cls):
        config = await DevPayConfigModel.filter(channel=PayEnum.WAY_ALI).get()
        params = json.loads(config.params)
        return {
            "app_id": params.get("app_id", "").strip(),
            "private_key": params.get("private_key", "").strip(),
            "public_key": params.get("public_key", "").strip(),
            "notify_url": f"{RequestUtil.domain}/{RequestUtil.module}/payment/notify_ali"
        }

    @classmethod
    async def page_pay(cls, attach: str, order_params: dict) -> str:
        """ 电脑网站支付(PC) """
        _pay = await cls.alipay()
        return_url = RequestUtil.domain + order_params.get("redirect_url", "").rstrip("/")
        order_string = _pay.api_alipay_trade_page_pay(
            out_trade_no=order_params.get("out_trade_no"),
            total_amount=str(order_params.get("order_amount")),
            subject=order_params.get("description"),
            return_url=return_url,
            passback_params=attach,
        )
        return "https://openapi.alipay.com/gateway.do?" + order_string

    @classmethod
    async def wap_pay(cls, attach: str, order_params: dict) -> str:
        """ 手机网站支付(H5) """
        _pay = await cls.alipay()
        return_url = RequestUtil.domain + order_params.get("redirect_url", "").rstrip("/")
        order_string = _pay.api_alipay_trade_wap_pay(
            out_trade_no=order_params.get("out_trade_no"),
            total_amount=str(order_params.get("order_amount")),
            subject=order_params.get("description"),
            return_url=return_url,
            passback_params=attach,
        )
        return "https://openapi.alipay.com/gateway.do?" + order_string

    @classmethod
    async def app_pay(cls, attach: str, order_params: dict):
        """ App支付 """
        _pay = await cls.alipay()
        return _pay.api_alipay_trade_app_pay(
            out_trade_no=order_params.get("out_trade_no"),
            total_amount=order_params.get("order_amount"),
            subject=order_params.get("description"),
            passback_params=attach
        )

    @classmethod
    async def mnp_pay(cls, attach: str, order_params: dict):
        """ 小程序支付 """
        _pay = await cls.alipay()
        return _pay.api_alipay_trade_create(
            out_trade_no=order_params.get("out_trade_no"),
            total_amount=order_params.get("order_amount"),
            subject=order_params.get("description"),
            buyer_id=order_params.get("buyer_id", ""),
            passback_params=attach
        )
