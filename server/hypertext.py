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
import math
import inspect
from functools import wraps
from typing import Generic, TypeVar, Sequence, Callable, Any
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from common.enums.errors import ErrorEnum

T = TypeVar("T")


class R(BaseModel, Generic[T]):
    """ 响应工具类 """
    code: int = Field(default=ErrorEnum.SUCCESS.code, description="状态")
    msg: str = Field(default=ErrorEnum.SUCCESS.msg, description="提示")
    data: T = Field(default=[T], description="数据")

    @classmethod
    def success(cls, msg: str = "OK", data: Any = None, code: int = 0):
        if data is None:
            data = []
        return cls(code=code, msg=msg, data=data)

    @classmethod
    def fail(cls, msg: str = "FAIL", data: Any = None, code: int = 1):
        if data is None:
            data = []
        return cls(code=code, msg=msg, data=data)


class PagingResult(BaseModel, Generic[T]):
    """ 分页结果封装 """
    current_page: int = Field(default=1, description="当前页码")
    last_page: int = Field(default=1, description="最后页码")
    per_page: int = Field(default=20, description="每页数据")
    total: int = Field(default=1, description="数据总量")
    extend: Sequence[T] = Field(default=[], description="扩展信息")
    lists: Sequence[T] = Field(description="分页数据")

    @classmethod
    def create(cls, data: Sequence[T], total: int, page_no: int, page_size: int) -> "PagingResult[T]":
        last_page = math.ceil(total / page_size)
        return cls(lists=data, total=total, current_page=page_no, per_page=page_size, last_page=last_page)


def response_json(func: Callable[..., T]) -> Callable[..., T]:
    """ 统一响应格式 """
    @wraps(func)
    async def wrapper(*args, **kwargs) -> T:
        if inspect.iscoroutinefunction(func):
            resp = await func(*args, **kwargs) or []
        else:
            resp = func(*args, **kwargs) or []
        return JSONResponse(
            content=jsonable_encoder(
                R.success(data=resp).dict(),
                by_alias=False
            ),
            media_type="application/json;charset=utf-8"
        )

    return wrapper
