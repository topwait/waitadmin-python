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
from typing import Union, Dict
from fastapi import UploadFile
from qcloud_cos import CosConfig, CosS3Client, CosServiceError


class QCloudStorage:
    """ 腾讯云COS """

    def __init__(self, config: Dict[str, str]):
        self.bucket = config.get("bucket", "")
        self.domain = config.get("domain", "")
        self.region = config.get("region", "")
        self.access_key = config.get("access_key", "")
        self.secret_key = config.get("secret_key", "")

        self.conf = CosConfig(
            Region=self.region,
            SecretId=self.access_key,
            SecretKey=self.secret_key
        )

        self.client = CosS3Client(self.conf)

    async def upload(self, file_in: UploadFile, key: str):
        """
        文件数据上传到七牛云。

        Args:
            file_in (UploadFile): 要上传的文件对象。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            self.client.put_object(
                Bucket=self.bucket,
                Body=file_in.file,
                Key=key
            )
            return None
        except CosServiceError as e:
            return e.get_error_code() + ": " + e.get_error_msg()
        except Exception as e:
            return str(e)

    def push(self, path: str, key: str) -> Union[str, None]:
        """
        从本地文件路径上传文件到腾讯COS。

        Args:
            path (str): 本地文件路径, 如: /www/image/aa.png。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        with open(path, "rb") as f:
            content = f.read()
            try:
                self.client.put_object(
                        Bucket=self.bucket,
                        Body=content,
                        Key=key)
                return None
            except CosServiceError as e:
                return e.get_error_code() + ": " + e.get_error_msg()
            except Exception as e:
                return str(e)

    def fetch(self, url: str, key: str) -> Union[str, None]:
        """
        从指定URL抓取文件并存储到腾讯云COS。

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
            content = urllib.request.urlopen(url)
            self.client.put_object(
                Bucket=self.bucket,
                Body=content.read(),
                Key=key
            )
        except CosServiceError as e:
            return e.get_error_code() + ": " + e.get_error_msg()
        except Exception as e:
            return str(e)

    def delete(self, key: str) -> Union[str, None]:
        """
        从腾讯云COS中删除。

        Args:
            key (str): 文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果抓取并保存成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            self.client.delete_object(Bucket=self.bucket, Key=key)
            return None
        except CosServiceError as e:
            return e.get_error_code() + ": " + e.get_error_msg()
        except Exception as e:
            return str(e)
