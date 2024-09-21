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


class PaymentDetailIn(BaseModel):
    """ 支付配置详情参数 """
    id: int = Query(..., gt=0, description="支付配置ID")


"""---------------❤︎华丽分割线❤︎---------------"""


class PaymentListVo(BaseModel):
    """ 支付配置列表Vo """
    id: int = Field(description="ID")
    channel: int = Field(description="渠道别名")
    shorter: str = Field(description="简写名称")
    logo: str = Field(description="渠道图标")
    icon: str = Field(description="支付图标")
    sort: int = Field(description="排序编号")
    status: int = Field(ge=0, le=1, description="渠道状态: [0=禁用, 1=启用]")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "channel": 2,
                "shorter": "微信支付",
                "name": "微信支付",
                "logo": "https://www.xx.com/wx.png",
                "icon": "https://www.xx.com/wx.png",
                "status": 1
            }
        }


class PaymentDetailVo(BaseModel):
    """ 支付配置详情Vo """
    id: int = Field(description="ID")
    channel: int = Field(description="渠道别名")
    shorter: str = Field(description="简写名称")
    name: str = Field(description="渠道名称")
    icon: str = Field(description="支付图标")
    sort: int = Field(description="排序编号")
    status: int = Field(ge=0, le=1, description="渠道状态: [0=禁用, 1=启用]")
    params: dict = Field(default_factory=dict, description="支付配置")

    class Config:
        json_schema_extra = {
            "example": {
                "channel": 2,
                "shorter": "微信支付",
                "name": "微信支付",
                "logo": "https://www.xx.com/wx.png",
                "icon": "https://www.xx.com/wx.png",
                "status": 1,
                "params": {}
            }
        }

