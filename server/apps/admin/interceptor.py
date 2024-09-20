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
from config import get_settings
from common.enums.errors import ErrorEnum
from apps.admin.cache.login_cache import LoginCache
from apps.admin.config import AdminConfig
from plugins.safe.driver import SecurityDriver


obstruction: Dict[str, List[str]] = {
    "LoginInterceptor": AdminConfig.not_need_login,
    "PermsInterceptor": AdminConfig.not_need_perms
}


class LoginInterceptor:
    @staticmethod
    async def handler(request: Request, bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        endpoint: any = request.scope.get("endpoint", lambda: None)
        if endpoint.__module__ == "starlette.staticfiles":
            return True

        token: str = bearer.credentials
        status = await SecurityDriver.module("admin").check_login(token)
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


class PermsInterceptor:
    @staticmethod
    async def handler(request: Request):
        module: str = get_settings().ROUTER_ALIAS.get("admin", "admin")
        uri: str = request.url.path.replace(f"/{module}/", "").replace("/", ":")
        admin_id: int = request.state.admin_id
        role_id: int = request.state.role_id

        # 免登录验证接口
        if uri in AdminConfig.not_need_login:
            return True

        # 免权限验证接口
        if uri in AdminConfig.not_need_perms or admin_id == 1:
            return True

        # 查询角色的权限
        perms: List[str] = await LoginCache.role_perms_get(role_id)
        if uri not in perms:
            raise AppException(
                msg=ErrorEnum.PERMISSIONS_ERROR.msg,
                code=ErrorEnum.PERMISSIONS_ERROR.code
            )

        return True
