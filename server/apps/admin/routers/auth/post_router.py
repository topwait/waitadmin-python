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
from apps.admin.schemas.auth import post_schema as schema
from apps.admin.service.auth.post_service import PostService

router = APIRouter(prefix="/post", tags=["权限岗位"])


@router.get("/whole", summary="所有岗位", response_model=R[PagingResult[schema.AuthPostWholeVo]])
@response_json
async def whole():
    return await PostService.whole()


@router.get("/lists", summary="岗位列表", response_model=R[PagingResult[schema.AuthPostListVo]])
@response_json
async def lists(params: schema.AuthPostSearchIn = Depends()):
    return await PostService.lists(params)


@router.get("/detail", summary="岗位列表", response_model=R[schema.AuthPostDetailVo])
@response_json
async def detail(params: schema.AuthPostDetailIn = Depends()):
    return await PostService.detail(params.id)


@router.post("/add", summary="岗位新增", response_model=R)
@response_json
async def add(params: schema.AuthPostAddIn):
    return await PostService.add(params)


@router.post("/edit", summary="岗位编辑", response_model=R)
@response_json
async def add(params: schema.AuthPostEditIn):
    return await PostService.edit(params)


@router.post("/delete", summary="岗位删除", response_model=R)
@response_json
async def delete(params: schema.AuthPostDeleteIn):
    return await PostService.delete(params.id)

