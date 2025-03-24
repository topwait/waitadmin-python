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
from config import get_settings
from kernels.utils import RequestUtil
from common.utils.config import ConfigUtil


class UrlUtil:
    """ Url工具 """

    @classmethod
    async def get_storage_domain(cls) -> str:
        """
        获取当前存储域名

        Returns:
            str: domain
        """
        engine: str = await ConfigUtil.get("storage", "engine", "local")
        if engine == "local":
            return RequestUtil.domain
        else:
            _config: dict = await ConfigUtil.get("storage", engine, {})
            return _config.get("domain", "").strip()

    @classmethod
    async def get_storage_engine(cls) -> str:
        """
        获取当前存储引擎

        Returns:
            str: [local,qiniu,aliyun,qcloud]
        """
        return await ConfigUtil.get("storage", "engine", "local")

    @staticmethod
    async def to_absolute_url(url) -> str:
        """
        将相对URL转换为绝对URL。

        Args:
            url (str): 要转换的URL。

        Returns:
            str: 转换后的绝对URL。
        """
        if not url or url is None:
            return ""

        if url.startswith("http:") or url.startswith("https:"):
            return url

        engine: str = await ConfigUtil.get("storage", "engine", "local")
        if engine == "local":
            return RequestUtil.domain + "/" + url
        else:
            config: dict = await ConfigUtil.get("storage", engine, {})
            domain: str = config.get("domain", "")
            return domain + "/" + url

    @staticmethod
    def to_relative_url(url) -> str:
        """
        将绝对URL转换为相对URL。

        Args:
            url (str): 待转换的URL。

        Returns:
            str: 转换后的相对URL或原URL。
        """
        if url.startswith("http:"+"//") or url.startswith("https://"):
            url = url.replace("http:"+"//", "").replace("https://", "")
            arr = url.split("/")
            arr.pop(0)
            return str("/".join(arr))
        else:
            return url

    @staticmethod
    def to_root_path(path: str = "") -> str:
        """
        将相对PATH转换为绝对路径。

        Args:
            path (str): 待转换的URL。

        Returns:
            str: 转换后的绝对PATH。
        """
        if not path:
            return get_settings().APP_PATH

        if path.startswith("http:" + "//") or path.startswith("https://"):
            path = UrlUtil.to_relative_url(path)

        root_app = get_settings().APP_PATH
        entrance = get_settings().UPLOAD["root"]
        return f"{root_app}/{entrance}/" + path.strip("/")

    @staticmethod
    def to_runtime_path(path) -> str:
        """
        将相对PATH转换为绝对路径。

        Args:
            path (str): 待转换的URL。

        Returns:
            str: 转换后的绝对PATH。
        """
        if path.startswith("http:" + "//") or path.startswith("https://"):
            path = UrlUtil.to_relative_url(path)

        root_app = get_settings().APP_PATH
        return f"{root_app}/runtime/" + path.strip("/")
