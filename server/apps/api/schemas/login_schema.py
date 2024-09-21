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


class RegisterIn(BaseModel):
    """ 账号注册参数 """
    scene: str = Field(..., min_length=1, pattern=r"^(mobile|email)$", description="注册场景: [mobile,email]")
    account: str = Field(..., min_length=1, max_length=80, description="登录账号")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")
    code: str = Field(..., min_length=6, max_length=20, description="验证码")

    class Config:
        json_schema_extra = {
            "example": {
                "scene": "mobile",
                "account": "13800138000",
                "password": "123456",
                "code": "628455"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "scene.min_length": "请选择注册场景",
            "scene.pattern": "注册场景不支持",
            "account.min_length": "请填写注册账号",
            "account.max_length": "账号不能大于80个字符",
            "password.min_length": "密码不能少于6个字符",
            "password.max_length": "密码不能大于20个字符",
            "code.min_length": "验证码错误",
            "code.max_length": "验证码错误"
        }


class AccountLoginIn(BaseModel):
    """ 账号登录参数 """
    account: str = Field(..., min_length=1, max_length=80, description="登录账号")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "13800138000",
                "password": "123456"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "account.min_length": "请填写登录账号",
            "account.max_length": "账号或密码错误",
            "password.min_length": "账号或密码错误",
            "password.max_length": "账号或密码错误"
        }


class MobileLoginIn(BaseModel):
    """ 手机登录参数 """
    mobile: str = Field(..., min_length=1, pattern=r"^(1[3-9]\d{9})?$", description="手机号")
    code: str = Field(..., min_length=6, max_length=20, description="验证码")

    class Config:
        json_schema_extra = {
            "example": {
                "mobile": "13800138000",
                "code": "265876"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "mobile.min_length": "请填写注册账号",
            "mobile.pattern": "手机号格式不正确",
            "code.min_length": "验证码错误",
            "code.max_length": "验证码错误"
        }


class OaLoginIn(BaseModel):
    """ 公众号登录参数 """
    state: str = Field(..., min_length=1, max_length=200, description="授权的唯一值")
    code: str = Field(..., min_length=1, max_length=200, description="微信的code")

    class Config:
        json_schema_extra = {
            "example": {
                "state": "27ab37b88696IflB",
                "code": "i8vd2VpeGluLnFxLmNvbS9"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "state.min_length": "state参数缺失",
            "state.max_length": "state参数异常",
            "code.min_length": "code参数缺失",
            "code.max_length": "code参数异常"
        }


class OaQrcodeIn(BaseModel):
    """ 微信二维码参数 """
    event: str = Field(..., pattern=r"^(login|bind)$", description="扫码场景: [login=登录, bind=绑定]")

    class Config:
        json_schema_extra = {
            "example": {
                "event": "login"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "scene.pattern": "二维码事件参数异常"
        }


class ScanLoginIn(BaseModel):
    """ 微信扫码参数 """
    # scene: str = Field(..., pattern=r"^(login|bind)$", description="扫码场景: [login=登录, bind=绑定]")
    state: str = Field(..., min_length=1, max_length=100, description="二维码密钥")

    class Config:
        json_schema_extra = {
            "example": {
                "state": "75672de284a4f44227f5c0cf5d151cb9Wvi41C"
            }
        }

    @classmethod
    def messages(cls):
        return {
            # "scene.pattern": "扫码场景参数异常",
            "state.min_length": "二维码密钥参数缺失",
            "state.max_length": "二维码密钥参数异常"
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class LoginTokenVo(BaseModel):
    """ 登录令牌Vo """
    token: str = Field(description="令牌")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "8b60a349771bGcb813e627ab37b88696IflBgj"
            }
        }


class LoginTicketVo(BaseModel):
    """ 登录扫码检测Vo """
    status: int = Field(default=0, description="状态: [0=等待扫码, 1=扫码失败, 2=扫码确认, 3=扫码成功]")
    expire: int = Field(default=0, description="时效")
    token: str = Field(default="", description="令牌")

    class Config:
        json_schema_extra = {
            "example": {
                "status": 0,
                "expire": 0,
                "token": "8b60a349771bGcb813e627ab37b88696IflBgj"
            }
        }


class LoginQrcodeVo(BaseModel):
    """ 公众号登录二维码 """
    key: str = Field(description="键")
    ticket: str = Field(description="票")
    url: str = Field(description="链接")
    expire_seconds: int = Field(description="有效秒数")

    class Config:
        json_schema_extra = {
            "example": {
                "key": "decc7a8719089456497e24412f815c8fdh2Hjt",
                "ticket": "gQFJ8DwAA5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAy",
                "url": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=gQFJ8DwAA5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAy",
                "expire_seconds": 120
            }
        }

