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
from apps.admin.schemas.system import crontab_schema as schema
from apps.admin.service.system.crontab_service import CrontabService

router = APIRouter(prefix="/crontab", tags=["定时任务"])


@router.get("/lists", summary="定时任务列表", response_model=R[PagingResult[schema.CrontabListVo]])
@response_json
async def lists(params: schema.CrontabSearchIn = Depends()):
    return await CrontabService.lists(params)


@router.get("/detail", summary="定时任务详情", response_model=R[schema.CrontabDetailVo])
@response_json
async def detail(params: schema.CrontabDetailIn = Depends()):
    return await CrontabService.detail(params.id)


@router.post("/add", summary="定时任务新增", response_model=R)
@response_json
async def add(params: schema.CrontabAddIn):
    await CrontabService.add(params)


@router.post("/edit", summary="定时任务编辑", response_model=R)
@response_json
async def edit(params: schema.CrontabEditIn):
    await CrontabService.edit(params)


@router.post("/delete", summary="定时任务删除", response_model=R)
@response_json
async def delete(params: schema.CrontabDetailIn):
    await CrontabService.delete(params.id)


@router.post("/stop", summary="定时任务停止", response_model=R)
@response_json
async def stop(params: schema.CrontabDetailIn):
    await CrontabService.delete(params.id)


@router.post("/run", summary="定时任务运行", response_model=R)
@response_json
async def run(params: schema.CrontabDetailIn):
    await CrontabService.delete(params.id)

