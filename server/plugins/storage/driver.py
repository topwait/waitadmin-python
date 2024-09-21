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
import os
import copy
import hashlib
import random
import time
import uuid
from typing import Union, Dict
from datetime import datetime
from fastapi import UploadFile
from exception import AppException
from config import get_settings
from common.utils.config import ConfigUtil
from plugins.storage.engine.local import LocalStorage
from plugins.storage.engine.qiniu import QiniuStorage
from plugins.storage.engine.aliyun import AliyunStorage
from plugins.storage.engine.qcloud import QCloudStorage
from pydantic import BaseModel, Field


class StorageDriver(object):
    """ 存储驱动类 """

    @classmethod
    async def upload(cls, file_in: UploadFile, root: str, stores: str, folder: str = "", synchro: bool = False):
        """
        异步上传文件到指定存储引擎。

        Args:
           file_in (UploadFile): 上传的文件对象。
           root (str): 存储根。
           stores (str): 存储仓库。
           folder (str): 存储目录。
           synchro (bool): OSS和本地同时存储。

        Returns:
           Dict[str, any]: 包含文件上传信息的字典,包含以下键：
               - ext (str): 文件扩展名。
               - name (str): 原始文件名。
               - size (int): 文件的大小。
               - path (str): 文件存储路径。

        Author:
            zero
        """
        # 获取文件信息
        file_size: int = cls.get_file_size(file_in)
        file_name: str = cls.__build_filename(file_in, stores, folder)
        origin_file_name: str = cls.__cropping_name(file_in.filename)
        origin_file_ext: str = origin_file_name.split(".")[-1].lower()

        # 验证上传信息
        # cls.__validate_file(file_in, file_size, file_type)

        # 调用上传服务
        engine: Union[LocalStorage, QiniuStorage, AliyunStorage, QCloudStorage] = await cls.__get_engine_class(root)
        if synchro and not isinstance(engine, LocalStorage):
            file = copy.deepcopy(file_in)
            await LocalStorage(root).upload(file, file_name)
        results = await engine.upload(file_in, file_name)

        # 是否上传成功
        if results is not None:
            raise AppException(results)

        # 返回上传信息
        return {
            "ext": origin_file_ext,
            "name": origin_file_name,
            "size": file_size,
            "path": file_name
        }

    @classmethod
    async def push(cls, path: str, key: str):
        """
        从本地文件路径上传。

        Args:
            path (str): 本地文件路径, 如: /www/image/aa.png。
            key (str):  保存文件名称, 如: storage/image/aa.png。

        Author:
            zero
        """
        engine: Union[LocalStorage, QiniuStorage, AliyunStorage, QCloudStorage] = await cls.__get_engine_class()
        results = engine.push(path, key)
        if results is not None:
            raise AppException(results)

    @classmethod
    async def fetch(cls, url: str, key: str):
        """
        从指定URL抓取文件上传。

        Args:
            url (str): 要抓取的URL, 如: https://www.xx.com/aa.png。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Author:
            zero
        """
        engine: Union[LocalStorage, QiniuStorage, AliyunStorage, QCloudStorage] = await cls.__get_engine_class()
        results = engine.fetch(url, key)
        if results is not None:
            raise AppException(results)

    @classmethod
    async def delete(cls, key: str):
        """
        删除指定的文件。

        Args:
            key (str): 要删除的文件key, 如: storage/image/aa.png。

        Author:
            zero
        """
        engine: Union[LocalStorage, QiniuStorage, AliyunStorage, QCloudStorage] = await cls.__get_engine_class()
        results = engine.delete(key)
        if results is not None:
            raise AppException(results)

    @classmethod
    def get_file_size(cls, file_in: UploadFile) -> int:
        """
        获取上传文件的大小(以字节为单位)。

        Args:
            file_in (UploadFile): 上传的文件对象。

        Returns:
            int: 文件的大小(字节数)。

        Author:
            zero
        """
        file_in.file.seek(0, os.SEEK_END)
        file_size = file_in.file.tell()
        file_in.file.seek(0, os.SEEK_SET)
        return file_size

    @classmethod
    def __build_filename(cls, file_in: UploadFile, stores: str, folder: str) -> str:
        """
        根据文件信息和类型构建文件名。

        Args:
            file_in (UploadFile): 上传的文件。
            stores (str): 存储仓库。
            folder (str): 存储目录。

        Returns:
            str: 构建后的文件名,包含文件类型、日期、哈希值和随机字符等。

        Author:
            zero
        """
        file_ext: str = file_in.filename.split(".")[-1].lower()
        save_pre: str = (stores + "/" + folder.strip("/")) if folder else stores

        date_str: str = datetime.now().strftime("%Y%m%d")
        rand_chars: str = "".join(random.sample(uuid.uuid4().hex, min(6, 10)))
        base_chars: str = uuid.uuid4().hex + datetime.now().strftime("%Y%m%d%H%M%S") + str(time.time())

        m = hashlib.md5()
        m.update(base_chars.encode("utf-8"))
        hash_str: str = m.hexdigest()
        path_name: str = save_pre + "/" + date_str + "/" + hash_str + rand_chars + "." + file_ext
        return path_name

    # @classmethod
    # def __validate_file(cls, file_in: UploadFile, file_size: int, file_type: str):
    #     """
    #     验证上传的文件是否符合要求。
    #
    #     Args:
    #         file_in (UploadFile): 上传的文件对象。
    #         file_size (int): 文件大小（字节）。
    #         file_type (str): 文件类型。
    #
    #     Raises:
    #         AppException
    #
    #     Author:
    #         zero
    #     """
    #     name: str = file_in.filename
    #     ext: str = name.split(".")[-1].lower()
    #
    #     if not ext:
    #         raise AppException("未知的文件类型")
    #
    #     if file_type not in ("image", "video", "audio", "package", "document"):
    #         raise AppException("不被支持的上传场景: %s" % file_type)
    #
    #     limits: Dict[str, Union[int, str]] = UploadSetting().limits.get(file_type, {})
    #     limit_ext: str = limits.get("ext", None)
    #     limit_size: int = int(limits.get("size", 0))
    #     if limit_ext and ext not in limit_ext:
    #         raise AppException(msg="不被支持的文件扩展: %s" % ext)
    #     if limit_size and file_size > limit_size:
    #         raise AppException(msg="传文件不能超出限制: %d M" % (limit_size / 1024 / 1024))

    @classmethod
    def __cropping_name(cls, filename: str) -> str:
        """
        裁剪文件名长度,确保文件名长度不超过180个字符。

        Args:
            filename (str): 原始文件名。

        Returns:
            str: 裁剪后的文件名。

        Author:
            zero
        """
        base_name = filename.rsplit(".", 1)[0]

        if len(base_name) > 180:
            base_name = base_name[:180]

        cropped_filename = f"{base_name}.{filename.rsplit('.', 1)[-1]}"
        return cropped_filename

    @classmethod
    async def __get_engine_class(cls, root: str = "public") -> Union[type(LocalStorage), QiniuStorage, AliyunStorage, QCloudStorage]:
        engine: str = await ConfigUtil.get("storage", "engine", "local")
        params: dict = await ConfigUtil.get("storage", engine, {})

        # 验证OSS参数
        if engine != "local":
            if not params:
                raise AppException("存储引擎配置参数错误(OSS)")
            if not params.get("bucket", ""):
                raise AppException("存储空间名称参数缺失(Bucket)")
            if not params.get("domain", ""):
                raise AppException("存储空间域名参数缺失(Domain)")
            if not params.get("access_key", ""):
                raise AppException("存储空间KEY参数缺失(ACCESS_KEY)")
            if not params.get("secret_key", ""):
                raise AppException("存储空间Secret参数缺失(SECRET_KEY)")

        # 获取上传引擎
        try:
            if engine == "local":
                return LocalStorage(root)
            elif engine == "qiniu":
                return QiniuStorage(params)
            elif engine == "aliyun":
                return AliyunStorage(params)
            elif engine == "qcloud":
                return QCloudStorage(params)
            else:
                raise Exception("未找到存储引擎: " + engine)
        except Exception as e:
            raise AppException(str(e))


# class UploadSetting(BaseModel):
#     """ 上传配置类 """
#     root: str = Field(default=get_settings().UPLOAD.get("root") or "")
#     path: str = Field(default=get_settings().UPLOAD.get("path") or "")
#     limits: Dict[str, Dict[str, str]] = Field(default=get_settings().UPLOAD.get("limits") or {})
