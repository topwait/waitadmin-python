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
from pydantic import BaseModel, Field


class RechargeIn(BaseModel):
    """ 充值参数 """
    money: Decimal = Field(..., gt=0, description="充值金额")
    package_id: int = Field(ge=0, default=0, description="充值套餐")

    class Config:
        json_schema_extra = {
            "example": {
                "money": 0.01,
                "package_id": 0
            }
        }

    @classmethod
    def messages(cls):
        return {
            "money.gt": "充值金额不能少于等于0",
            "package_id.ge": "套餐选择异常",
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class RechargePackageVo(BaseModel):
    """ 充值套餐列表Vo """
    id: int = Field(description="ID")
    name: str = Field(description="套餐名称")
    money: Decimal = Field(max_digits=10, decimal_places=2, description="充值金额")
    give_money: Decimal = Field(max_digits=10, decimal_places=2, description="赠送金额")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "0.01",
                "money": 0.1,
                "give_money": 0
            }
        }


class RechargePlaceVo(BaseModel):
    """ 充值下单结果Vo """
    order_id: int = Field(description="ID")
    paid_amount: Decimal = Field(max_digits=10, decimal_places=2, description="赠送金额")

    class Config:
        json_schema_extra = {
            "example": {
                "order_id": 1,
                "paid_amount": 0.01
            }
        }
