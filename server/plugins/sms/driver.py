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
from plugins.sms.engine.aliyun import AliyunSms
from plugins.sms.engine.tencent import TencentSms


class SmsDriver(object):

    @classmethod
    async def send_sms(cls, mobile: str, template_id: str, template_params=None):
        engine: str = await ConfigUtil.get("sms", "engine", "")
        params: dict = await ConfigUtil.get("sms", engine, {})

        if not engine:
            raise Exception("尚未开启短信发送功能")
        if not params:
            raise Exception("找不到短信相关的配置")

        if engine == "aliyun":
            return AliyunSms(params).send(
                mobile=mobile,
                template_id=template_id,
                template_params=template_params
            )
        elif engine == "tencent":
            return TencentSms(params).send(
                mobile=mobile,
                template_id=template_id,
                template_params=template_params
            )
        else:
            raise Exception("找不到短信渠道引擎")
