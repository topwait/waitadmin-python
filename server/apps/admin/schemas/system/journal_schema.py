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
from typing import Union
from fastapi import Query
from pydantic import BaseModel, Field


class JournalSearchIn(BaseModel):
    """ 系统日志搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    method: Union[str, None] = Query(default=None, description="请求方法: [GET, POST, PUT, DELETE, OPTION]")
    url: Union[str, None] = Query(default=None, description="访问地址")
    ip: Union[str, None] = Query(default=None, description="来源IP")
    start_time: Union[int, str, None] = Query(default=None, description="开始时间")
    end_time: Union[int, str, None] = Query(default=None, description="结束时间")


class JournalDetailIn(BaseModel):
    """ 系统日志详情参数 """
    id: int = Query(..., gt=0, description="日志ID")


class JournalListVo(BaseModel):
    """ 系统日志列表Vo """
    id: int = Field(description="任务ID")
    admin: str = Field(default="", description="操作人")
    summary: str = Field(description="摘要信息")
    method: str = Field(description="请求方式: [GET, POST, PUT, DELETE, OPTION]")
    url: str = Field(description="请求路由")
    ip: str = Field(description="请求IP")
    ua: str = Field(description="请求UA")
    error: str = Field(description="错误信息")
    status: int = Field(description="执行状态: [1=运行, 2=失败]")
    task_time: int = Field(description="最大执行时长")
    create_time: str = Field(description="操作时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 108,
                "admin": "admin",
                "summary": "日志列表",
                "method": "GET",
                "url": "/epi/system/journal/lists",
                "ip": "127.0.0.1",
                "ua": "chrome",
                "error": "",
                "status": 1,
                "task_time": 14,
                "create_time": "2024-05-10 15:26:42"
            }
        }


class JournalDetailVo(BaseModel):
    """ 系统日志详情Vo """
    id: int = Field(description="任务ID")
    nickname: str = Field(default="", description="操作昵称")
    username: str = Field(default="", description="操作账号")
    summary: str = Field(description="摘要信息")
    method: str = Field(description="请求方式: [GET, POST, PUT, DELETE, OPTION]")
    url: str = Field(description="请求路由")
    ip: str = Field(description="请求IP")
    ua: str = Field(description="请求UA")
    user_agent: str = Field(description="UA详情")
    endpoint: str = Field(description="执行函数")
    params: str = Field(description="请求参数")
    error: str = Field(description="错误信息")
    status: int = Field(description="执行状态: [1=运行, 2=失败]")
    task_time: int = Field(description="最大执行时长")
    start_time: str = Field(description="开始执行时间")
    end_time: str = Field(description="结束执行时间")
    create_time: str = Field(description="操作时间")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nickname": "小明",
                "username": "admin",
                "summary": "",
                "method": "GET",
                "url": "/epi/setting/basics/detail",
                "ip": "127.192.120.145",
                "ua": "chrome",
                "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "endpoint": "apps.admin.routers.setting.basics.detail()",
                "params": "",
                "error": "",
                "status": 0,
                "task_time": 9,
                "start_time": "2024-05-10 14:21:35.274679",
                "end_time": "2024-05-10 11:29:20.5019362",
                "create_time": "2024-05-10 11:29:20"
            }
        }
