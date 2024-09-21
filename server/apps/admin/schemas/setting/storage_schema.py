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


class StorageParams(BaseModel):
    """ 存储参数 """
    bucket: str = Field(default="", description="存储空间名称")
    domain: str = Field(default="", description="访问空间域名")
    access_key: str = Field(default="", description="ACCESS_KEY")
    secret_key: str = Field(default="", description="SECRET_KEY")
    region: str = Field(default="", description="REGION")


class StorageDetailVo(BaseModel):
    """ 存储配置详情Vo """
    drive: str = Field(..., description="存储渠道")
    local: dict = Field(..., default_factory=dict, description="本地存储")
    qiniu: StorageParams = Field(..., description="七牛云存储")
    aliyun: StorageParams = Field(..., description="阿里云存储")
    qcloud: StorageParams = Field(..., description="腾讯云存储")

    class Config:
        json_schema_extra = {
            "example": {
                "drive": "local",
                "local": {},
                "qiniu": {
                    "bucket": "wa",
                    "domain": "https://qiniu.wa.com",
                    "access_key": "Eg223XdJz3xX8pwJaWavP60PvGAXoNiU34eKEcE2",
                    "secret_key": "5CrRiNj8WVHwkPdtDOGhwR5NTCuuGIrKeNDQt3-h",
                    "region": ""
                },
                "aliyun": {
                    "bucket": "",
                    "domain": "",
                    "access_key": "",
                    "secret_key": "",
                    "region": ""
                },
                "qcloud": {
                    "bucket": "",
                    "domain": "",
                    "access_key": "",
                    "secret_key": "",
                    "region": ""
                }
            }
        }
