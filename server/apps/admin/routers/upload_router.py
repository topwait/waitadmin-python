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
from fastapi import APIRouter, UploadFile, Form, Request
from hypertext import R, response_json
from apps.admin.service.upload_service import UploadService
from apps.admin.schemas.common_schema import UploadResultVo

router = APIRouter(prefix="/upload", tags=["上传接口"])


@router.post("/files", summary="上传文件", response_model=R[UploadResultVo])
@response_json
async def files(
        request: Request,
        file: UploadFile,
        cid: int = Form(ge=0, default=0),
        scene: str = Form(default="image"),
        is_attach: int = Form(ge=0, le=1, default=1),
) -> UploadResultVo:
    admin_id: int = request.state.admin_id
    return await UploadService.file(file, cid, scene, is_attach, admin_id)
