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
from typing import List

from fastapi import APIRouter, Depends
from hypertext import R, response_json
from apps.admin.schemas.setting import notice_schema as schema
from apps.admin.service.setting.notice_service import NoticeService


router = APIRouter(prefix="/notice", tags=["通知配置"])


@router.get("/lists", summary="通知配置列表", response_model=R[List[schema.NoticeListVo]])
@response_json
async def lists():
    return await NoticeService.lists()


@router.get("/detail", summary="通知配置详情", response_model=R[schema.NoticeDetailVo])
@response_json
async def detail(params: schema.NoticeDetailIn = Depends()):
    return await NoticeService.detail(params.id)


@router.post("/save", summary="通知配置保存", response_model=R)
@response_json
async def save(params: schema.NoticeDetailVo):
    return await NoticeService.save(params)
