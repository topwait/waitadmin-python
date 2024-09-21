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
from typing import Dict
from common.utils.config import ConfigUtil


class WeChatConfig:
    """ 微信参数配置类 """

    @classmethod
    async def get_wx_config(cls) -> Dict[str, str]:
        """ 小程序配置 """
        config = await ConfigUtil.get("wx_channel") or {}
        return {
            "app_id": config.get("app_id", "").strip(),
            "app_secret": config.get("app_secret", "").strip()
        }

    @classmethod
    async def get_oa_config(cls) -> Dict[str, str]:
        """ 公众号配置 """
        config = await ConfigUtil.get("oa_channel") or {}
        return {
            "app_id": config.get("app_id", "").strip(),
            "app_secret": config.get("app_secret", "").strip(),
            "token": config.get("token", "wa").strip(),
            "aes_key": config.get("aes_key", "").strip(),
        }

    @classmethod
    async def get_op_config(cls) -> Dict[str, str]:
        """ 开发平台配置 """
        config = await ConfigUtil.get("op_channel") or {}
        return {
            "app_id": config.get("app_id", "").strip(),
            "app_secret": config.get("app_secret", "").strip()
        }
