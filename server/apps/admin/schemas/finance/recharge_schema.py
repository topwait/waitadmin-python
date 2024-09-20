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
from decimal import Decimal
from typing import Union
from fastapi import Query
from pydantic import BaseModel, Field


class RechargeSearchIn(BaseModel):
    """ 充值记录搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    user: Union[str, None] = Query(default=None, description="用户信息")
    order_sn: Union[str, None] = Query(default=None, description="充值单号")
    pay_way: Union[str, int, None] = Query(default=None, description="支付方式: [2=微信, 3=支付宝]")
    pay_status: Union[str, int, None] = Query(default=None, description="支付状态: [0=未支付, 1=已支付]")
    start_time: Union[int, str, None] = Query(default=None, description="开始时间")
    end_time: Union[int, str, None] = Query(default=None, description="结束时间")


"""---------------❤︎华丽分割线❤︎---------------"""


class RechargeListVo(BaseModel):
    """ 充值记录列表Vo """
    id: int = Field(description="文章ID")
    order_sn: str = Field(description="充值单号")
    paid_amount: Decimal = Field(description="充值金额")
    give_amount: Decimal = Field(description="赠送金额")
    pay_way: str = Field(description="支付方式")
    pay_status: int = Field(description="支付状态: [0=未支付, 1=已支付]")
    create_time: str = Field(description="创建时间")
    pay_time: str = Field(description="支付时间")
    user: dict = Field(default="用户信息")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 2,
                "order_sn": "B918447816245681",
                "paid_amount": 0.01,
                "give_amount": 0.0,
                "pay_way": "微信支付",
                "pay_status": 1,
                "create_time": "2023-09-18 21:46:21",
                "pay_time": "2023-09-18 21:46:24",
                "user": {
                    "sn": "80965941",
                    "avatar": "http://0.0.0.0:8100/xiao.png",
                    "mobile": "13800138000",
                    "nickname": "xiao"
                }
            }
        }
