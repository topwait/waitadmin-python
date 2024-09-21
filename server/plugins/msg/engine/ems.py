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
from common.enums.notice import NoticeEnum
from common.models.notice import NoticeRecord
from plugins.mail.driver import MailDriver


class EmsNotice:

    async def send(self, scene: int, params: dict, template: dict):
        """
        发送邮件通知。

        Args:
            scene (int): 发送场景参数。
            params (int): 发送的参数。
            template (int): 邮件模型参数。

        Raises:
            AppException: 发送失败时抛出错误。

        Author:
            zero
        """
        # 建发送记录
        record = await NoticeRecord.create(
            scene=scene,
            user_id=params.get("user_id", 0),
            account=params.get("email"),
            title=template.get("name"),
            code=self._get_code(params, template),
            content=self._get_content(params, template),
            receiver=template.get("get_client"),
            sender=NoticeEnum.SENDER_SMS,
            status=NoticeEnum.STATUS_WAIT,
            is_read=NoticeEnum.VIEW_UNREAD,
            is_captcha=template.get("is_captcha"),
            expire_time=int(params.get("expire_time", 0)) + int(time.time()) + 900,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        # 发送短信通知
        try:
            await (MailDriver()
                   .to(params.get("email"))
                   .subject(template.get("ems_template").get("template_code"))
                   .body(self._get_content(params, template))
                   .send())

            await NoticeRecord.filter(id=record.id).update(
                status=NoticeEnum.STATUS_OK,
                update_time=int(time.time())
            )
        except Exception as e:
            await NoticeRecord.filter(id=record.id).update(
                status=NoticeEnum.STATUS_FAIL,
                error=str(e),
                update_time=int(time.time())
            )
            raise Exception(str(e))

    @staticmethod
    def _get_content(params: dict, template: dict) -> str:
        """
        获取邮件内容(替换模板变量)。

        Args:
            params (int): 发送的参数。
            template (int): 邮件模型参数。

        Returns:
             str: 处理后的邮件模型。

        Author:
            zero
        """
        content = template.get("ems_template", {}).get("content", "")
        for item, val in params.items():
            search_replace = "${" + item + "}"
            content = content.replace(search_replace, str(val))

        return content

    @staticmethod
    def _get_code(params: dict, template: dict) -> str:
        """
        获取邮件验证码(某些场景不需要)。

        Args:
            params (int): 发送的参数。
            template (int): 邮件模型参数。

        Returns:
             str: 邮件验证码值。

        Author:
            zero
        """
        code = ""
        if template.get("is_captcha", False):
            code_dict = {k: v for k, v in params.items() if k in template.get("variable", {})}
            if code_dict and code_dict is not None:
                code = list(code_dict.values())[0]

        return str(code)
