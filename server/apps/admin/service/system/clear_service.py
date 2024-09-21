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
from apps.admin.schemas.system import clear_schema as schema
from common.utils.cache import RedisUtil


class ClearService:

    @classmethod
    async def clean(cls, post: schema.CleanIn):
        """
        清理系统缓存。

        Args:
           post (schema.CleanIn): 清理参数。

        Author:
            zero
        """
        if post.system:
            await RedisUtil.delete("sys:config")

        if post.login:
            cursor = 0
            while True:
                cursor, keys = await RedisUtil.scan_keys("login:*", cursor)
                for key in keys:
                    await RedisUtil.delete(key)
                if cursor == 0:
                    break
