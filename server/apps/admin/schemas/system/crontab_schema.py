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
from typing import List, Dict
from fastapi import Query
from pydantic import BaseModel, Field


class CrontabSearchIn(BaseModel):
    """ 定时任务搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")


class CrontabDetailIn(BaseModel):
    """ 定时任务详情参数 """
    id: int = Query(..., gt=0, description="当前页码")


class CrontabAddIn(BaseModel):
    """ 定时任务新增参数 """
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    command: str = Field(..., min_length=1, max_length=200, description="执行命令")
    params: str = Field(max_length=200, default="", description="附带参数")
    trigger: str = Field(max_length=100, default="", description="触发类型")
    rules: List[dict] = Field(..., min_length=1, max_length=65535, description="运行规则")
    concurrent: int = Field(ge=1, le=10, default=0, description="并发数量")
    remarks: str = Field(max_length=255, default="", description="备注信息")
    status: int = Field(ge=0, le=1, default=0, description="执行状态: [1=运行, 2=暂停, 3=错误]")

    @classmethod
    def messages(cls):
        return {
            "name.min_length": "请填写任务名称",
            "name.max_length": "任务名称不能超出100个字符",
            "command.min_length": "请填写任务执行命令",
            "command.max_length": "执行命令不能超出200个字符",
            "params.max_length": "附带参数不能超出200个字符",
            "trigger.max_length": "触发类型类型不能超出200个字符",
            "rules.min_length": "请填写完善触发规则",
            "rules.max_length": "触发规则的长度不能超出65535个字符",
            "concurrent.ge": "并发数量最少不能少于1",
            "concurrent.le": "并发数量最大不能超出10",
            "remarks.max_length": "备注信息备注信息不能超出255个字符",
            "status.ge": "运行状态不符合规则: [1, 2, 3]",
            "status.le": "运行状态不符合规则: [1, 2, 3]"
        }

    class Config:
        json_schema_extra = {
            "example": {
                "name": "GC垃圾清理器",
                "command": "common.crontab.gc",
                "params": "",
                "trigger": "interval",
                "rules": [{"key": "weeks", "value": ""}],
                "concurrent": 1,
                "remarks": "",
                "status": 1
            }
        }


class CrontabEditIn(BaseModel):
    """ 定时任务编辑参数 """
    id: int = Field(..., gt=0, description="任务ID")
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    command: str = Field(..., min_length=1, max_length=200, description="执行命令")
    params: str = Field(max_length=200, default="", description="附带参数")
    trigger: str = Field(max_length=100, default="", description="触发类型")
    rules: List[dict] = Field(..., min_length=1, max_length=65535, description="运行规则")
    concurrent: int = Field(ge=1, le=10, default=0, description="并发数量")
    remarks: str = Field(max_length=255, default="", description="备注信息")
    status: int = Field(ge=0, le=1, default=0, description="执行状态: [1=运行, 2=暂停, 3=错误]")

    @classmethod
    def messages(cls):
        return CrontabAddIn.messages()

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "GC垃圾清理器",
                "command": "common.crontab.gc",
                "params": "",
                "trigger": "interval",
                "rules": [{"key": "weeks", "value": ""}],
                "concurrent": 1,
                "remarks": "",
                "status": 1
            }
        }


class CrontabListVo(BaseModel):
    """ 定时任务列表Vo """
    id: int = Field(description="任务ID")
    name: str = Field(description="任务名称")
    command: str = Field(description="命令")
    params: str = Field(description="参数")
    error: str = Field(description="错误原因")
    remarks: str = Field(description="备注信息")
    concurrent: int = Field(description="并发数量")
    status: int = Field(description="执行状态: [1=运行, 2=暂停, 3=错误]")
    exe_time: int = Field(description="执行时长")
    max_time: int = Field(description="最大执行时长")
    last_time: str = Field(description="最后执行时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "垃圾清理",
                "command": "gc",
                "params": "0 2 * * *",
                "error": "-",
                "remarks": "-",
                "concurrent": 1,
                "status": 1,
                "exe_time": 6,
                "max_time": 6,
                "last_time": "2024-04-18 11:22:33"
            }
        }


class CrontabDetailVo(BaseModel):
    """ 定时任务列表Vo """
    id: int = Field(description="任务ID")
    name: str = Field(description="任务名称")
    command: str = Field(description="命令")
    params: str = Field(description="参数")
    rules: List[dict] = Field(description="规则")
    remarks: str = Field(description="备注信息")
    concurrent: int = Field(description="并发数量")
    status: int = Field(description="执行状态: [1=运行, 2=暂停, 3=错误]")
    tasks: List[Dict[str, str]] = Field(description="任务列表")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "垃圾清理",
                "remarks": "用于清理系统垃圾",
                "command": "common.crontab.gc",
                "params": "{'text': 'wa'}",
                "concurrent": 1,
                "status": 1,
                "rules": [
                    {
                        "key": "seconds",
                        "value": "10"
                    }
                ],
                "tasks": [
                    {
                        "id": "common.crontab.gc.1",
                        "next_run_time": "2024-05-09 20:52:19"
                    }
                ]
            }
        }
