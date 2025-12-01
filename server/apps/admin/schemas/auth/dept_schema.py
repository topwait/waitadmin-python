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
from typing import Union, List
from fastapi import Query
from pydantic import BaseModel, Field


class AuthDeptSearchIn(BaseModel):
    """ 部门搜索参数 """
    name: Union[str, None] = Query(default=None, description="部门名称")
    mobile: Union[str, None] = Query(default=None, description="部门电话")
    is_disable: Union[bool, None] = Field(default=None, description="是否禁用")


class AuthDeptDetailIn(BaseModel):
    """ 部门详情参数 """
    id: int = Query(gt=0, description="部门ID")


class AuthDeptAddIn(BaseModel):
    """ 部门新增参数 """
    pid: int = Field(..., ge=0, description="上级主键")
    name: str = Field(..., min_length=1, max_length=100, description="部门名称")
    duty: str = Field(..., min_length=1, max_length=30, description="负责人名")
    mobile: str = Field(..., min_length=1, max_length=30, description="部门电话")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: bool = Field(default=False, description="是否禁用")

    @classmethod
    def messages(cls):
        return {
            "pid.missing": "请选择上级部门",
            "pid.ge": "上级部门选择异常",
            "name.min_length": "请填写部门名称",
            "name.max_length": "部门名称不能超出100个字符",
            "duty.min_length": "请填写负责人姓名",
            "duty.max_length": "负责姓名不能超出100个字符",
            "mobile.min_length": "请填写部门电话",
            "mobile.max_length": "部门电话不能超出30个字符",
            "sort.ge": "排序号不能少于0",
            "sort.le": "排序号不能大于999999",
            "is_disable.bool_parsing": "部门状态必须为布尔值"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "pid": 1,
                "name": "Microsoft",
                "duty": "Marco",
                "mobile": "13800138000",
                "sort": 0,
                "is_disable": False
            }
        }


class AuthDeptEditIn(BaseModel):
    """ 部门编辑参数 """
    id: int = Field(..., gt=0, description="部门ID")
    pid: int = Field(..., ge=0, description="上级主键")
    name: str = Field(..., max_length=100, description="部门名称")
    duty: str = Field(..., max_length=30, description="负责人名")
    mobile: str = Field(..., max_length=30, description="部门电话")
    sort: int = Field(ge=0, le=999999, default=0, description="排序编号")
    is_disable: bool = Field(default=False, description="是否禁用")

    @classmethod
    def messages(cls):
        return AuthDeptAddIn.messages()

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 1,
                "name": "Microsoft",
                "duty": "Marco",
                "mobile": "13800138000",
                "sort": 0,
                "is_disable": False
            }
        }


class AuthDeptDeleteIn(BaseModel):
    """ 部门删除参数 """
    id: int = Field(..., gt=0, description="部门ID", examples=[1])

    @classmethod
    def messages(cls):
        return {
            "id.missing": "id参数缺失"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1
            }
        }


"""--------------- Separator ---------------"""


class AuthDeptWholeVo(BaseModel):
    """ 所有部门Vo """
    id: int = Field(description="部门ID")
    pid: int = Field(description="父级ID")
    name: str = Field(description="部门名称")
    is_disable: bool = Field(description="是否禁用")
    children: Union["AuthDeptWholeVo", List, None] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "name": "Microsoft",
                "is_disable": False,
                "children": []
            }
        }


class AuthDeptListVo(BaseModel):
    """ 部门列表Vo """
    id: int = Field(description="部门ID")
    pid: int = Field(description="父级ID")
    name: str = Field(description="部门名称")
    mobile: str = Field(description="部门电话")
    duty: str = Field(description="负责人")
    sort: int = Field(description="排序编号")
    is_disable: bool = Field(description="是否禁用")
    create_time: str = Field(description="创建时间")
    update_time: str = Field(description="更新时间")
    children: Union["AuthDeptListVo", List, None] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "name": "Microsoft",
                "duty": "Marco",
                "mobile": "13800138000",
                "sort": 0,
                "is_disable": False,
                "create_time": "2024-04-18 15:30:01",
                "update_time": "2024-04-18 16:41:47",
                "children": []
            }
        }


class AuthDeptDetailVo(BaseModel):
    """ 部门详情Vo """
    id: int = Field(description="菜单ID")
    pid: int = Field(description="父级ID")
    name: str = Field(description="部门名称")
    duty: str = Field(description="负责人名")
    mobile: str = Field(description="部门电话")
    sort: int = Field(description="排序编号")
    is_disable: bool = Field(description="是否禁用")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "pid": 0,
                "name": "Microsoft",
                "duty": "Marco",
                "mobile": "13800138000",
                "sort": 0,
                "is_disable": False
            }
        }
