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
import json
import time
import typing
import xmltodict
from fastapi import FastAPI, Request
from starlette.types import ASGIApp
from starlette.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from config import get_settings
from common.utils.tools import ToolsUtil
from common.models.sys import SysLogModel
from plugins.safe.driver import SecurityDriver


def init_middlewares(app: FastAPI):
    logs_middleware: typing.Type[any] = LogsMiddleware
    demo_middleware: typing.Type[any] = DemoMiddleware
    app.add_middleware(logs_middleware)
    app.add_middleware(demo_middleware)


class LogsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.STATUS_OK = 1
        self.STATUS_FAIL = 2

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 模块验证
        module: str = get_settings().ROUTER_ALIAS.get("admin", "admin")
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if request.state.module != module or endpoint.__module__ == "starlette.staticfiles":
            return await call_next(request)

        # 登录信息
        admin_id: int = int(await SecurityDriver.module("admin").get_login_id())
        role_id: int = int((await SecurityDriver.module("admin").get_login_data()).get("role_id", 0))
        request.state.admin_id = admin_id
        request.state.role_id = role_id

        # 忽略接口
        if request.method in ["GET", "OPTIONS"]:
            return await call_next(request)

        # 静态文件
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if endpoint.__module__ == "starlette.staticfiles":
            return await call_next(request)

        # 异常信息
        error: str = ""
        errno: any = None
        status: int = self.STATUS_OK
        start_time: float = time.time()

        # 请求参数
        if request.method == "POST":
            content_type: str = request.headers.get("content-type")
            if content_type.startswith("multipart/form-data"):
                args = ""
            elif content_type.startswith("application/xml"):
                form_params = await request.body()
                dict_params = xmltodict.parse(form_params)
                args = json.dumps([dict_params], ensure_ascii=False)
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
            error = str(e)
            errno = e
            status = self.STATUS_FAIL

        # 请求信息
        end_time: float = time.time()
        task_time: float = (end_time - start_time) * 1000
        summary: str = request.scope.get("route").summary if request.scope.get("route") else ""
        user_agent: str = request.headers.get("user-agent", "")

        # 保存记录
        await SysLogModel.create(
            admin_id=admin_id,
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


class DemoMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        # 模块验证
        module: str = get_settings().ROUTER_ALIAS.get("admin", "admin")
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if request.state.module != module or endpoint.__module__ == "starlette.staticfiles":
            return await call_next(request)

        # 允许通过
        uri: str = request.url.path.replace(f"/{module}/", "").replace("/", ":")
        if uri in ["login:check", "login:logout"]:
            return await call_next(request)

        # 演示拦截
        if get_settings().ENV_DEMO and request.method == "POST":
            admin_id = await SecurityDriver.module("admin").get_login_id()
            if int(admin_id) != 1:
                return JSONResponse({"code": 1, "msg": "演示环境不支持修改数据!", "data": []})

        # 执行逻辑
        return await call_next(request)
