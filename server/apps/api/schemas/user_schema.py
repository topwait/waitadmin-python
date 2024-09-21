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
from decimal import Decimal
from fastapi import Query
from pydantic import BaseModel, Field


class UserCollectSearchIn(BaseModel):
    """ 文章搜索参数 """
    page: int = Query(gt=0, default=1, description="当前页码")


class UserEditIn(BaseModel):
    """ 编辑信息参数 """
    field: str = Field(..., min_length=1, max_length=100, description="键")
    value: str = Field(..., min_length=1, max_length=300, description="值")

    class Config:
        json_schema_extra = {
            "example": {
                "field": "account",
                "value": "wait"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "field.min_length": "请填写要修改的字段",
            "field.max_length": "填写的字段名称异常",
            "value.min_length": "请填写对应字段需修改的值",
            "value.max_length": "修改的值不能超300个字符"
        }


class UserForgetPwdIn(BaseModel):
    """ 忘记密码参数 """
    code: str = Field(min_length=6, max_length=20, description="验证码")
    mobile: str = Field(min_length=1, pattern=r"^(1[3-9]\d{9})?$", description="手机号")
    password: str = Field(min_length=6, max_length=20, description="新密码")

    class Config:
        json_schema_extra = {
            "example": {
                "account": "13800138000",
                "password": "123456",
                "code": "628455"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "mobile.min_length": "请填写手机号",
            "mobile.pattern": "手机号格式不正确",
            "password.min_length": "新密码不能少于6个字符",
            "password.max_length": "新密码不能大于20个字符",
            "code.min_length": "验证码错误",
            "code.max_length": "验证码错误"
        }


class UserChangePwdIn(BaseModel):
    """ 修改密码参数 """
    old_pwd: str = Field(min_length=6, max_length=20, description="旧密码")
    new_pwd: str = Field(min_length=6, max_length=20, description="新密码")

    class Config:
        json_schema_extra = {
            "example": {
                "old_pwd": "123456",
                "new_pwd": "123457"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "old_pwd.min_length": "旧密码错误",
            "old_pwd.max_length": "旧密码错误",
            "new_pwd.min_length": "新密码不能少于6个字符",
            "new_pwd.max_length": "新密码不能大于20个字符",
        }


class UserBindMobileIn(BaseModel):
    """ 绑定手机参数 """
    scene: str = Field(min_length=1, description="场景: [change,bind]")
    mobile: str = Field(min_length=1, pattern=r"^(1[3-9]\d{9})?$", description="手机号")
    code: str = Field(min_length=6, max_length=20, description="验证码")

    class Config:
        json_schema_extra = {
            "example": {
                "scene": "change",
                "mobile": "13800138000",
                "code": "628455"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "scene.min_length": "绑定场景缺失: [change,bind]",
            "mobile.min_length": "请填写手机号",
            "mobile.pattern": "手机号格式不正确",
            "code.min_length": "验证码错误",
            "code.max_length": "验证码错误"
        }


class UserBindEmailIn(BaseModel):
    """ 绑定邮箱参数 """
    scene: str = Field(min_length=1, description="场景: [change,bind]")
    email: str = Field(min_length=1, description="邮箱号: [change,bind]")
    code: str = Field(min_length=4, max_length=20, description="验证码")

    class Config:
        json_schema_extra = {
            "example": {
                "scene": "change",
                "email": "wait@163.com",
                "code": "628455"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "scene.min_length": "绑定场景缺失: [change,bind]",
            "email.min_length": "请填写邮箱号",
            "email.pattern": "邮箱号格式不正确",
            "code.min_length": "验证码错误",
            "code.max_length": "验证码错误"
        }


class UserBindWechatIn(BaseModel):
    """ 绑定微信参数 """
    state: str = Field(default="", max_length=200, description="公众号盐,小程序是不需要")
    code: str = Field(..., min_length=1, max_length=64, description="微信Code")

    class Config:
        json_schema_extra = {
            "example": {
                "state": "27ab37b88696IflB",
                "code": "8b60a349771bdEb813e627ab37b88696IflBgj"
            }
        }

    @classmethod
    def messages(cls):
        return {
            "state.max_length": "state参数异常",
            "code.min_length": "code微信参数错误",
            "code.max_length": "code微信参数错误"
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class UserCenterVo(BaseModel):
    """ 个人中心Vo """
    id: int = Field(description="用户ID")
    sn: str = Field(description="用户编号")
    account: str = Field(description="用户账号")
    nickname: str = Field(description="用户名称")
    avatar: str = Field(description="用户头像")
    mobile: str = Field(description="手机号码")
    email: str = Field(description="电子邮箱")
    collect: int = Field(description="收藏数量")
    balance: Decimal = Field(default=0, description="钱包余额")
    gender: int = Field(default=0, description="用户性别: [0=未知, 1=男, 2=女]")
    is_wechat: int = Field(default=0, description="已绑微信: [0=否, 1=是]")
    is_password: int = Field(default=0, description="已设密码: [0=否, 1=是]")
    create_time: str = Field(default="", description="注册时间")
    last_login_time: str = Field(default="", description="最后登录时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sn": "38604409",
                "account": "wait",
                "nickname": "u38604409",
                "avatar": "https://wa.com/static/avatar.png",
                "mobile": "13800138000",
                "email": "13800@163.com",
                "collect": 0,
                "balance": 0.0,
                "gender": 0,
                "is_wechat": 0,
                "is_password": 0,
                "create_time": "2023-12-20 11:27:05",
                "last_login_time": "2023-12-20 11:27:05"
            }
        }


class UserCollectVo(BaseModel):
    """ 文章收藏Vo """
    id: int = Field(description="收藏ID")
    image: str = Field(description="封面图")
    title: str = Field(description="文章标题")
    browse: int = Field(description="阅读量")
    collect: int = Field(description="收藏量")
    create_time: str = Field(description="收藏时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "image": "https://wa.com/static/article.png",
                "title": "this is title",
                "browse": 10,
                "collect": 15,
                "last_login_time": "2023-12-20 11:27:05"
            }
        }
