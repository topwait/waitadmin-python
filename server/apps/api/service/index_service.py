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
from pydantic import TypeAdapter
from exception import AppException
from apps.api.schemas import index_schema as schema
from apps.api.service.article_service import ArticleService
from common.models.dev import DevBannerModel
from common.enums.public import BannerEnum
from common.utils.config import ConfigUtil
from common.utils.tools import ToolsUtil
from common.utils.urls import UrlUtil
from plugins.msg.driver import MsgDriver


class IndexService:
    """ 公共服务类 """

    @classmethod
    async def homing(cls) -> schema.HomingVo:
        """
        主页数据

        Returns:
            schema.HomingVo: 主页数据Vo

        Author:
            zero
        """
        _adv_lists = await (DevBannerModel
                            .filter(position=BannerEnum.SIDE)
                            .filter(is_disable=0, is_delete=0)
                            .order_by("-sort", "-id")
                            .all())

        _banner_lists = await (DevBannerModel
                               .filter(position=BannerEnum.HOME)
                               .filter(is_disable=0, is_delete=0)
                               .order_by("-sort", "-id")
                               .all())

        adv = []
        for _adv in _adv_lists:
            vo = TypeAdapter(schema.BannerListVo).validate_python(_adv.__dict__)
            vo.image = await UrlUtil.to_absolute_url(vo.image)
            adv.append(vo)

        banners = []
        for _banner in _banner_lists:
            vo = TypeAdapter(schema.BannerListVo).validate_python(_banner.__dict__)
            vo.image = await UrlUtil.to_absolute_url(vo.image)
            banners.append(vo)

        return schema.HomingVo(
            adv=adv,
            banner=banners,
            lately=await ArticleService.recommend("lately"),
            ranking=await ArticleService.recommend("ranking"),
            topping=await ArticleService.recommend("topping"),
            everyday=await ArticleService.recommend("everyday")
        )

    @classmethod
    async def config(cls) -> schema.ConfigVo:
        """
        全局配置

        Returns:
            schema.ConfigVo: 全局配置Vo

        Author:
            zero
        """
        pc = await ConfigUtil.get("pc") or {}
        login = await ConfigUtil.get("login") or {}
        website = await ConfigUtil.get("website") or {}
        recharge = await ConfigUtil.get("recharge") or {}

        return schema.ConfigVo(
            login={
                "is_agreement": int(login.get("is_agreement", 0)),
                "defaults": login.get("defaults", ""),
                "register": login.get("registers", []),
                "means": login.get("login_modes", []),
                "oauth": login.get("login_other", []),
            },
            website={
                "icp": website.get("icp", ""),
                "pcp": website.get("pcp", ""),
                "domain": website.get("domain", ""),
                "analyse": website.get("analyse", ""),
                "copyright": website.get("copyright", "")
            },
            pc={
                "favicon": await UrlUtil.to_absolute_url(pc.get("favicon", "")),
                "logo": await UrlUtil.to_absolute_url(pc.get("logo", "")),
                "name": pc.get("name", ""),
                "title": pc.get("title", ""),
                "keywords": pc.get("keywords", ""),
                "description": pc.get("description", "")
            },
            recharge={
                "status": int(recharge.get("status", 0)),
                "min_recharge": float(recharge.get("min_recharge", 0))
            }
        )

    @classmethod
    async def policy(cls, type_: str) -> schema.PolicyVo:
        """
        政策协议

        Returns:
            schema.PolicyVo: 政策协议Vo

        Author:
            zero
        """
        content = await ConfigUtil.get("policy", type_) or ""
        return schema.PolicyVo(
            content=content
        )

    @classmethod
    async def send_sms(cls, scene: int, mobile: str):
        """
        发送短信

        Args:
            scene (int): 发送场景码
            mobile (str): 接收手机号

        Author:
            zero
        """
        try:
            await MsgDriver.send(scene, {
                "mobile": mobile,
                "code": ToolsUtil.make_rand_digit(6)
            })
        except Exception as e:
            raise AppException(str(e))

    @classmethod
    async def send_email(cls, scene: int, email: str):
        """
        发送邮件

        Args:
            scene (int): 发送场景码
            email (str): 接收邮箱号

        Author:
            zero
        """
        try:
            await MsgDriver.send(scene, {
                "email": email,
                "code": ToolsUtil.make_rand_digit(6)
            })
        except Exception as e:
            raise AppException(str(e))
