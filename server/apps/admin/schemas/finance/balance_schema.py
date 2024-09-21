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


class BalanceSearchIn(BaseModel):
    """ 余额明细搜索参数 """
    page_no: int = Query(gt=0, default=1, description="当前页码")
    page_size: int = Query(gt=0, le=200, default=15, description="每页条数")
    user: Union[str, None] = Query(default=None, description="用户信息")
    source_type: Union[str, int, None] = Query(default=None, description="来源类型")
    start_time: Union[int, str, None] = Query(default=None, description="开始时间")
    end_time: Union[int, str, None] = Query(default=None, description="结束时间")


"""---------------❤︎华丽分割线❤︎---------------"""


class BalanceListVo(BaseModel):
    """余额明细列表Vo """
    id: int = Field(description="文章ID")
    log_sn: str = Field(description="日志编号")
    action: int = Field(description="变动类型: [1=增加, 2=减少]")
    source_sn: str = Field(description="来源单号")
    source_type: str = Field(description="来源类型")
    change_amount: Decimal = Field(description="变动的金额")
    before_amount: Decimal = Field(description="变动前金额")
    after_amount: Decimal = Field(description="变动后金额")
    create_time: str = Field(description="创建时间")
    user: dict = Field(default="用户信息")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "log_sn": "202319254523567",
                "action": 1,
                "source_sn": "-",
                "source_type": "平台扣减余额",
                "change_amount": 0.01,
                "before_amount": 0.0,
                "after_amount": 0.0,
                "create_time": "2024-07-20 01:26:18",
                "user": {
                    "sn": "80965941",
                    "avatar": "http://0.0.0.0:8100/xiao.png",
                    "mobile": "13800138000",
                    "nickname": "xiao"
                }
            }
        }
