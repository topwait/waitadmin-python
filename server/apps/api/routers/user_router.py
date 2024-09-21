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
from apps.api.schemas import user_schema as schema
from apps.api.service.user_service import UserService

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/center", summary="个人中心", response_model=R[schema.UserCenterVo])
@response_json
async def center(request: Request):
    user_id: int = request.state.user_id
    return await UserService.center(user_id)


@router.get("/collect", summary="收藏列表", response_model=R[schema.UserCenterVo])
@response_json
async def collect(request: Request, params: schema.UserCollectSearchIn = Depends()):
    user_id: int = request.state.user_id
    return await UserService.collect(user_id, params)


@router.post("/edit", summary="编辑信息", response_model=R)
@response_json
async def edit(request: Request, params: schema.UserEditIn):
    user_id: int = request.state.user_id
    return await UserService.edit(
        params.field,
        params.value,
        user_id
    )


@router.post("/forget_pwd", summary="找回密码", response_model=R)
@response_json
async def forget_pwd(params: schema.UserForgetPwdIn):
    return await UserService.forget_pwd(
        params.code,
        params.mobile,
        params.password
    )


@router.post("/change_pwd", summary="修改密码", response_model=R)
@response_json
async def change_pwd(request: Request, params: schema.UserChangePwdIn):
    user_id: int = request.state.user_id
    return await UserService.change_pwd(
        params.old_pwd,
        params.new_pwd,
        user_id
    )


@router.post("/bind_mobile", summary="绑定手机", response_model=R)
async def bind_mobile(request: Request, params: schema.UserBindMobileIn):
    user_id: int = request.state.user_id
    return await UserService.bind_mobile(
        params.scene,
        params.mobile,
        params.code,
        user_id
    )


@router.post("/bind_email", summary="绑定邮箱", response_model=R)
@response_json
async def bind_email(request: Request, params: schema.UserBindEmailIn):
    user_id: int = request.state.user_id
    return await UserService.bind_email(
        params.scene,
        params.email,
        params.code,
        user_id
    )


@router.post("/bind_wechat", summary="绑定微信", response_model=R)
async def bind_wechat(request: Request, params: schema.UserBindWechatIn):
    user_id: int = request.state.user_id
    terminal: int = request.state.terminal
    return await UserService.bind_wechat(
        params.state,
        params.code,
        user_id,
        terminal
    )
