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
from exception import AppException
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import email_schema as schema


class EmailService:
    """ 邮箱配置服务类 """

    @classmethod
    async def detail(cls) -> schema.EmailDetailVo:
        """
        登录配置详情。

        Returns:
            schema.EmailDetailVo: 邮箱配置详情Vo。

        Author:
            zero
        """
        conf = await ConfigUtil.get("email") or {}
        return schema.EmailDetailVo(
            smtp_type=conf.get("smtp_type", "") or "smtp",
            smtp_host=conf.get("smtp_host", ""),
            smtp_port=conf.get("smtp_port", ""),
            smtp_user=conf.get("smtp_user", ""),
            smtp_pass=conf.get("smtp_pass", ""),
            verify_type=conf.get("verify_type", "") or "default"
        )

    @classmethod
    async def save(cls, post: schema.EmailDetailVo):
        """
        邮箱配置保存。

         Args:
            post (schema.EmailDetailVo): 邮箱配置参数。

        Author:
            zero
        """
        if post.verify_type not in ["default", "ssl"]:
            post.verify_type = "default"

        await ConfigUtil.set("email", "smtp_type", "smtp")
        await ConfigUtil.set("email", "smtp_host", post.smtp_host)
        await ConfigUtil.set("email", "smtp_port", post.smtp_port)
        await ConfigUtil.set("email", "smtp_user", post.smtp_user)
        await ConfigUtil.set("email", "smtp_pass", post.smtp_pass)
        await ConfigUtil.set("email", "verify_type", post.verify_type)
