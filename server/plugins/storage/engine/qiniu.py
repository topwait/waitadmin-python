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
import json
from typing import Union, Dict
from fastapi import UploadFile
from qiniu import Auth, BucketManager, put_data, put_file


class QiniuStorage:
    """ 七牛云OSS """

    def __init__(self, config: Dict[str, str]):
        self.bucket = config.get("bucket", "")
        self.domain = config.get("domain", "")
        self.ak = config.get("access_key", "")
        self.sk = config.get("secret_key", "")
        self.auth = Auth(self.ak, self.sk)

    async def upload(self, file_in: UploadFile, key: str) -> Union[str, None]:
        """
        文件数据上传到七牛云OSS。

        Args:
            file_in (UploadFile): 要上传的文件对象。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            token = self.auth.upload_token(self.bucket, key)
            response = put_data(token, key=key, data=file_in.file)
            return self.__handle_error(response, "put_file")
        except Exception as e:
            return str(e)

    def push(self, path: str, key: str) -> Union[str, None]:
        """
        本地文件上传到七牛云OSS。

        Args:
            path (str): 本地文件路径, 如: /www/image/aa.png。
            key (str):  保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            token = self.auth.upload_token(self.bucket, key)
            response = put_file(token, key=key, file_path=path)
            return self.__handle_error(response, "put_file")
        except Exception as e:
            return str(e)

    def fetch(self, url: str, key: str) -> Union[str, None]:
        """
        从指定URL抓取文件并存储到七牛云OSS。

        Args:
            url (str): 要抓取的URL, 如: https://www.xx.com/aa.png。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果抓取并保存成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            bucket = BucketManager(self.auth)
            response = bucket.fetch(key=key, bucket=self.bucket, url=url)
            return self.__handle_error(response, "fetch")
        except Exception as e:
            return str(e)

    def delete(self, key: str) -> Union[str, None]:
        """
        从七牛云删除指定key的文件。

        Args:
            key (str): 要删除的文件key, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果删除成功返回None, 否则返回错误信息。
        """
        try:
            bucket = BucketManager(self.auth)
            response = bucket.delete(bucket=self.bucket, key=key)
            return self.__handle_error(response, "delete")
        except Exception as e:
            return str(e)

    @staticmethod
    def __handle_error(response, scene: str) -> Union[str, None]:
        """
        处理响应错误。

        Args:
           response: 请求响应结果。
           scene (str): 操作场景名称。

        Returns:
            Union[str, None]: 如果删除成功返回None,否则返回错误信息。
        """
        if response and response[1].status_code != 200:
            try:
                error = json.loads(response[1].error).get("error")
                if scene == "delete" and error == "no such file or directory":
                    return None
                return str(response[1].status_code) + ": " + error
            except json.JSONDecodeError as e:
                return f"Upload {scene} error decoding JSON: {e}"
            except Exception as e:
                return f"Upload {scene} an unexpected error occurred: {e}"
        return None
