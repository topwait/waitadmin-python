# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin_fastapi
# | github:  https://github.com/topwait/waitadmin_fastapi
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
import oss2
from typing import Union, Dict
from fastapi import UploadFile
from oss2.exceptions import (
    SignatureDoesNotMatch,
    RequestError,
    ServerError,
    ClientError,
    OssError
)


class AliyunStorage:
    """ 阿里云OSS """

    def __init__(self, config: Dict[str, str]):
        self.bucket = config.get("bucket", "")
        self.domain = config.get("domain", "")
        self.endpoint = config.get("region", "")
        self.access_key = config.get("access_key", "")
        self.secret_key = config.get("secret_key", "")
        self.auth = oss2.Auth(self.access_key, self.secret_key)
        try:
            self.bucket = oss2.Bucket(auth=self.auth, endpoint=self.endpoint, bucket_name=self.bucket)
        except OssError as e:
            raise Exception(f"{e.status}: {e.body}")

    def upload(self, file_in: UploadFile, key: str) -> Union[str, None]:
        """
        文件数据上传到阿里云OSS。

        Args:
            file_in (UploadFile): 要上传的文件对象。
            key (str): 保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            self.bucket.put_object(key=key, data=file_in.file)
            return None
        except RequestError as e:
            return f"{e.status}: {e.body}"
        except (SignatureDoesNotMatch, ServerError, ClientError, OssError) as e:
            return f"{e.status}: {e.details.get('Message')}"
        except Exception as e:
            return str(e)

    def push(self, path: str, key: str) -> Union[str, None]:
        """
        从本地文件路径上传文件到阿里云OSS。

        Args:
            path (str): 本地文件路径, 如: /www/image/aa.png。
            key (str):  保存文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果上传成功返回None,否则返回错误信息。

        Author:
            zero
        """
        with open(path, "rb") as f:
            content = f.read()
            try:
                self.bucket.put_object(key, content)
                return None
            except RequestError as e:
                return f"{e.status}: {e.body}"
            except (SignatureDoesNotMatch, ServerError, ClientError, OssError) as e:
                return f"{e.status}: {e.details.get('Message')}"
            except Exception as e:
                return str(e)

    def fetch(self, url: str, key: str) -> Union[str, None]:
        """
        从指定URL抓取文件并存储到阿里云OSS。

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
            self.bucket.put_object(key, content.read())
        except RequestError as e:
            return f"{e.status}: {e.body}"
        except (SignatureDoesNotMatch, ServerError, ClientError, OssError) as e:
            return f"{e.status}: {e.details.get('Message')}"
        except Exception as e:
            return str(e)

    def delete(self, key: str) -> Union[str, None]:
        """
        从阿里云OSS中删除。

        Args:
            key (str): 文件名称, 如: storage/image/aa.png。

        Returns:
            Union[str, None]: 如果抓取并保存成功返回None,否则返回错误信息。

        Author:
            zero
        """
        try:
            self.bucket.delete_object(key)
            return None
        except RequestError as e:
            return f"{e.status}: {e.body}"
        except (SignatureDoesNotMatch, ServerError, ClientError, OssError) as e:
            return f"{e.status}: {e.details.get('Message')}"
        except Exception as e:
            return str(e)
