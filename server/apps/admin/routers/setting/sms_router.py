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
from fastapi import APIRouter
from hypertext import R, response_json
from apps.admin.schemas.setting import sms_schema as schema
from apps.admin.service.setting.sms_service import SmsService


router = APIRouter(prefix="/sms", tags=["短信配置"])


@router.get("/lists", summary="短信配置列表", response_model=R[schema.SmsListVo])
@response_json
async def lists():
    return await SmsService.lists()


@router.get("/detail", summary="短信配置详情", response_model=R[schema.SmsDetailVo])
@response_json
async def detail(alias: str):
    return await SmsService.detail(alias)


@router.post("/save", summary="短信配置保存", response_model=R)
@response_json
async def save(params: schema.SmsDetailVo):
    return await SmsService.save(params)
