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


class BacksDetailVo(BaseModel):
    """ 网站配置Vo """
    name: str = Field(default="", max_length=30, description="网站名称")
    title: str = Field(default="", max_length=30, description="网站标题")
    cover: str = Field(default="", max_length=500, description="登录封面")
    favicon: str = Field(default="", max_length=500, description="网站图标")
    logo_black_big: str = Field(default="", max_length=500, description="深色大logo")
    logo_black_small: str = Field(default="", max_length=500, description="深色小logo")
    logo_white_big: str = Field(default="", max_length=500, description="浅色大logo")
    logo_white_small: str = Field(default="", max_length=500, description="浅色小logo")
    contacts: str = Field(default="", max_length=20, description="联系人名")
    mobile: str = Field(default="", max_length=20, description="联系电话")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "this is web name",
                "title": "this is web title",
                "cover": "https://xx.com/images/cover.png",
                "favicon": "https://xx.com/images/favicon.icom",
                "logo_black_big": "https://xx.com/images/logo_black_big.png",
                "logo_black_small": "https://xx.com/images/logo_black_small.png",
                "logo_white_big": "https://xx.com/images/logo_white_big.png",
                "logo_white_small": "https://xx.com/images/logo_white_small.png",
                "contacts": "wait",
                "mobile": "13800138000"
            }
        }
