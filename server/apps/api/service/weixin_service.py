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
import time
from typing import Dict, List
from apps.api.cache.wechat_cache import WechatCache
from apps.api.widgets.user_widget import UserWidget
from kernels.utils import RequestUtil
from common.enums.client import ClientEnum
from plugins.wechat.service import WechatService


class WeixinService:
    """ 微信服务类 """

    @classmethod
    async def reply(cls, messages: Dict[str, str]):
        """
        微信公众号回调应答处理

        Args:
            messages (Dict[str, str]): 微信数据

        Returns:
            Response

        Author:
            zero
        """
        Event: str = messages.get("Event")
        ToUserName: str = messages.get("ToUserName")      # account
        FromUserName: str = messages.get("FromUserName")  # openid

        if Event == "SCAN":
            EventKey: List[str] = messages.get("EventKey").split(":")
            scene: str = EventKey[0] if len(EventKey) >= 2 else ""
            state: str = EventKey[1] if len(EventKey) >= 2 else EventKey[0]

            results = ""
            if scene == "login":
                results = await cls._scan_login_event(state, FromUserName)
            elif scene == "bind":
                results = await cls._scan_bind_event(state)

            return WechatService.oa_reply_message(
                msg_type="text",
                to_user_name=ToUserName,
                from_user_name=FromUserName,
                message={"content": results}
            )
        elif Event == "subscribe":
            pass

    @classmethod
    async def _scan_login_event(cls, state: str, openid: str) -> str:
        """
        微信扫码登录回调处理

        Args:
            state (str): 缓存键
            openid (str): openid

        Returns:
            str: string

        Author:
            zero
        """
        result = await WechatCache.login_scan_get(state)
        if result is None or int(result["status"]) > 0:
            return "二维码已失效,请重新扫码"

        try:
            user = await UserWidget.openid_user(openid)
            if not user:
                await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_ING)
                url = await WechatService.oa_build_auth_url(
                    redirect_uri=f"{RequestUtil.domain}/user/authen?scene=login",
                    state=state
                )
                return f"<a href='{url}'>点击确认登录</a>"
            else:
                if user.is_disable:
                    await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_FAIL)
                    return "账号已被禁止登录,请联系客服处理"
                else:
                    user.last_login_ip = RequestUtil.host
                    user.last_login_time = int(time.time())
                    await user.save()
                    token: str = await UserWidget.gran_token(user.id, ClientEnum.PC)
                    await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_OK, token)
                    return "登录成功"
        except Exception as e:
            return str(e)

    @classmethod
    async def _scan_bind_event(cls, state: str) -> str:
        """
        微信扫码绑定回调处理

        Args:
            state (str): 缓存键

        Returns:
            str: string

        Author:
            zero
        """
        result = await WechatCache.login_scan_get(state)
        if result is None or int(result["status"]) > 0:
            return "二维码已失效,请重新扫码"

        try:
            await WechatCache.login_scan_set(state, WechatCache.SCAN_STATUS_ING)
            url = await WechatService.oa_build_auth_url(
                redirect_uri=f"{RequestUtil.domain}/user/authen?scene=bind",
                state=state
            )
            return f"<a href='{url}'>点击确认绑定</a>"
        except Exception as e:
            return str(e)
