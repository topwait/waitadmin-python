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
import json
import asyncio
import aiofiles
import aiohttp


class CurlUtil:
    @classmethod
    async def curl(cls, method: str, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起CURL请求

        Args:
            method (str): 请求方式: [GET,POST,DELETE,PUT,PATCH]
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        method = method.upper()
        if method not in ["GET", "POST", "DELETE", "PUT", "PATCH"]:
            raise Exception(f"Unsupported request method `{method}`")

        async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=ssl),
                timeout=aiohttp.ClientTimeout(total=timeout),
                headers=headers
        ) as session:
            try:
                request_method = getattr(session, method.lower())
                async with request_method(url=url, json=data) as response:
                    results = await response.text()
                    if response.status == 404:
                        raise Exception("API 404 Not Found")
                    try:
                        return json.loads(results)
                    except json.JSONDecodeError:
                        return {"text": results, "status": response.status}
            except aiohttp.ClientError as err:
                raise Exception(f"Curl Request error: {err}")
            except asyncio.TimeoutError:
                raise Exception(f"Curl Request timeout")
            except aiohttp.client_exceptions.ClientResponseError as err:
                raise Exception(err.status, err.message)

    @classmethod
    async def curl_get(cls, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起GET请求

        Args:
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        return await cls.curl(method="GET", url=url, headers=headers, data=data, timeout=timeout, ssl=ssl)

    @classmethod
    async def curl_put(cls, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起PUT请求

        Args:
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        return await cls.curl(method="PUT", url=url, headers=headers, data=data, timeout=timeout, ssl=ssl)

    @classmethod
    async def curl_post(cls, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起POST请求

        Args:
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        return await cls.curl(method="POST", url=url, headers=headers, data=data, timeout=timeout, ssl=ssl)

    @classmethod
    async def curl_patch(cls, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起PATCH请求

        Args:
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        return await cls.curl(method="PATCH", url=url, headers=headers, data=data, timeout=timeout, ssl=ssl)

    @classmethod
    async def curl_delete(cls, url: str, headers: dict = None, data: dict = None, timeout=60, ssl=False):
        """
        发起DELETE请求

        Args:
            url (str): 网络文件地址
            headers (dict): 请求头参数
            data (dict): Body参数
            timeout (int): 超时时间(s)
            ssl (bool): ssl

        Author:
            zero
        """
        return await cls.curl(method="DELETE", url=url, headers=headers, data=data, timeout=timeout, ssl=ssl)

    @classmethod
    async def download_file(
            cls,
            url: str,
            save_path: str,
            timeout: int = 60,
            max_retries: int = 3,
            initial_backoff: float = 0.1):
        """
        下载网络文件

        Args:
            url (str): 网络文件地址
            save_path (str): 保存路径(如: /www/images/test.png)
            timeout (int): 超时时间
            max_retries (int): 最大重试次数
            initial_backoff (float): 初始重试间隔(秒), 会指数增长

        Author:
            zero
        """
        retries = 0
        last_exception = None

        while retries <= max_retries:
            try:
                timeout_obj = aiohttp.ClientTimeout(total=timeout)
                async with aiohttp.ClientSession(timeout=timeout_obj) as session:
                    async with session.get(url) as response:
                        if response.status == 200:
                            # 确保保存目录存在
                            os.makedirs(os.path.dirname(save_path), exist_ok=True)
                            # 写入模式保存文件
                            async with aiofiles.open(save_path, "wb") as f:
                                async for chunk in response.content.iter_chunked(4096):
                                    await f.write(chunk)
                            return save_path
                        else:
                            # 如果不是200状态码，视为可重试的错误（除非是404等）
                            if 400 <= response.status < 500 and response.status != 429:
                                # 4xx错误除了429（太多请求）外，通常不需要重试
                                raise Exception(f"HTTP error {response.status}")
                            raise Exception(f"HTTP error {response.status}")

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                retries += 1
                if retries <= max_retries:
                    # 指数退避：等待 1, 2, 4, 8... 秒
                    wait_time = initial_backoff * (2 ** (retries - 1))
                    await asyncio.sleep(wait_time)
                continue
            except Exception as e:
                last_exception = e
                break
        raise Exception(f"download file after {max_retries} retries: {str(last_exception)}")
