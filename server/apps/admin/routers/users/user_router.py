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
from fastapi import APIRouter, Depends
from hypertext import R, PagingResult, response_json
from apps.admin.schemas.users import user_schema as schema
from apps.admin.service.users.user_service import UserService

router = APIRouter(prefix="/user", tags=["用户管理"])


@router.get("/sessions", summary="会话列表", response_model=R[PagingResult[schema.UserSessionListVo]])
@response_json
async def sessions(params: schema.UserSessionIn = Depends()):
    return await UserService.sessions(params)


@router.get("/wallet_logs", summary="余额日志", response_model=R[PagingResult[schema.UserWalletLogsVo]])
@response_json
async def wallet_logs(params: schema.UserWalletLogIn = Depends()):
    return await UserService.wallet_logs(params)


@router.get("/lists", summary="用户列表", response_model=R[schema.UserListVo])
@response_json
async def lists(params: schema.UserSearchIn = Depends()):
    return await UserService.lists(params)


@router.get("/detail", summary="用户详情", response_model=R[schema.UserDetailVo])
@response_json
async def detail(params: schema.UserDetailIn = Depends()):
    return await UserService.detail(params.id)


@router.post("/edit", summary="用户编辑", response_model=R)
@response_json
async def edit(params: schema.UserEditIn):
    return await UserService.edit(
        params.user_id,
        params.field,
        params.value
    )


@router.post("/blacklist", summary="拉黑名单", response_model=R)
@response_json
async def blacklist(params: schema.UserIdIn):
    return await UserService.blacklist(params.user_id)


@router.post("/change_group", summary="修改分组", response_model=R)
@response_json
async def change_group(params: schema.UserChangeGroupIn):
    return await UserService.change_group(
        params.user_id,
        params.group_id
    )


@router.post("/reset_password", summary="重置密码", response_model=R)
@response_json
async def reset_password(params: schema.UserResetPasswordIn):
    return await UserService.reset_password(
        params.user_id,
        params.password
    )


@router.post("/adjust_account", summary="调整账户", response_model=R)
@response_json
async def adjust_account(params: schema.UserAdjustAccountIn):
    return await UserService.adjust_account(
        params.user_id,
        params.action,
        params.amount
    )


@router.post("/kick_out", summary="强制下线", response_model=R)
@response_json
async def kick_out(params: schema.UserKickOutIn):
    return await UserService.kick_out(
        params.user_id,
        params.uuid
    )
