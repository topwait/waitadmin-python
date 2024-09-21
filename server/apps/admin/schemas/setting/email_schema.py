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


class EmailDetailVo(BaseModel):
    """ 邮箱配置详情Vo """
    smtp_type: str = Field(..., description="发送方式")
    smtp_host: str = Field(..., description="服务器地址")
    smtp_port: str = Field(..., description="服务器端口")
    smtp_user: str = Field(..., description="发件邮箱号")
    smtp_pass: str = Field(..., description="邮箱授权码")
    verify_type: str = Field(..., description="验证方式: [default,ssl]")

    class Config:
        json_schema_extra = {
            "example": {
                "smtp_type": "smtp",
                "smtp_host": "smtp.163.com",
                "smtp_port": 25,
                "smtp_user": "wa@163.com",
                "smtp_pass": "account",
                "verify_type": "MBK2JJF6OMR4VR2S"
            }
        }
