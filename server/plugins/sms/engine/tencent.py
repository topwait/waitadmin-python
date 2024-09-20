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
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.sms.v20210111 import sms_client, models


class TencentSms:
    def __init__(self, config: dict):
        self.config = {
            "": config.get(""),
        }
        pass

    @staticmethod
    def get_client(config):
        secret_id = config.get("secretId")
        secret_key = config.get("secretKey")
        cred = credential.Credential(secret_id, secret_key)

        # 实例化一个http选项,可选的,没有特殊需求可以跳过。
        http_profile = HttpProfile()
        http_profile.reqMethod = "POST"                    # post请求(默认为post请求)
        http_profile.reqTimeout = 60                       # 请求超时时间，单位为秒(默认60秒)
        http_profile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)

        # 实例化一个客户端配置对象,可以指定超时时间等配置
        client_profile = ClientProfile()
        client_profile.signMethod = "HmacSHA256"
        client_profile.httpProfile = http_profile

        return sms_client.SmsClient(cred, "ap-beijing", client_profile)

    def send(self, mobile: str, template_id: str, template_params: dict):
        _sms_client = self.get_client(self.config)
        req = models.SendSmsRequest()
        req.SmsSdkAppId = self.config.get("appId")
        req.SignName = self.config.get("sign")
        req.TemplateId = template_id
        req.PhoneNumberSet = ["+86{}".format(mobile.strip())]
        req.TemplateParamSet = template_params

        response = _sms_client.SendSms(req)
        try:
            resp_data = response.SendStatusSet[0]
            if resp_data.Code.upper() != "OK":
                return resp_data.Message
            return True
        except Exception as e:
            raise Exception(str(e))
