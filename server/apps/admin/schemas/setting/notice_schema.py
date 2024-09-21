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
from typing import Dict
from pydantic import BaseModel, Field


class NoticeDetailIn(BaseModel):
    id: int = Field(gt=0, description="ID")


class NoticeListVo(BaseModel):
    """ 通知配置列表参数 """
    id: int = Field(description="ID")
    scene: int = Field(description="通知场景")
    name: str = Field(description="通知场景")
    type: str = Field(description="通知类型")
    sys_status: int = Field(ge=0, le=2, description="系统通知")
    ems_status: int = Field(ge=0, le=2, description="邮件通知")
    sms_status: int = Field(ge=0, le=2, description="短信通知")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "scene": 101,
                "name": "免密登录验证码",
                "type": "验证码",
                "sys_status": 2,
                "ems_status": 2,
                "sms_status": 1
            }
        }


class NoticeDetailVo(BaseModel):
    """ 通知配置详情参数 """
    id: int = Field(description="ID")
    scene: int = Field(description="通知场景")
    name: str = Field(description="通知场景")
    type: str = Field(description="通知类型")
    client: str = Field(description="接收端口")
    remarks: str = Field(description="场景描述")
    variable: dict = Field(description="场景描述")
    sys_template: Dict[str, str] = Field(default_factory=dict, description="系统通知")
    ems_template: Dict[str, str] = Field(default_factory=dict, description="邮件通知")
    sms_template: Dict[str, str] = Field(default_factory=dict, description="短信通知")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "scene": 101,
                "name": "免密登录验证码",
                "type": "验证码",
                "client": "用户端",
                "remarks": "用户手机号码登录时发送",
                "variable": {
                    "code": "验证码"
                },
                "sys_template": {},
                "ems_template": {},
                "sms_template": {
                    "status": "1",
                    "content": "${code}",
                    "template_code": "SMS_182535543"
                }
            }
        }
