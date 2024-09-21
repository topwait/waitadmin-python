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
from apps.admin.schemas.setting import basics_schema as schema


class BasicsService:
    """ 网站配置服务类 """

    @classmethod
    async def detail(cls) -> schema.BasicsDetailVo:
        """
        网站配置详情。

        Returns:
            schema.BasicsDetailVo: 网站配置详情Vo。

        Author:
            zero
        """
        website_conf = await ConfigUtil.get("website") or {}
        h5_conf = await ConfigUtil.get("h5") or {}
        pc_conf = await ConfigUtil.get("pc") or {}

        return schema.BasicsDetailVo(
            website=schema.WebsiteParams(
                icp=website_conf.get("icp", ""),
                pcp=website_conf.get("pcp", ""),
                copyright=website_conf.get("copyright", ""),
                analyse=website_conf.get("analyse", ""),
            ),
            h5=schema.H5Params(
                logo=await UrlUtil.to_absolute_url(h5_conf.get("logo", "")),
                title=h5_conf.get("title", ""),
                status=int(h5_conf.get("status", 1)),
                close_url=h5_conf.get("close_url", ""),
            ),
            pc=schema.PcParams(
                favicon=await UrlUtil.to_absolute_url(pc_conf.get("favicon", "")),
                logo=await UrlUtil.to_absolute_url(pc_conf.get("logo", "")),
                name=pc_conf.get("name", ""),
                title=pc_conf.get("title", ""),
                keywords=pc_conf.get("keywords", ""),
                description=pc_conf.get("description", "")
            )
        )

    @classmethod
    async def save(cls, post: schema.BasicsDetailVo):
        """
        网站配置保存。

         Args:
            post (schema.BasicsDetailVo): 网站配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("website", "icp", post.website.icp)
        await ConfigUtil.set("website", "pcp", post.website.pcp)
        await ConfigUtil.set("website", "copyright", post.website.copyright)
        await ConfigUtil.set("website", "analyse", post.website.analyse)

        await ConfigUtil.set("h5", "logo", UrlUtil.to_relative_url(post.h5.logo))
        await ConfigUtil.set("h5", "title", post.h5.title)
        await ConfigUtil.set("h5", "status", post.h5.status)
        await ConfigUtil.set("h5", "close_url", post.h5.close_url)

        await ConfigUtil.set("pc", "favicon", UrlUtil.to_relative_url(post.pc.favicon))
        await ConfigUtil.set("pc", "logo", UrlUtil.to_relative_url(post.pc.logo))
        await ConfigUtil.set("pc", "name", post.pc.name)
        await ConfigUtil.set("pc", "title", post.pc.title)
        await ConfigUtil.set("pc", "keywords", post.pc.keywords)
        await ConfigUtil.set("pc", "description", post.pc.description)
