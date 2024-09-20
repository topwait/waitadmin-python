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


class SmsParams(BaseModel):
    """ 短信参数 """
    sign: str = Field(default="", description="短信签名")
    app_id: str = Field(default="", description="app_id")
    acc_key: str = Field(default="", description="key")
    acc_secret: str = Field(default="", description="secret")


class SmsListVo(BaseModel):
    """ 短信列表Vo """
    alias: str = Field(description="短信别名")
    name: str = Field(description="短信名称")
    desc: str = Field(description="短信描述")
    image: str = Field(description="短信图标")
    status: int = Field(ge=0, le=1, description="短信状态: [0=禁用, 1=启用]")

    class Config:
        json_schema_extra = {
            "example": {
                "alias": "aliyun",
                "name": "阿里云短信",
                "desc": "阿里云短信服务（Short Message Service）",
                "image": "http://0.0.0.0:8100/static/images/service_aliyun.png",
                "status": 1
            }
        }


class SmsDetailVo(BaseModel):
    """ 短信详情Vo """
    alias: str = Field(description="短信别名")
    name: str = Field(description="短信名称")
    status: int = Field(ge=0, le=1, description="短信状态: [0=禁用, 1=启用]")
    params: SmsParams = Field(description="短信参数")

    class Config:
        json_schema_extra = {
            "example": {
                "alias": "aliyun",
                "name": "阿里云短信",
                "status": 1,
                "params": {
                  "sign": "WaitAdmin",
                  "app_id": "867354488",
                  "acc_key": "LTtI2tFasBEVz5EroCj5NNsp",
                  "acc_secret": "E2bZ0Wh5EofT8u5FgsOFdlYdKnbWsz"
                }
              }
        }
