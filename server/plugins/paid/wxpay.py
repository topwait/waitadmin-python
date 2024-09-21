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
import time
import uuid
from typing import Dict
from urllib.parse import quote
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from wechatpayv3 import WeChatPay, WeChatPayType
from kernels.utils import RequestUtil
from common.enums.pay import PayEnum
from common.enums.client import ClientEnum
from common.models.dev import DevPayConfigModel
from plugins.wechat.configs import WeChatConfig


class WxpayService:

    @classmethod
    async def unify_order(cls, terminal: int, attach, order: dict):
        order_params = {
            "openid": order.get("openid", ""),
            "out_trade_no": order.get("out_trade_no", ""),
            "description": order.get("description", ""),
            "order_amount": order.get("order_amount", 0),
            "redirect_url": order.get("redirect_url", "")
        }

        if terminal == ClientEnum.MNP:
            config = await WeChatConfig.get_wx_config()
            return await cls._jsapi_pay(attach, config.get("app_id"), order_params)
        elif terminal == ClientEnum.OA:
            config = await WeChatConfig.get_oa_config()
            return await cls._jsapi_pay(attach, config.get("app_id"), order_params)
        elif terminal == ClientEnum.H5:
            config = await WeChatConfig.get_oa_config()
            return await cls._web_pay(attach, config.get("app_id"), order_params)
        elif terminal == ClientEnum.PC:
            config = await WeChatConfig.get_oa_config()
            return await cls._native_pay(attach, config.get("app_id"), order_params)
        elif terminal == ClientEnum.IOS or terminal == ClientEnum.ANDROID:
            config = await WeChatConfig.get_oa_config()
            return await cls._app_pay(attach, config.get("app_id"), config.get("mch_id"), order_params)

    @classmethod
    async def wxpay(cls, appid: str = ""):
        config = await cls.options()
        return WeChatPay(
            appid=appid,
            mchid=config.get("mch_id"),
            apiv3_key=config.get("secret_key"),
            private_key=config.get("private_key"),
            cert_serial_no=config.get("cert_serial_no"),
            notify_url=config.get("notify_url"),
            cert_dir="./runtime/cert",
            partner_mode=False,
            wechatpay_type=None,
            proxy=None,
            timeout=(10, 30)
        )

    @classmethod
    async def options(cls) -> Dict[str, str]:
        config = await DevPayConfigModel.filter(channel=PayEnum.WAY_MNP).get()
        params = json.loads(config.params)

        # 证书私钥(兼容处理)
        private_key = str(params.get("apiclient_key", ""))
        private_key = private_key.replace("-----BEGIN PRIVATE KEY-----", "")
        private_key = private_key.replace("-----END PRIVATE KEY-----", "")
        private_key = private_key.strip().replace("\n", "").strip()
        private_key = "-----BEGIN PRIVATE KEY-----\n" + private_key + "\n-----END PRIVATE KEY-----"

        # 商户证书(兼容处理)
        certificate = str(params.get("apiclient_cert", ""))
        certificate = certificate.replace("-----BEGIN CERTIFICATE-----", "")
        certificate = certificate.replace("-----END CERTIFICATE-----", "")
        certificate = certificate.strip().replace("\n", "").strip()
        certificate = "-----BEGIN CERTIFICATE-----\n" + certificate + "\n-----END CERTIFICATE-----"

        # 商户证书序列号
        try:
            pem_data = str(certificate).encode()
            pem_cert = x509.load_pem_x509_certificate(pem_data, default_backend())
            hex_serial = hex(pem_cert.serial_number)
            cert_serial_no = hex_serial[2:] if hex_serial.startswith("0x") else hex_serial
        except Exception as e:
            raise Exception("apiclient_cert configuration error: {}".format(str(e)))

        return {
            "mch_id": str(params.get("mch_id", "")).strip(),
            "secret_key": str(params.get("secret_key", "")).strip(),
            "private_key": private_key,
            "certificate": certificate,
            "cert_serial_no": cert_serial_no,
            "notify_url": f"{RequestUtil.domain}/{RequestUtil.module}/payment/notify_mnp"
        }

    @classmethod
    async def _jsapi_pay(cls, attach, appid: str, order_params: dict) -> Dict[str, str]:
        _key = {}
        _app = await cls.wxpay(appid)
        code, message = _app.pay(
            *_key,
            pay_type=WeChatPayType.JSAPI,
            description=str(order_params["description"]),
            out_trade_no=str(order_params["out_trade_no"]),
            attach=attach,
            amount={
               "total": int(order_params["order_amount"] * 100)
            },
            payer={
                "openid": str(order_params["openid"])
            }
        )

        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = str(int(time.time()))
            noncestr = str(uuid.uuid4()).replace("-", "")
            package = "prepay_id=" + prepay_id
            sign = _app.sign([appid, timestamp, noncestr, package])
            signtype = "RSA"
            return {
                "appId": appid,
                "timeStamp": timestamp,
                "nonceStr": noncestr,
                "package": "prepay_id=%s" % prepay_id,
                "signType": signtype,
                "paySign": sign
            }
        else:
            raise Exception(result["message"])

    @classmethod
    async def _mnp_pay(cls, attach, appid: str, order_params: dict) -> Dict[str, str]:
        _key = {}
        _app = await cls.wxpay(appid)
        code, message = _app.pay(
            *_key,
            pay_type=WeChatPayType.MINIPROG,
            description=str(order_params["description"]),
            out_trade_no=str(order_params["out_trade_no"]),
            attach=attach,
            payer={
                "openid": str(order_params["openid"])
            },
            amount={
                "total": int(order_params["order_amount"] * 100)
            }
        )

        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = str(int(time.time()))
            noncestr = str(uuid.uuid4()).replace("-", "")
            package = "prepay_id=" + prepay_id
            sign = _app.sign(data=[appid, timestamp, noncestr, package])
            signtype = "RSA"
            return {
                "appId": appid,
                "timeStamp": timestamp,
                "nonceStr": noncestr,
                "package": "prepay_id=%s" % prepay_id,
                "signType": signtype,
                "paySign": sign
            }
        else:
            raise Exception(result["message"])

    @classmethod
    async def _app_pay(cls, attach, appid: str, mch_id: str, order_params: dict) -> Dict[str, str]:
        """ App支付 """
        _key = {}
        _app = await cls.wxpay(appid)
        code, message = _app.pay(
            *_key,
            attach=attach,
            pay_type=WeChatPayType.APP,
            description=str(order_params["description"]),
            out_trade_no=str(order_params["out_trade_no"]),
            amount={
                "total": int(order_params["order_amount"] * 100)
            }
        )

        result = json.loads(message)
        if code in range(200, 300):
            prepay_id = result.get("prepay_id")
            timestamp = str(int(time.time()))
            noncestr = str(uuid.uuid4()).replace("-", "")
            package = "Sign=WXPay"
            sign = _app.sign(data=[appid, timestamp, noncestr, prepay_id])
            return {
                "appid": appid,
                "partnerid": mch_id,
                "prepayid": prepay_id,
                "package": package,
                "nonceStr": noncestr,
                "timestamp": timestamp,
                "sign": sign
            }
        else:
            raise Exception(result["message"])

    @classmethod
    async def _web_pay(cls, attach, appid: str, order_params: dict) -> Dict[str, str]:
        """ H5支付 """
        _key = {}
        _app = await cls.wxpay(appid)
        code, message = _app.pay(
            *_key,
            pay_type=WeChatPayType.H5,
            description=str(order_params["description"]),
            out_trade_no=str(order_params["out_trade_no"]),
            attach=attach,
            amount={
                "total": int(order_params["order_amount"] * 100)
            },
            scene_info={
                "payer_client_ip": "113.66.231.22",
                "h5_info": {
                    "type": "Wap"
                }
            }
        )

        results = json.loads(message)
        if code == 200:
            domain: str = ""
            redirect: str = f"{domain}/mobile/{order_params['redirect_url']}?id={order_params['id']}&from={attach}"
            return {"h5_url": results["h5_url"] + "&redirect_url=" + quote(redirect)}
        else:
            raise Exception(results["message"])

    @classmethod
    async def _native_pay(cls, attach, appid: str, order_params: dict) -> str:
        """ Native(PC)支付 """
        _key = {}
        _app = await cls.wxpay(appid)
        code, message = _app.pay(
            *_key,
            pay_type=WeChatPayType.NATIVE,
            description=str(order_params["description"]),
            out_trade_no=str(order_params["out_trade_no"]),
            attach=attach,
            amount={
                "total": int(order_params["order_amount"] * 100)
            }
        )

        results = json.loads(message)
        if code == 200:
            return results["code_url"]
        else:
            raise Exception(results["message"])
