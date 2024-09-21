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
from common.utils.urls import UrlUtil
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import backs_schema as schema


class BacksService:
    """ 后台配置服务类 """

    @classmethod
    async def detail(cls) -> schema.BacksDetailVo:
        """
        后台配置详情。

        Returns:
            schema.BacksDetailVo: 后台配置详情Vo。

        Author:
            zero
        """
        backs_conf = await ConfigUtil.get("backs") or {}
        return schema.BacksDetailVo(
            name=backs_conf.get("name", ""),
            title=backs_conf.get("title", ""),
            favicon=await UrlUtil.to_absolute_url(backs_conf.get("favicon", "")),
            cover=await UrlUtil.to_absolute_url(backs_conf.get("cover", "")),
            logo_black_big=await UrlUtil.to_absolute_url(backs_conf.get("logo_black_big", "")),
            logo_black_small=await UrlUtil.to_absolute_url(backs_conf.get("logo_black_small", "")),
            logo_white_big=await UrlUtil.to_absolute_url(backs_conf.get("logo_white_big", "")),
            logo_white_small=await UrlUtil.to_absolute_url(backs_conf.get("logo_white_small", "")),
            contacts=backs_conf.get("contacts", ""),
            mobile=backs_conf.get("mobile", "")
        )

    @classmethod
    async def save(cls, post: schema.BacksDetailVo):
        """
        后台配置保存。

         Args:
            post (schema.BacksDetailVo): 后台配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("backs", "name", post.name)
        await ConfigUtil.set("backs", "title", post.title)
        await ConfigUtil.set("backs", "cover", UrlUtil.to_relative_url(post.cover))
        await ConfigUtil.set("backs", "favicon", UrlUtil.to_relative_url(post.favicon))
        await ConfigUtil.set("backs", "logo_black_big", UrlUtil.to_relative_url(post.logo_black_big))
        await ConfigUtil.set("backs", "logo_black_small", UrlUtil.to_relative_url(post.logo_black_small))
        await ConfigUtil.set("backs", "logo_white_big", UrlUtil.to_relative_url(post.logo_white_big))
        await ConfigUtil.set("backs", "logo_white_small", UrlUtil.to_relative_url(post.logo_white_small))

        await ConfigUtil.set("backs", "contacts", post.contacts)
        await ConfigUtil.set("backs", "mobile", post.mobile)
