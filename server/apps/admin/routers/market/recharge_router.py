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
from typing import List, Dict, Union
from fastapi import APIRouter, Depends
from hypertext import R, response_json
from apps.admin.schemas.market import recharge_schema as schema
from apps.admin.service.market.recharge_service import RechargeService

router = APIRouter(prefix="/recharge", tags=["充值套餐"])


@router.get("/lists", summary="充值套餐列表", response_model=R[Dict[str, Union[schema.RechargeConfigIn, schema.RechargePackageListVo]]])
@response_json
async def lists():
    return await RechargeService.lists()


@router.get("/detail", summary="充值套餐详情", response_model=R[List[schema.RechargePackageDetailVo]])
@response_json
async def detail(params: schema.RechargePackageDetailIn = Depends()):
    return await RechargeService.detail(params.id)


@router.post("/add", summary="充值套餐新增", response_model=R)
@response_json
async def add(params: schema.RechargePackageAddIn):
    return await RechargeService.add(params)


@router.post("/edit", summary="充值套餐编辑", response_model=R)
@response_json
async def edit(params: schema.RechargePackageEditIn):
    return await RechargeService.edit(params)


@router.post("/delete", summary="充值套餐删除", response_model=R)
@response_json
async def delete(params: schema.RechargePackageDeleteIn):
    return await RechargeService.delete(params.id)


@router.post("/config", summary="充值配置修改", response_model=R)
@response_json
async def config(params: schema.RechargeConfigIn):
    return await RechargeService.config(params)
