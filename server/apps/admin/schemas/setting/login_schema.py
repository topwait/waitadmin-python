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


class LoginDetailVo(BaseModel):
    """ 存储配置详情Vo """
    is_agreement: int = Field(..., ge=0, le=1, description="存储渠道")
    defaults: str = Field(..., description="默认登录方式")
    registers: List[str] = Field(..., description="允许注册方式")
    login_modes: List[str] = Field(..., description="通用登录方式")
    login_other: List[str] = Field(..., description="第三方登录")

    class Config:
        json_schema_extra = {
            "example": {
                "is_agreement": 1,
                "defaults": "account",
                "registers": ["mobile", "email"],
                "login_modes": ["account", "mobile"],
                "login_other": ["wx"]
            }
        }
