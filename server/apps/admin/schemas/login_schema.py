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


class LoginCheckIn(BaseModel):
    """ 登录参数 """
    username: str = Field(..., min_length=4, max_length=20, description="登录账号")
    password: str = Field(..., min_length=6, max_length=20, description="登录密码")
    uuid: str = Field(max_length=38, default="", description="验证标识")
    code: str = Field(max_length=4, default="", description="登录验证码")

    @classmethod
    def messages(cls):
        return {
            "username.min_length": "账号或密码错误",
            "username.max_length": "账号或密码错误",
            "password.min_length": "账号或密码错误",
            "password.max_length": "账号或密码错误",
            "uuid.max_length": "验证标识异常",
            "code.max_length": "验证码错误"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "password": "123456",
                "uuid": "452f5e532a35d23a6b9cba0f548150d10JdQ9A",
                "code": "2opc"
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class LoginCaptchaVo(BaseModel):
    """ 登录验证码Vo """
    uuid: str = Field(description="UUID")
    image: str = Field(description="验证码")

    class Config:
        json_schema_extra = {
            "example": {
                "uuid": "a288117605958106e531e36708f6c0089hz8vx",
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJR...",
            }
        }


class LoginSuccessVo(BaseModel):
    """ 登录成功Vo """
    token: str = Field(description="登录令牌")
    username: str = Field(description="账号名称")
    nickname: str = Field(description="用户昵称")
    avatar: str = Field(description="用户头像")

    class Config:
        json_schema_extra = {
            "example": {
                "token": "252f5e532a35d73a6b5cba0f548150c10GdE68",
                "username": "admin",
                "nickname": "admin",
                "avatar": "https://www.xx.com/avatar.png"
            }
        }
