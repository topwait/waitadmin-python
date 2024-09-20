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
from pydantic import BaseModel, Field


class PolicyDetailVo(BaseModel):
    """ 协议配置详情Vo """
    service: str = Field(..., description="服务协议")
    privacy: str = Field(..., description="隐私协议")
    payment: str = Field(..., description="支付协议")

    class Config:
        json_schema_extra = {
            "example": {
                "service": "",
                "privacy": "",
                "payment": ""
            }
        }
