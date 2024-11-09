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
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


class AliyunSms:
    def __init__(self, config: dict):
        self.status = 0
        self.sign = config.get("sign", "")
        self.APP_KEY = config.get("acc_key", "")
        self.SECRET = config.get("acc_secret", "")

    def send(self, mobile: str, template_id: str, template_params: dict):
        try:
            request = CommonRequest(domain="dysmsapi.aliyuncs.com", version="2017-05-25", action_name="SendSms")
            request.set_method("POST")
            request.set_protocol_type("https")
            request.add_query_param("PhoneNumbers", mobile)
            request.add_query_param("SignName", self.sign)
            request.add_query_param("TemplateCode", template_id)
            request.add_query_param("TemplateParam", template_params)
            client = AcsClient(ak=self.APP_KEY, secret=self.SECRET)
            response = client.do_action_with_exception(request)

            resp_data = json.loads(response)
            if resp_data.get("Code") != "OK" or resp_data.get("Message") != "OK":
                return resp_data.get("Message", response)

            return True
        except Exception as e:
            raise Exception(str(e))
