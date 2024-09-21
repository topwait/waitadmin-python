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
from common.utils.config import ConfigUtil
from kernels.utils import RequestUtil


class UrlUtil:
    """ Url工具 """

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
