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
import time
from exception import AppException
from common.models.notice import NoticeSetting
from common.models.notice import NoticeRecord
from common.enums.notice import NoticeEnum
from plugins.msg.engine.ems import EmsNotice
from plugins.msg.engine.sms import SmsNotice


class MsgDriver:

    @classmethod
    async def send(cls, scene: int, params: dict = None):
        """
        根据场景发送通知。

        Args:
            scene (int): 通知场景编号。
            params (dict, optional): 发送通知时所需的参数。

        Raises:
            AppException: 如果指定的通知场景不存在则抛出异常。

        Author:
            zero
        """
        notice = await NoticeSetting.filter(is_delete=0, scene=scene).first()

        if notice:
            template = notice.__dict__
            template["variable"] = json.loads(notice.variable)
            template["ems_template"] = json.loads(notice.ems_template)
            template["sms_template"] = json.loads(notice.sms_template)

            if template["ems_template"].get("status", 0):
                return await EmsNotice().send(scene, params, template)

            if template["sms_template"].get("status", 0):
                return await SmsNotice().send(scene, params, template)
        else:
            raise AppException("通知场景不存在")

    @classmethod
    async def check_code(cls, scene: int, code: str, auto_verify: bool = False) -> bool:
        """
        检查验证码是否有效。

        Args:
            scene (int): 验证场景编号。
            code (str): 需要验证的验证码字符串。
            auto_verify (bool, optional): 是否在验证成功后自动标记为已读。默认为False。

        Returns:
            bool: 如果验证码有效且未过期, 则返回True; 否则返回False。

        Author:
            zero
        """
        record = await NoticeRecord.filter(
            code=code,
            scene=scene,
            status=NoticeEnum.STATUS_OK,
            is_read=NoticeEnum.VIEW_UNREAD,
            is_captcha=1,
            is_delete=0
        ).first()

        check_record = record
        if not check_record:
            return False

        result = True
        if record.expire_time and record.expire_time <= int(time.time()):
            result = False

        if result and auto_verify:
            await NoticeRecord.filter(id=record.id)\
                .update(
                    is_read=NoticeEnum.VIEW_READ,
                    update_time=int(int(time.time()))
                )

        return result

    @classmethod
    async def verify_code(cls, scene: int, code: str) -> int:
        """
        核销验证码。

        Args:
            scene (int): 验证场景编号。
            code (str): 需要标记为已读的验证码字符串。

        Returns:
            int: 被更新的记录数。

        Author:
            zero
        """
        return await NoticeRecord.filter(
            code=code,
            scene=scene,
        ).update(is_read=NoticeEnum.VIEW_READ, update_time=int(int(time.time())))
