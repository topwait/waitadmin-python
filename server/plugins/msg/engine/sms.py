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
from typing import Union
from common.utils.config import ConfigUtil
from common.enums.notice import NoticeEnum
from common.models.notice import NoticeRecord
from plugins.sms.driver import SmsDriver


class SmsNotice:

    async def send(self, scene: int, params: dict, template: dict):
        """
        发送短信通知。

        Args:
            scene (int): 发送场景参数。
            params (int): 发送的参数。
            template (int): 短信模型参数。

        Raises:
            AppException: 发送失败时抛出错误。

        Author:
            zero
        """
        # 建发送记录
        record = await NoticeRecord.create(
            scene=scene,
            user_id=params.get("user_id", 0),
            account=params.get("mobile"),
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
        result = await SmsDriver().send_sms(
            mobile=params.get("mobile"),
            template_id=template.get("sms_template").get("template_code"),
            template_params=await self._get_sms_params(params, template)
        )
        # 是否发送成功
        if isinstance(result, bool):
            await NoticeRecord.filter(id=record.id).update(
                status=NoticeEnum.STATUS_OK,
                update_time=int(time.time())
            )
        else:
            await NoticeRecord.filter(id=record.id).update(
                status=NoticeEnum.STATUS_FAIL,
                error=result,
                update_time=int(time.time())
            )
            raise Exception(result)

    @staticmethod
    def _get_content(params: dict, template: dict) -> str:
        """
        获取短信内容(替换模板变量)。

        Args:
            params (int): 发送的参数。
            template (int): 短信模型参数。

        Returns:
             str: 处理后的短信模型。

        Author:
            zero
        """
        content = template.get("sms_template", {}).get("content", "")
        for item, val in params.items():
            search_replace = "${" + item + "}"
            content = content.replace(search_replace, str(val))

        return content

    @staticmethod
    def _get_code(params: dict, template: dict) -> str:
        """
        获取短信验证码(某些场景不需要)。

        Args:
            params (int): 发送的参数。
            template (int): 短信模型参数。

        Returns:
             str: 短信验证码值。

        Author:
            zero
        """
        code = ""
        if template.get("is_captcha", False):
            code_dict = {k: v for k, v in params.items() if k in template.get("variable", {})}
            if code_dict:
                code = list(code_dict.values())[0]

        return str(code)

    @staticmethod
    async def _get_sms_params(params: dict, template: dict) -> Union[dict, list]:
        """
        获取短信参数(对腾讯短信作特殊处理)。

        Args:
            params (int): 发送的参数。
            template (int): 短信模型参数。

        Returns:
             str: 处理后的短信参数。

        Author:
            zero
        """
        # 获取当前短信引擎
        engine = await ConfigUtil.get("sms", "engine", "aliyun")
        if engine != "tencent":
            return params

        # 获取变量名数组
        arr = []
        content = template.get("sms_template", {}).get("content", "")
        for item, val in params.items():
            search = "{" + item + "}"
            if search in content and item not in arr:
                arr.append(item)

        # 获取变量名数组
        positions = {item: content.find("{" + item + "}") for item in arr if "{" + item + "}" in content}
        arr2 = sorted(positions.items(), key=lambda x: x[1])

        # 提取排序后的变量名
        arr3 = [item for item, _ in arr2]

        # 获取变量数组的对应值
        arr4 = [params[v] for v in arr3 if v in params]

        # 返回已处理的变量结果
        return arr4
