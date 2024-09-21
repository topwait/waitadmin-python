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
from fastapi import Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from exception import AppException
from common.enums.errors import ErrorEnum
from plugins.safe.driver import SecurityDriver
from apps.api.config import ApiConfig


obstruction: Dict[str, List[str]] = {
    "LoginInterceptor": ApiConfig.not_need_login
}


class LoginInterceptor:
    @staticmethod
    async def handler(request: Request, bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if endpoint.__module__ == "starlette.staticfiles":
            return True

        # 验登录状态
        token: str = bearer.credentials
        terminal: int = request.state.terminal
        status = await SecurityDriver.module("api").check_login(token, terminal)
        if status == "invalid":
            raise AppException(
                msg="登录失效",
                code=ErrorEnum.TOKEN_VALID.code
            )
        elif status == "disable":
            raise AppException(
                msg="您账号已被禁用",
                code=ErrorEnum.TOKEN_VALID.code
            )
        elif status == "kick":
            raise AppException(
                msg="您已被踢下线喇",
                code=ErrorEnum.TOKEN_VALID.code
            )

        return True
