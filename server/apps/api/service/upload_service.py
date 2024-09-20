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
import time
from fastapi import UploadFile
from config import get_settings
from exception import AppException
from common.utils.urls import UrlUtil
from common.enums.attach import AttachEnum
from common.models.attach import AttachModel
from plugins.storage.driver import StorageDriver
from apps.api.schemas.index_schema import UploadResultVo


class UploadService:
    """ 上传服务类 """

    @classmethod
    async def files(cls, file_in: UploadFile, scene: str, user_id: int):
        """
        上传文件。

        Args:
            file_in (UploadFile): 文件对象。
            scene (str): 上传场景。
            user_id (int): 用户ID。

        Returns:
            UploadResultVo: 上传结果Vo。

        Author:
            zero
        """
        root: str = get_settings().UPLOAD.get("root", "") or ""
        path: str = get_settings().UPLOAD.get("path", "") or ""
        limits: dict = get_settings().UPLOAD.get("limits", {}) or {}

        fileSize: int = StorageDriver.get_file_size(file_in)
        fileExt: str = file_in.filename.split(".")[-1].lower()
        if limits.get(scene):
            where = limits.get(scene, {})
            _size = where.get("size") or 0
            _ext = where.get("ext") or []
            if _size and fileExt not in _ext:
                raise AppException(msg="不被支持的文件扩展: %s" % fileExt)
            if _ext and fileSize > _size:
                raise AppException(msg="传文件不能超出限制: %d M" % (_size / 1024 / 1024))
        else:
            raise AppException(f"不被支持的上传场景: {scene}")

        result = await StorageDriver.upload(file_in, root, path, scene)

        attach = await AttachModel.create(
            uid=user_id,
            cid=0,
            file_type=AttachEnum.get_code_by_msg(scene),
            file_name=result.get("name"),
            file_path=result.get("path"),
            file_size=result.get("size"),
            file_ext=result.get("ext"),
            is_user=1,
            is_attach=0,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        return UploadResultVo(
            id=attach.id,
            name=attach.file_name,
            size=attach.file_size,
            ext=attach.file_ext,
            path=attach.file_path,
            url=await UrlUtil.to_absolute_url(attach.file_path)
        )
