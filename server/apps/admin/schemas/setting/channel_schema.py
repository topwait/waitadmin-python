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


class WxParams(BaseModel):
    """ 微信小程序参数 """
    name: str = Field(default="", max_length=500, description="小程序名称")
    original_id: str = Field(default="", max_length=500, description="原始ID")
    qr_code: str = Field(default="", max_length=500, description="二维码")
    app_id: str = Field(default="", max_length=500, description="AppID")
    app_secret: str = Field(default="", max_length=500, description="AppSecret")
    request_domain: str = Field(default="", description="request合法域名")
    socket_domain: str = Field(default="", description="socket合法域名")
    upload_file_domain: str = Field(default="", description="uploadFile合法域名")
    download_file_domain: str = Field(default="", description="downloadFile合法域名")
    udp_domain: str = Field(default="", description="udp合法域名")


class OaParams(BaseModel):
    """ 微信公众号参数 """
    name: str = Field(default="", max_length=500, description="公众号名称")
    original_id: str = Field(default="", max_length=500, description="原始ID")
    qr_code: str = Field(default="", max_length=500, description="二维码")
    app_id: str = Field(default="", max_length=500, description="AppID")
    app_secret: str = Field(default="", max_length=500, description="AppSecret")
    url: str = Field(default="", description="URL")
    token: str = Field(default="", description="Token")
    aes_key: str = Field(default="", description="EncodingAESKey")
    encryption_type: int = Field(default=1, ge=1, le=3, description="消息加密方式: [1=明文, 2=兼容, 3=安全]")
    wk_domain: str = Field(default="", description="业务域名")
    js_domain: str = Field(default="", description="JS接口安全域名")
    web_domain: str = Field(default="", description="网页授权域名")


class OpParams(BaseModel):
    """ 微信开放平台参数 """
    app_id: str = Field(default="", max_length=500, description="AppID")
    app_secret: str = Field(default="", max_length=500, description="AppSecret")


class ChannelDetailVo(BaseModel):
    """ 渠道配置详情Vo """
    wx: WxParams = Field(..., description="微信参数")
    oa: OaParams = Field(..., description="微信公众号参数")
    op: OpParams = Field(..., description="微信开放平台参数")

    class Config:
        json_schema_extra = {
            "example": {
                "wx": {
                    "name": "",
                    "original_id": "",
                    "qr_code": "",
                    "app_id": "",
                    "app_secret": "",
                    "request_domain": "https://www.xx.com",
                    "socket_domain": "https://www.xx.com",
                    "upload_file_domain": "https://www.xx.com",
                    "download_file_domain": "https://www.xx.com",
                    "udp_domain": "https://www.xx.com"
                },
                "oa": {
                    "name": "",
                    "original_id": "",
                    "qr_code": "",
                    "app_id": "wx43953855d03bf978",
                    "app_secret": "b5da9d44v314549b4c0d821679c70ab7",
                    "url": "https://www.xx.com",
                    "token": "wa",
                    "aes_key": "",
                    "encryption_type": 1,
                    "wk_domain": "https://www.xx.com",
                    "js_domain": "https://www.xx.com",
                    "web_domain": "https://www.xx.com"
                },
                "op": {
                    "app_id": "",
                    "app_secret": ""
                }
            }
        }
