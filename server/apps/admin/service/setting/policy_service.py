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
from apps.admin.schemas.setting import policy_schema as schema


class PolicyService:
    """ 协议配置服务类 """

    @classmethod
    async def detail(cls) -> schema.PolicyDetailVo:
        """
        协议配置详情。

        Returns:
            schema.PolicyDetailVo: 协议配置详情Vo。

        Author:
            zero
        """
        conf = await ConfigUtil.get("policy") or {}
        return schema.PolicyDetailVo(
            service=conf.get("service", ""),
            privacy=conf.get("privacy", ""),
            payment=conf.get("payment", "")
        )

    @classmethod
    async def save(cls, post: schema.PolicyDetailVo):
        """
        协议配置保存。

         Args:
            post (schema.PolicyDetailVo): 协议配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("policy", "service", post.service)
        await ConfigUtil.set("policy", "privacy", post.privacy)
        await ConfigUtil.set("policy", "payment", post.payment)
