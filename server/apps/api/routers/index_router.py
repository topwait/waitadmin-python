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
from hypertext import R, response_json
from apps.api.schemas import index_schema as schema
from apps.api.service.index_service import IndexService

router = APIRouter(prefix="/index", tags=["公共接口"])


@router.get("/homing", summary="主页数据", response_model=R[schema.ConfigVo])
@response_json
async def homing():
    return await IndexService.homing()


@router.get("/config", summary="全局配置", response_model=R[schema.ConfigVo])
@response_json
async def config():
    return await IndexService.config()


@router.get("/policy", summary="协议政策", response_model=R[schema.PolicyVo])
@response_json
async def policy(params: schema.QueryPolicyIn = Depends()):
    return await IndexService.policy(params.type)


@router.post("/send_sms", summary="发送短信", response_model=R)
@response_json
async def send_sms(params: schema.SendSmsIn):
    return await IndexService.send_sms(params.scene, params.mobile)


@router.post("/send_email", summary="发送邮件", response_model=R)
@response_json
async def send_email(params: schema.SendEmailIn):
    return await IndexService.send_email(params.scene, params.email)
