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
from kernels.utils import RequestUtil
from common.utils.urls import UrlUtil
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import channel_schema as schema


class ChannelService:
    """ 渠道配置服务类 """

    @classmethod
    async def detail(cls) -> schema.ChannelDetailVo:
        """
        渠道配置详情。

        Returns:
            schema.ChannelDetailVo: 配置详情Vo。

        Author:
            zero
        """
        wx = await ConfigUtil.get("wx_channel") or {}
        oa = await ConfigUtil.get("oa_channel") or {}
        op = await ConfigUtil.get("op_channel") or {}

        domain: str = RequestUtil.domain
        return schema.ChannelDetailVo(
            wx=schema.WxParams(
                name=wx.get("name", ""),
                original_id=wx.get("original_id", ""),
                qr_code=await UrlUtil.to_absolute_url(wx.get("qr_code", "")),
                app_id=wx.get("app_id", ""),
                app_secret=wx.get("app_secret", ""),
                request_domain=domain,
                socket_domain=domain,
                upload_file_domain=domain,
                download_file_domain=domain,
                udp_domain=domain,
            ),
            oa=schema.OaParams(
                name=oa.get("name", ""),
                original_id=oa.get("original_id", ""),
                qr_code=await UrlUtil.to_absolute_url(oa.get("qr_code", "")),
                app_id=oa.get("app_id", ""),
                app_secret=oa.get("app_secret", ""),
                url=domain,
                token=oa.get("token", ""),
                aes_key=oa.get("aes_key", ""),
                encryption_type=int(oa.get("encryption_type", 1)),
                wk_domain=domain,
                js_domain=domain,
                web_domain=domain,
            ),
            op=schema.OpParams(
                app_id=op.get("app_id", ""),
                app_secret=op.get("app_secret", ""),
            )
        )

    @classmethod
    async def save(cls, post: schema.ChannelDetailVo):
        """
        渠道配置保存。

         Args:
            post (schema.ChannelDetailVo): 配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("wx_channel", "name", post.wx.name)
        await ConfigUtil.set("wx_channel", "original_id", post.wx.original_id)
        await ConfigUtil.set("wx_channel", "qr_code", UrlUtil.to_relative_url(post.wx.qr_code))
        await ConfigUtil.set("wx_channel", "app_id", post.wx.app_id)
        await ConfigUtil.set("wx_channel", "app_secret", post.wx.app_secret)

        await ConfigUtil.set("oa_channel", "name", post.oa.name)
        await ConfigUtil.set("oa_channel", "original_id", post.oa.original_id)
        await ConfigUtil.set("oa_channel", "qr_code", UrlUtil.to_relative_url(post.oa.qr_code))
        await ConfigUtil.set("oa_channel", "app_id", post.oa.app_id)
        await ConfigUtil.set("oa_channel", "app_secret", post.oa.app_secret)
        await ConfigUtil.set("oa_channel", "token", post.oa.token)
        await ConfigUtil.set("oa_channel", "aes_key", post.oa.aes_key)
        await ConfigUtil.set("oa_channel", "encryption_type", post.oa.encryption_type)

        await ConfigUtil.set("op_channel", "app_id", post.op.app_id)
        await ConfigUtil.set("op_channel", "app_secret", post.op.app_secret)
