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
from exception import AppException
from common.utils.config import ConfigUtil
from apps.admin.schemas.setting import login_schema as schema


class LoginService:
    """ 登录配置服务类 """

    @classmethod
    async def detail(cls) -> schema.LoginDetailVo:
        """
        登录配置详情。

        Returns:
            schema.LoginDetailVo: 登录配置详情Vo。

        Author:
            zero
        """
        conf = await ConfigUtil.get("login") or {}
        pc = conf.get("pc") or {}

        return schema.LoginDetailVo(
            pc=schema.LoginConfig(
                is_agreement=bool(pc.get("is_agreement", False)),
                default_method=pc.get("default_method", "account"),
                usable_channel=pc.get("usable_channel", []),
                usable_register=pc.get("usable_register", [])
            )
        )

    @classmethod
    async def save(cls, post: schema.LoginDetailVo):
        """
        登录配置保存。

         Args:
            post (schema.LoginDetailVo): 登录配置参数。

        Author:
            zero
        """
        client = {"pc": "PC端"}
        orders = ["account", "mobile", "email", "wx"]

        config = post.model_dump()
        for k in ["pc"]:
            # 读取数据
            defaults = config[k]["default_method"]
            channels = config[k]["usable_channel"]
            register = config[k]["usable_register"]

            # 从新排序
            config[k]["usable_channel"] = sorted(channels, key=lambda x: orders.index(x))
            config[k]["usable_register"] = sorted(register, key=lambda x: orders.index(x))

            # 验证渠道
            if channels and defaults not in channels:
                 raise AppException(f"{client[k]}『默认登录方式』尚未在可用登录方式启用")

        await ConfigUtil.set("login", "pc", config["pc"])
