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


class WebsiteParams(BaseModel):
    """ 网站参数 """
    icp: str = Field(default="", max_length=500, description="ICP备案")
    pcp: str = Field(default="", max_length=500, description="公安备案")
    copyright: str = Field(default="", description="网站版权")
    analyse: str = Field(default="", description="统计代码")


class H5Params(BaseModel):
    """ H5端参数 """
    title: str = Field(default="", max_length=200, description="网站标题")
    logo: str = Field(default="", max_length=300, description="网站logo")
    status: int = Field(default=0, ge=0, le=1, description="启用状态: [0=关闭, 1=开启]")
    close_url: str = Field(default="", max_length=1000, description="关闭后访问地址")


class PcParams(BaseModel):
    """ Pc端参数 """
    favicon: str = Field(default="", max_length=250, description="网站图标")
    logo: str = Field(default="", max_length=250, description="网站logo")
    name: str = Field(default="", max_length=200, description="网站名称")
    title: str = Field(default="", max_length=200, description="网站标题")
    keywords: str = Field(default="", max_length=200, description="关键词组")
    description: str = Field(default="", max_length=500, description="关键词组")


class BasicsDetailVo(BaseModel):
    """ 网站配置Vo """
    website: WebsiteParams = Field(..., description="网站配置")
    h5: H5Params = Field(..., description="H5端配置")
    pc: PcParams = Field(..., description="PC端配置")

    class Config:
        json_schema_extra = {
            "example": {
                "website": {
                    "icp": "粤ICP备1542364号",
                    "pcp": "粤ICP备1542364号",
                    "copyright": "© 2023-2024 xxx工作室 版权所有 · www.xxx.cn",
                    "analyse": ""
                },
                "h5": {
                    "logo": "https://xx.com/images/logo.png",
                    "title": "this is WaitAdmin-Python",
                    "status": 1,
                    "close_url": ""
                },
                "pc": {
                    "favicon": "https://xx.com/images/favicon.icom",
                    "logo": "https://xx.com/images/logo.png",
                    "name": "this is web name",
                    "title": "this is WaitAdmin-Python",
                    "keyword": "",
                    "description": ""
                }
            }
        }
