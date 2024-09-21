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
from fastapi import APIRouter, Request
from hypertext import R, response_json
from apps.admin.schemas import login_schema as schema
from apps.admin.service.login_service import LoginService

router = APIRouter(prefix="/login", tags=["登录系统"])


@router.get("/captcha", summary="登录验证码", response_model=R[schema.LoginCaptchaVo])
@response_json
async def captcha(request: Request):
    client_ip = request.client.host
    return await LoginService.captcha(client_ip)


@router.post("/check", summary="登录验证", response_model=R[schema.LoginSuccessVo])
@response_json
async def check(request: Request, params: schema.LoginCheckIn):
    return await LoginService.check(request, params)


@router.post("/logout", summary="退出系统", response_model=R)
@response_json
async def logout(request: Request):
    token: str = request.headers.get("authorization", "")
    await LoginService.logout(token)
