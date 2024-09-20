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
from typing import Dict
from weixin import WXAPPAPI
from weixin.client import WeixinMpAPI, bind_method
from weixin.oauth2 import OAuth2AuthExchangeError
from .configs import WeChatConfig


class WechatService:
    """ 微信功能服务类 """
    oa_access_token: Dict[str, str] = {}
    mnp_access_token: Dict[str, str] = {}

    @classmethod
    async def oa_auth2_session(cls, code: str, scope: str = "snsapi_userinfo"):
        """
        公众号登录凭证

        Document:
            https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html

        Args:
            code (str): 小程序生成的code
            scope (str): 授权场景: [snsapi_base=只能取openId, snsapi_userinfo=用户信息, snsapi_login=开放平台]

        Returns:
            Dict[str, str]: ["session_key", "openid", "unionid]

        Author:
            zero
        """
        if scope == "snsapi_login":
            config: Dict[str, str] = await WeChatConfig.get_op_config()
        else:
            config: Dict[str, str] = await WeChatConfig.get_oa_config()

        # 通过code换取网页授权access_token (/sns/oauth2/access_token)
        api = WeixinMpAPI(appid=config.get("app_id"), app_secret=config.get("app_secret"))
        access = api.exchange_code_for_access_token(code=code)

        # 拉取用户信息(需scope为snsapi_userinfo)
        oauth = WeixinMpAPI(access_token=access.get("access_token"))
        user = oauth.user(openid=access.get("openid"), scope=[scope])
        return {
            "openid": user.get("openid", ""),
            "unionid": user.get("unionid", ""),
            "nickname": user.get("nickname", ""),
            "avatarUrl": user.get("headimgurl", ""),
            "gender": int(user.get("sex", 0))
        }

    @classmethod
    async def oa_build_auth_url(cls, redirect_uri: str, state: str, scope: str = "snsapi_userinfo") -> str:
        """
        公众号链接生成

        Document:
            https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/Wechat_webpage_authorization.html

        Args:
            redirect_uri (str): 重定向地址(需要在公众号配置的)
            state (str): 状态码,用于标记是否超时
            scope (str): 授权场景: [snsapi_base=只能取openId, snsapi_userinfo=用户信息, snsapi_login=开放平台]

        Returns:
            str: url

        Author:
            zero
        """
        if scope == "snsapi_login":
            config: Dict[str, str] = await WeChatConfig.get_op_config()
        else:
            config: Dict[str, str] = await WeChatConfig.get_oa_config()

        api = WeixinMpAPI(
            appid=config.get("app_id"),
            app_secret=config.get("app_secret"),
            redirect_uri=redirect_uri
        )

        return api.get_authorize_login_url(scope=[scope], state=state)

    @classmethod
    def oa_reply_message(cls, msg_type: str, to_user_name: str, from_user_name: str, message: Dict[str, str]) -> str:
        """
        公众号回复消息模板格式

        Document:
            https://developers.weixin.qq.com/doc/offiaccount/Message_Management/Passive_user_reply_message.html#1

        Args:
            msg_type (str): 消息类型
            to_user_name (str): 发送用户
            from_user_name (str): 来源用户
            message (Dict[str, str]): 看文档要发送消息的字段

        Returns:
            str: xml

        Author:
            zero
        """
        create_time = str(int(time.time()))
        if msg_type == "text":  # 回复文本消息
            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[{message["content"]}]]></Content>
            </xml>"""
        elif msg_type == "image":  # 回复图片消息
            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[image]]></MsgType>
                <Image>
                    <MediaId><![CDATA[{message["media_id"]}]]></MediaId>
                </Image>
            </xml>"""
        elif msg_type == "voice":  # 回复语音消息
            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[voice]]></MsgType>
                <Voice>
                    <MediaId><![CDATA[{message["media_id"]}]]></MediaId>
                </Voice>
            </xml>"""
        elif msg_type == "video":  # 回复视频消息
            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[video]]></MsgType>
                <Video>
                    <MediaId><![CDATA[{message["media_id"]}]]></MediaId>
                    <Title><![CDATA[{message["title"]}]]></Title>
                    <Description><![CDATA[{message["description"]}]]></Description>
                </Video>
            </xml>"""
        elif msg_type == "music":  # 回复音乐消息
            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <Music>
                    <Title><![CDATA[{message["title"]}]]></Title>
                    <Description><![CDATA[{message["description"]}]]></Description>
                    <MusicUrl><![CDATA[{message["music_url"]}]]></MusicUrl>
                    <HQMusicUrl><![CDATA[{message.get("hq_music_url", "")}]]></HQMusicUrl>
                    <ThumbMediaId><![CDATA[{message["media_id"]}]]></ThumbMediaId>
                </Music>
            </xml>"""
        elif msg_type == "news":  # 回复图文消息
            articles = ""
            for item in message.get("articles") or []:
                articles += f"""<item>
                        <Title><![CDATA[{item.get("title")}]]></Title>
                        <Description><![CDATA[{item.get("description")}]]></Description>
                        <PicUrl><![CDATA[{item.get("pic_url")}]]></PicUrl>
                        <Url><![CDATA[{item.get("url")}]]></Url>
                    </item>"""

            return f"""<xml>
                <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
                <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
                <CreateTime>{create_time}</CreateTime>
                <MsgType><![CDATA[music]]></MsgType>
                <ArticleCount>{message["article_count"]}</ArticleCount>
                <Articles>
                    [article_item]
                </Articles>
            </xml>""".replace("[article_item]", articles)

    @classmethod
    async def oa_build_qr_code(cls, code: str, event: str):
        """
        公众号二维码生成

        Document:
            https://developers.weixin.qq.com/doc/offiaccount/Account_Management/Generating_a_Parametric_QR_Code.html

        Args:
            code (str): 唯一编码
            event (str): 事件: [login=登录,bind=绑定微信]

        Returns:
            Dict[str, str]: ["url", "key", "ticket", "expire_seconds"]

        Author:
            zero
        """
        try:
            config: Dict[str, str] = await WeChatConfig.get_oa_config()
            access: Dict[str, str] = await cls.get_oa_access_token()

            api = WeixinMpAPI(
                appid=config.get("app_id"),
                app_secret=config.get("app_secret"),
                access_token=access.get("access_token")
            )

            ticket_code: str = code
            response = api.qrcode(json_body={
                "expire_seconds": 120,
                "action_name": "QR_STR_SCENE",
                "action_info": {
                    "scene": {"scene_str": event + ":" + ticket_code}
                }
            })

            if not response.get("ticket"):
                raise Exception(str(response.get("errcode")) + ": " + response.get("errmsg"))

            return {
                "url": "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=" + response.get("ticket"),
                "key": ticket_code,
                "ticket": response.get("ticket"),
                "expire_seconds": response.get("expire_seconds"),
            }
        except OAuth2AuthExchangeError as e:
            raise Exception(str(e.code) + ": " + e.description)

    @classmethod
    async def wx_code2_session(cls, code: str) -> Dict[str, str]:
        """
        小程序登录凭证

        Document:
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html

        Args:
            code (str): 小程序生成的code

        Returns:
            Dict[str, str]: ["session_key", "openid", "unionid"]

        Author:
            zero
        """
        try:
            config: Dict[str, str] = await WeChatConfig.get_wx_config()

            api = WXAPPAPI(appid=config.get("app_id"), app_secret=config.get("app_secret"))
            response = api.exchange_code_for_session_key(code=code)
            if response.get("errcode") != 0 or not response.get("phone_info"):
                raise Exception(str(response.get("errcode")) + ": " + response.get("errmsg"))

            return {
                "session_key": response.get("session_key", ""),
                "openid": response.get("openid", ""),
                "unionid": response.get("unionid", ""),
            }
        except OAuth2AuthExchangeError as e:
            raise Exception(str(e.code) + ": " + e.description)

    @classmethod
    async def wx_phone_number(cls, code: str) -> Dict[str, str]:
        """
        小程序手机号码

        Document:
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html

        Args:
            code (str): 小程序生成的code

        Returns:
            Dict[str, str]: ["countryCode", "phoneNumber", "purePhoneNumber"]

        Author:
            zero
        """
        config: Dict[str, str] = await WeChatConfig.get_wx_config()
        access: Dict[str, str] = await cls.get_mnp_access_token()

        setattr(WXAPPAPI, "phone", bind_method(
            path="/wxa/business/getuserphonenumber",
            method="POST",
            accepts_parameters=["json_body"],
            response_type="entry",
        ))

        api = WXAPPAPI(
            appid=config.get("app_id"),
            app_secret=config.get("app_secret"),
            access_token=access.get("access_token")
        )

        api.phone = api.phone
        response = api.phone(json_body={"code": code})
        if response.get("errcode") != 0 or not response.get("phone_info"):
            raise Exception(str(response.get("errcode")) + ": " + response.get("errmsg"))

        return {
            # 区号(+86)
            "countryCode": response.get("phone_info").get("countryCode"),
            # 手机号码
            "phoneNumber": response.get("phone_info").get("phoneNumber"),
            # 纯手机号
            "purePhoneNumber": response.get("phone_info").get("purePhoneNumber"),
        }

    @classmethod
    async def get_oa_access_token(cls) -> Dict[str, str]:
        """
        获取公众号全局唯一后台接口调用凭据
        令牌有效时长2小时,需要定时刷新令牌

        Document:
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html

        Returns:
            Dict[str, str]: ["access_token", "create_time", "expires_in"]

        Author:
            zero
        """
        try:
            current_time: int = int(time.time())
            if cls.mnp_access_token:
                expires_in: int = int(cls.mnp_access_token.get("expires_in"))
                if expires_in > current_time:
                    return cls.mnp_access_token

            config: Dict[str, str] = await WeChatConfig.get_oa_config()
            api = WeixinMpAPI(
                appid=config.get("app_id"),
                app_secret=config.get("app_secret"),
                grant_type="client_credential"
            )

            response = api.client_credential_for_access_token()
            cls.mnp_access_token = {
                # 唯一令牌
                "access_token": response.get("access_token"),
                # 创建时间
                "create_time": current_time,
                # 失效时间
                "expires_in": current_time + 690
            }

            return cls.mnp_access_token
        except OAuth2AuthExchangeError as e:
            cls.mnp_access_token = {}
            raise Exception(str(e.code) + ": " + e.description)

    @classmethod
    async def get_mnp_access_token(cls) -> Dict[str, str]:
        """
        获取小程序全局唯一后台接口调用凭据
        令牌有效时长2小时,需要定时刷新令牌

        Document:
            https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html

        Returns:
            Dict[str, str]: ["access_token", "create_time", "expires_in"]

        Author:
            zero
        """
        try:
            current_time: int = int(time.time())
            if cls.mnp_access_token:
                expires_in: int = int(cls.mnp_access_token.get("expires_in"))
                if expires_in > current_time:
                    return cls.mnp_access_token

            config: Dict[str, str] = await WeChatConfig.get_wx_config()
            api = WeixinMpAPI(
                appid=config.get("app_id"),
                app_secret=config.get("app_secret"),
                grant_type="client_credential"
            )

            response = api.client_credential_for_access_token()
            cls.mnp_access_token = {
                # 唯一令牌
                "access_token": response.get("access_token"),
                # 创建时间
                "create_time": current_time,
                # 失效时间
                "expires_in": current_time + 7200 - 300
            }

            return cls.mnp_access_token
        except OAuth2AuthExchangeError as e:
            cls.mnp_access_token = {}
            raise Exception(str(e.code) + ": " + e.description)
