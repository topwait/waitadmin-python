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
import time
import json
import typing
import xmltodict
from fastapi import FastAPI, Request
from starlette.types import ASGIApp
from starlette.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from config import get_settings
from .config import ApiConfig
from common.utils.tools import ToolsUtil
from common.models.users import UserVisitorModel
from plugins.safe.driver import SecurityDriver


def init_middlewares(app: FastAPI):
    logs_middleware: typing.Type[any] = LogsMiddleware
    app.add_middleware(logs_middleware)


class LogsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.STATUS_OK = 1
        self.STATUS_FAIL = 2

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 模块验证
        module: str = get_settings().ROUTER_ALIAS.get("api", "api")
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if request.state.module != module or endpoint.__module__ == "starlette.staticfiles":
            return await call_next(request)

        # 登录信息
        request.state.user_id = int(await SecurityDriver.module("api").get_login_id())
        request.state.terminal = int(request.headers.get("Terminal") or 0)

        # 无需记录
        uri: str = request.url.path.replace(f"/{module}/", "").replace("/", ":")
        if ApiConfig.add_record_log and uri not in ApiConfig.add_record_log:
            return await call_next(request)

        # 异常信息
        error: str = ""
        errno: any = None
        status: int = self.STATUS_OK
        start_time: float = time.time()

        # 请求参数
        if request.method == "POST":
            content_type: str = request.headers.get("content-type", "")
            if content_type.startswith("application/xml"):
                form_params = await request.body()
                dict_params = xmltodict.parse(form_params)
                args = json.dumps([dict_params], ensure_ascii=False)
            elif content_type.startswith("multipart/form-data"):
                args = ""
            else:
                form_params = await request.json()
                for key in ["password", "password_confirm", "password_old"]:
                    if form_params.get(key):
                        form_params[key] = "******"
                args = json.dumps([form_params], ensure_ascii=False)
        else:
            args = str(request.query_params)

        # 执行方法
        response = None
        try:
            response = await call_next(request)
        except Exception as e:
            errno = e
            error = str(e)
            status = self.STATUS_FAIL

        # 请求信息
        end_time: float = time.time()
        task_time: float = round(end_time - start_time, 3)
        summary: str = request.scope.get("route").summary if request.scope.get("route") else ""
        user_agent: str = request.headers.get("user-agent", "")

        await UserVisitorModel.create(
            user_id=request.state.user_id,
            terminal=request.state.terminal,
            summary=summary,
            endpoint=f"{endpoint.__module__}.{endpoint.__name__}()",
            method=request.method,
            url=request.url.path,
            ip=request.client.host,
            ua=ToolsUtil.to_user_agent(user_agent),
            user_agent=user_agent,
            params=args,
            error=error,
            status=status,
            start_time=start_time,
            end_time=end_time,
            task_time=task_time,
            create_time=int(time.time())
        )

        # 发送异常
        if errno:
            raise errno

        # 执行完成
        return response
