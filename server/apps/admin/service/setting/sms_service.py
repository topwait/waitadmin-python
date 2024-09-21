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
from typing import List
from common.utils.urls import UrlUtil
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import sms_schema as schema


class SmsService:
    """ 短信配置服务类 """

    @classmethod
    async def lists(cls) -> List[schema.SmsListVo]:
        """
        短信配置列表。

        Returns:
            List[schema.SmsListVo]: 短信配置列表。

        Author:
           zero
        """
        engine = await ConfigUtil.get("sms", "engine", "aliyun")

        aliyun = schema.SmsListVo(
            alias="aliyun",
            name="阿里云短信",
            desc="阿里云短信服务（Short Message Service）",
            image=await UrlUtil.to_absolute_url("static/images/service_aliyun.png"),
            status=1 if engine == "aliyun" else 0
        )

        tencent = schema.SmsListVo(
            alias="tencent",
            name="腾讯云短信",
            desc="腾讯云短信服务（Short Message Service）",
            image=await UrlUtil.to_absolute_url("static/images/service_tencent.png"),
            status=1 if engine == "tencent" else 0
        )

        return [aliyun, tencent]

    @classmethod
    async def detail(cls, alias: str) -> schema.SmsDetailVo:
        """
        短信配置详情。

        Returns:
            schema.SmsDetailVo: 短信配置详情Vo。

        Author:
           zero
        """
        engine = await ConfigUtil.get("sms", "engine", "aliyun")
        if alias == "aliyun":
            config = await ConfigUtil.get("sms", "aliyun", {})
            return schema.SmsDetailVo(
                alias="aliyun",
                name="阿里云短信",
                status=1 if engine == "aliyun" else 0,
                params=schema.SmsParams(
                    sign=config.get("sign", ""),
                    app_id=config.get("app_id", ""),
                    acc_key=config.get("acc_key", ""),
                    acc_secret=config.get("acc_secret", ""),
                )
            )
        else:
            config = await ConfigUtil.get("sms", "tencent", {})
            return schema.SmsDetailVo(
                alias="tencent",
                name="腾讯云短信",
                status=1 if engine == "tencent" else 0,
                params=schema.SmsParams(
                    sign=config.get("sign", ""),
                    app_id=config.get("app_id", ""),
                    acc_key=config.get("acc_key", ""),
                    acc_secret=config.get("acc_secret", ""),
                )
            )

    @classmethod
    async def save(cls, post: schema.SmsDetailVo):
        """
        短信配置保存。

         Args:
            post (schema.SmsDetailVo): 短信配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("sms", post.alias, post.params.__dict__)

        engine = await ConfigUtil.get("sms", "engine", "aliyun")
        if engine == post.alias and post.status == 0:
            await ConfigUtil.set("sms", "engine", "")
        else:
            await ConfigUtil.set("sms", "engine", post.alias)
