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
import shutil
import aiofiles
from typing import Union
from fastapi import UploadFile

SIZE = 2048


class LocalStorage:
    """ 本地存储 """

    def __init__(self, root_dir: str):
        self.root_dir: str = root_dir

    async def upload(self, file_in: UploadFile, key: str) -> Union[str, None]:
        """
        文件数据上传到本地存储。

        Args:
            file_in (UploadFile): 要上传的文件对象。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            if self.root_dir:
                key = self.root_dir + "/" + key

            dir_path = os.path.dirname(key)
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            async with aiofiles.open(key, "wb") as file_out:
                content = await file_in.read(SIZE)
                while content:
                    await file_out.write(content)
                    content = await file_in.read(SIZE)

            return None
        except Exception as e:
            return "Upload file failed: %s" % str(e)

    def push(self, path: str, key: str) -> Union[str, None]:
        """
        本地文件拷贝到指定目录。

        Args:
            path (str): 本地文件路径, 如: /www/image/aa.png。
            key (str):  保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            if self.root_dir:
                key = self.root_dir + "/" + key

            if not os.path.exists(path):
                return "The source file does not exist"

            dst_dir, _ = os.path.split(key)
            os.makedirs(dst_dir, exist_ok=True)

            shutil.copy2(path, key)
            return None
        except Exception as e:
            return str(e)

    def fetch(self, url: str, key: str) -> Union[str, None]:
        """
        从指定URL抓取文件并存储到本地。

        Args:
            url (str): 要抓取的URL, 如: https://www.xx.com/aa.png。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果抓取并保存成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            import urllib.request
            if self.root_dir:
                key = self.root_dir + "/" + key

            with urllib.request.urlopen(url) as response, open(key, "wb") as out_file:
                data = response.read()
                out_file.write(data)
        except Exception as e:
            return str(e)

    def delete(self, key: str) -> Union[str, None]:
        """
        删除指定的文件。

        Args:
            key (str): 要删除的文件key, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果删除成功返回None, 否则返回错误信息。
        """
        if self.root_dir:
            key = self.root_dir + "/" + key

        if os.path.exists(key):
            try:
                os.remove(key)
                return None
            except OSError as e:
                return f"Error: {key} : {e.strerror}"
