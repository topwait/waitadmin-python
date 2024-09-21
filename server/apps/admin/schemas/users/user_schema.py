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
from typing import Union
from fastapi import Query
from pydantic import BaseModel, Field


class UserSessionIn(BaseModel):
    """ 会话列表参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=10, description="每页条数")
    user_id: int = Query(ge=0, efault=0, description="用户ID")
    scene: Union[str, None] = Query(default="all", description="场景: all=全部,online=在线,kick=已踢")


class UserWalletLogIn(BaseModel):
    """ 余额日志参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=10, description="每页条数")
    user_id: int = Query(..., ge=0, description="用户ID")


class UserSearchIn(BaseModel):
    """ 用户搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    keyword: Union[str, None] = Query(default=None, description="用户信息")
    is_disable: Union[str, None] = Query(default=None, description="是否禁用: [0=否, 1=是]")


class UserDetailIn(BaseModel):
    """ 用户详情参数 """
    id: int = Query(..., gt=0, description="用户ID")


class UserIdIn(BaseModel):
    """ 用户ID参数 """
    user_id: int = Field(..., gt=0, description="用户ID")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing": "请选择用户"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1
            }
        }


class UserEditIn(BaseModel):
    """ 编辑信息参数 """
    user_id: int = Field(..., gt=0, description="用户ID")
    field: str = Field(..., min_length=1, description="键")
    value: str = Field(..., min_length=1, description="值")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing":  "请选择修改的用户",
            "field.min_length": "请填写要修改字段",
            "value.min_length": "请填写要修改的值"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "field": "nickname",
                "value": "wait"
            }
        }


class UserKickOutIn(BaseModel):
    """ 强制下载参数 """
    user_id: int = Field(..., gt=0, description="用户ID")
    uuid: str = Field(..., min_length=1, description="UUID")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing": "请选择下载用户",
            "uuid.min_length": "请填写登录标识"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "uuid": "0934aca7-7a63-453b-8979-7b8ae4b3bdcc"
            }
        }


class UserChangeGroupIn(BaseModel):
    """ 修改分组参数 """
    user_id: int = Field(..., gt=0, description="用户ID")
    group_id: int = Field(..., ge=0, description="分组ID")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing":  "请选择用户",
            "group_id.missing": "请选择分组",
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "group_id": 1
            }
        }


class UserResetPasswordIn(BaseModel):
    """ 重置参数 """
    user_id: int = Field(..., gt=0, description="用户ID")
    password: str = Field(..., min_length=6, max_length=20, description="新密码")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing": "请选择用户",
            "password.min_length": "密码不能少于6个字符",
            "password.max_length": "密码不能大于20个字符"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "password": "123456"
            }
        }


class UserAdjustAccountIn(BaseModel):
    """ 重置参数 """
    user_id: int = Field(..., gt=0, description="用户ID")
    action: str = Field(..., pattern=r"^(inc|dec|final)$", description="操作")
    amount: Decimal = Field(..., max_digits=10, decimal_places=2, description="值")

    @classmethod
    def messages(cls):
        return {
            "user_id.missing": "请选择用户",
            "action.pattern": "操作类型不支持: [inc,dec,final]",
            "amount.max_digits": "变动的值整数部分不能超出8位",
            "amount.decimal_places": "变动的值只能保留2位小数",
        }

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "action": "inc",
                "amount": 10.40
            }
        }


"""---------------❤︎华丽分割线❤︎---------------"""


class UserListVo(BaseModel):
    """ 用户列表Vo """
    id: int = Field(description="用户ID")
    sn: str = Field(description="用户编号")
    group: str = Field(description="所属分组")
    nickname: str = Field(description="用户名称")
    avatar: str = Field(description="用户头像")
    mobile: str = Field(description="手机号码")
    email: str = Field(description="电子邮箱")
    is_disable: int = Field(description="是否显示: [0=否, 1=是]")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sn": "06275433",
                "group": "Gentleman",
                "avatar": "https://www.xxx.com/wait.png",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "is_disable": 0,
                "last_login_ip": "127.0.0.1",
                "last_login_time": "2024-04-18 11:22:33",
                "create_time": "2024-04-18 11:22:33",
                "update_time": "2024-04-18 11:22:33"
            }
        }


class UserDetailVo(BaseModel):
    """ 用户详情Vo """
    id: int = Field(description="用户ID")
    sn: str = Field(description="用户编号")
    account: str = Field(description="用户账号")
    nickname: str = Field(description="用户名称")
    avatar: str = Field(description="用户头像")
    gender: str = Field(description="用户性别")
    mobile: str = Field(description="手机号码")
    email: str = Field(description="电子邮箱")
    balance: float = Field(description="钱包余额")
    is_disable: int = Field(description="是否显示: [0=否, 1=是]")
    last_login_ip: str = Field(description="最后登录IP")
    last_login_time: str = Field(description="最后登录时间")
    create_time: str = Field(description="创建时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "sn": "06275433",
                "account": "wait",
                "avatar": "https://www.xxx.com/wait.png",
                "gender": "男",
                "mobile": "13800138000",
                "email": "13800138000@163.com",
                "is_disable": 0,
                "last_login_ip": "127.0.0.1",
                "last_login_time": "2024-04-18 11:22:33",
                "create_time": "2024-04-18 11:22:33"
            }
        }


class UserWalletLogsVo(BaseModel):
    """ 余额日志Vo """
    id: int = Field(description="记录ID")
    action: int = Field(description="操作类型: [1=增加, 2=减少]")
    op_user: str = Field(description="操作用户")
    log_sn: str = Field(description="日志编号")
    source_type: str = Field(description="来源类型")
    source_sn: str = Field(description="来源单号")
    change_amount: Decimal = Field(description="变动金额")
    before_amount: Decimal = Field(description="变动前金额")
    after_amount: Decimal = Field(description="变动后金额")
    remarks: str = Field(description="操作的备注")
    create_time: str = Field(description="创建时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "action": 2,
                "op_user": "admin",
                "log_sn": "20240626153658469907",
                "source_type": "平台扣减余额",
                "source_sn": "",
                "change_amount": 10.0,
                "before_amount": 70.0,
                "after_amount": 60.0,
                "remarks": "",
                "create_time": "2024-06-26 15:36:58"
              }
        }


class UserSessionListVo(BaseModel):
    """ 会话列表Vo """
    uuid: str = Field(description="标识")
    tips: str = Field(description="提示")
    device: str = Field(description="设备")
    status: int = Field(description="状态: [1=在线, 2=已失效, 2=踢下线]")
    login_host: str = Field(description="登录IP")
    surplus_time: str = Field(description="剩余时长")
    create_time: str = Field(description="创建时间")
    expire_time: str = Field(description="失效时间")
    last_op_time: str = Field(description="最后操作时间")
    last_ip_address: str = Field(description="最后操作IP")
    last_ua_browser: str = Field(description="最后操作UA")

    class Config:
        json_schema_extra = {
            "example": {
                "uuid": "67c089b9-6bba-4b46-ae5c-096e1e50b077",
                "tips": "在线",
                "device": "微信小程序",
                "status": 1,
                "login_host": "192.168.3.11",
                "create_time": "2024-06-26 16:42:56",
                "expire_time": "2024-06-26 18:42:56",
                "last_op_time": "2024-06-26 16:42:56",
                "last_ip_address": "127.0.0.1",
                "last_ua_browser": ""
            }
        }

