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
import aiosmtplib
from aiosmtplib import SMTP
from typing import Union, List
from email.message import EmailMessage
from common.utils.config import ConfigUtil


class MailDriver:

    def __init__(self, host: str = "", port: int = 25, username: str = "", password: str = "", ssl: bool = False):
        self.port: int = port
        self.host: str = host
        self.username: str = username
        self.password: str = password
        self.verify_type: str = "ssl" if ssl else "default"
        self.messages = EmailMessage()

    async def init_config(self):
        """
        初始化邮件配置
        """
        if not self.host:
            config = await ConfigUtil.get("email") or {}
            self.port = int(config.get("smtp_port", 25))
            self.host = str(config.get("smtp_host", ""))
            self.username = config.get("smtp_user", "")
            self.password = config.get("smtp_pass", "")
            self.verify_type = config.get("verify_type", "default")

    async def smtp(self):
        """
        获取邮件服务连接

        Warning:
            连接使用完后记得把连接关闭
            关闭方式: smtp_client.quit()

        Author:
            zero
        """
        await self.init_config()
        smtp_client = SMTP(
            hostname=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            use_tls=True if self.verify_type == "ssl" else False
        )
        await smtp_client.connect()
        return smtp_client

    async def send(self):
        """
        发送邮件消息

        Raises:
            RuntimeError

        Author:
            zero
        """
        await self.init_config()

        if not self.messages["From"]:
            self.messages["From"] = self.username

        result = await aiosmtplib.send(
            self.messages,
            hostname=self.host,
            port=25,
            username=self.username,
            password=self.password,
            use_tls=True if self.verify_type == "ssl" else False
        )

        if not result[1].startswith("Mail OK"):
            raise Exception(result[1])

    def subject(self, title: str):
        """
        设置邮件标题

        Args:
            title (str): 邮件的标题。

        Author:
            zero
        """
        self.messages["subject"] = title
        return self

    def body(self, body: str):
        """
        设置邮件内容

        Args:
            body (str): 邮件文本内容。

        Author:
            zero
        """
        self.messages.set_content(body)
        return self

    def add_alternative(self, body: str, subtype: str = "html"):
        """
        设置HTML内容

        Args:
            body (str): HTML文本内容。
            subtype (str): 文本类型。

        Author:
            zero
        """
        self.messages.add_alternative(body, subtype=subtype)
        return self

    def add_attachment(self, path: str, filename: str, maintype: str, subtype: str):
        """
        设置邮件附件

        Args:
            path (str): 文件的本地路径: 如: /www/aa.png。
            filename (str): 文件的名称: 如: wa.png。
            maintype (str): 文件的类型, 如: image。
            subtype (str): 文件子类型, 如: png。

        Author:
            zero
        """
        with open(path, "rb") as f:
            data = f.read()
        self.messages.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
        return self

    def fromm(self, address: str):
        """
        设置发件人 (发出的邮箱号)

        Args:
            address (Union[str, List[str]]): 发送者的邮箱。

        Example:
            address = "wa@qq.com"

        Author:
            zero
        """
        self.messages["From"] = address
        return self

    def to(self, address: Union[str, List[str]]):
        """
        设置收件人 (发送给谁?)

        Args:
            address (Union[str, List[str]]): 接收者的邮箱。

        Example:
            address = "wa@qq.com"
            address = ["wa.qq.com", "wa.163.com"]

        Author:
            zero
        """
        self.messages["To"] = address
        return self

    def cc(self, address: Union[str, List[str]]):
        """
        设置抄送人 (抄送给谁?)

        Args:
            address (Union[str, List[str]]): 接收者的邮箱。

        Example:
            address = "wa@qq.com"
            address = ["wa.qq.com", "wa.163.com"]

        Author:
            zero
        """
        self.messages["Cc"] = address
        return self
