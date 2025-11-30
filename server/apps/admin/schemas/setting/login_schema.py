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
from typing import List
from pydantic import BaseModel, Field


class LoginConfig(BaseModel):
    """ 登录注册配置 """
    is_agreement: bool = Field(..., description="显示授权协议")
    default_method: str = Field(..., pattern=r"^(account|mobile|wx)$", description="默认登录方式")
    usable_channel: List[str] = Field(default=[], description="可用登录方式: [account, mobile, wx]")
    usable_register: List[str] = Field(default=[], description="允许注册方式: [account, mobile, email]")


class LoginDetailVo(BaseModel):
    """ 登录配置详情Vo """
    pc: LoginConfig = Field(..., description="PC端登录配置")

    class Config:
        json_schema_extra = {
            "example": {
                "pc": {
                    "is_agreement": True,
                    "default_method": "account",
                    "usable_channel": ["account", "mobile", "wx"],
                    "usable_register": ["account", "mobile", "email"]
                }
            }
        }
