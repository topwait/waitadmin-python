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
from fastapi import Query
from pydantic import BaseModel, Field


class RechargePackageDetailIn(BaseModel):
    """ 充值套餐详情参数 """
    id: int = Query(..., gt=0, description="套餐ID")


class RechargePackageAddIn(BaseModel):
    """ 充值套餐新增参数 """
    money: Decimal = Field(..., max_digits=10, decimal_places=2, description="充值金额")
    give_money: Decimal = Field(default=Decimal(0), max_digits=10, decimal_places=2, description="赠送金额")
    sort: int = Field(ge=0, default=0, description="排序编号")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return {
            "money.missing": "请填写充值金额",
            "money.max_digits": "充值金额整数部分不能超出8位",
            "money.decimal_places": "充值金额只能保留2位小数",
            "give_money.max_digits": "赠送金额整数部分不能超出8位",
            "give_money.decimal_places": "赠送金额只能保留2位小数",
            "sort.ge": "排序号不能少于0",
            "is_show.ge": "管理员状态非合法值: [0, 1]",
            "is_show.le": "管理员状态非合法值: [0, 1]"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "money": 0.01,
                "give_money": 0,
                "sort": 10,
                "is_show": 1
            }
        }


class RechargePackageEditIn(BaseModel):
    """ 充值套餐编辑参数 """
    id: int = Field(..., gt=0, description="套餐ID")
    money: Decimal = Field(..., max_digits=10, decimal_places=2, description="充值金额")
    give_money: Decimal = Field(default=Decimal(0), max_digits=10, decimal_places=2, description="赠送金额")
    sort: int = Field(ge=0, default=0, description="排序编号")
    is_show: int = Field(ge=0, le=1, default=0, description="是否显示: [0=否, 1=是]")

    @classmethod
    def messages(cls):
        return RechargePackageAddIn.messages()

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "money": 0.01,
                "give_money": 0,
                "sort": 10,
                "is_show": 1
            }
        }


class RechargePackageDeleteIn(BaseModel):
    """ 充值套餐删除参数 """
    id: int = Field(gt=0, description="套餐ID", examples=[1])

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


class RechargeConfigIn(BaseModel):
    """ 充值套餐配置参数 """
    status: int = Field(ge=0, le=1, description="充值状态", examples=[1])
    min_recharge: Decimal = Field(..., max_digits=10, decimal_places=2, description="最低充值金额")

    class Config:
        json_schema_extra = {
            "example": {
                "status": 1,
                "min_recharge": 0.01
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class RechargePackageListVo(BaseModel):
    """ 充值套餐列表Vo """
    id: int = Field(description="套餐ID")
    money: Decimal = Field(description="充值金额")
    give_money: Decimal = Field(description="赠送金额")
    sort: int = Field(description="排序编号")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "money": 0.01,
                "give_money": 0,
                "sort": 10,
                "is_show": 1,
                "create_time": "2023-07-22 11:33:44",
                "update_time": "2023-07-22 11:33:44",
            }
        }


class RechargePackageDetailVo(BaseModel):
    """ 充值套餐详情Vo """
    id: int = Field(description="套餐ID")
    money: Decimal = Field(description="充值金额")
    give_money: Decimal = Field(description="所属部门")
    sort: int = Field(description="排序编号")
    is_show: int = Field(description="是否显示: [0=否, 1=是]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "money": 0.01,
                "give_money": 0,
                "sort": 10,
                "is_show": 1
            }
        }
