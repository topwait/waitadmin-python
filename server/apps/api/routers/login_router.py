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
from fastapi import APIRouter, Request, Depends
from hypertext import R, response_json
from apps.api.schemas import login_schema as schema
from apps.api.service.login_service import LoginService

router = APIRouter(prefix="/login", tags=["登录管理"])


@router.post("/register", summary="账号注册", response_model=R[schema.LoginTokenVo])
@response_json
async def register(request: Request, params: schema.RegisterIn):
    terminal: int = request.state.terminal
    return await LoginService.register(params, terminal)


@router.post("/account_login", summary="账号登录", response_model=R[schema.LoginTokenVo])
@response_json
async def account_login(request: Request, params: schema.AccountLoginIn):
    terminal: int = request.state.terminal
    return await LoginService.account_login(
        params.account,
        params.password,
        terminal
    )


@router.post("/mobile_login", summary="手机登录", response_model=R[schema.LoginTokenVo])
@response_json
async def mobile_login(request: Request, params: schema.MobileLoginIn):
    terminal: int = request.state.terminal
    return await LoginService.mobile_login(
        params.mobile,
        params.code,
        terminal
    )


@router.post("/oa_login", summary="公众号授权登录", response_model=R[schema.LoginTokenVo])
@response_json
async def oa_login(request: Request, params: schema.OaLoginIn):
    terminal: int = request.state.terminal
    return await LoginService.oa_login(
        params.state,
        params.code,
        terminal
    )


@router.get("/qrcode", summary="微信登录二维码", response_model=R[schema.LoginQrcodeVo])
@response_json
async def qrcode(params: schema.OaQrcodeIn = Depends()):
    return await LoginService.qrcode(params.event)


@router.get("/ticket", summary="微信登录扫码检测", response_model=schema.LoginTicketVo)
@response_json
async def ticket(params: schema.ScanLoginIn = Depends()):
    return await LoginService.ticket(params.state)


@router.post("/logout", summary="退出系统", response_model=R)
@response_json
async def logout(request: Request):
    token = request.headers.get("aa", "")
    return await LoginService.logout(token)
