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
from fastapi import Query
from pydantic import BaseModel, Field


class PayListenIn(BaseModel):
    """ 支付监听参数 """
    order_id: int = Query(..., gt=0, description="订单ID")
    attach: str = Query(..., min_length=1, description="支付场景: [recharge]")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "attach": "recharge"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "order_id.gt": "请指定订单",
            "attach.min_length": "请指定订单来源"
        }


class PayPrepayIn(BaseModel):
    """ 预支付参数 """
    order_id: int = Field(..., gt=0, description="订单ID")
    pay_way: int = Field(..., gt=0, description="支付方式: [1=余额,2=微信,3=支付宝]")
    attach: str = Field(..., min_length=1, description="支付场景: [recharge]")
    redirect_url: str = Field(default='', description="重定向Url")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "pay_way": 2,
                "attach": "recharge",
                "redirect_url": ""
            }
        }

    @classmethod
    def messages(cls):
        return {
            "order_id.gt": "请正确下单",
            "pay_way.min_length": "请选择支付方式",
            "attach.min_length": "请指定订单来源"
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class PayWayListVo(BaseModel):
    """ 支付方式列表Vo """
    channel: int = Field(description="支付渠道")
    shorter: str = Field(description="支付名称")
    icon: str = Field(description="支付图标")

    class Config:
        json_schema_extra = {
            "example": {
                "channel": 2,
                "shorter": "微信支付",
                "icon": "https://www.xx.cn/wxpay.cn"
            }
        }


class PayListenVo(BaseModel):
    """ 支付监听结果Vo """
    status: int = Field(description="订单状态: [-1=订单不存在, 0=未支付, 1=已支付, 2=已过期]")
    message: str = Field(description="状态描述")

    class Config:
        json_schema_extra = {
            "example": {
                "status": 0,
                "message": "订单未支付"
            }
        }
