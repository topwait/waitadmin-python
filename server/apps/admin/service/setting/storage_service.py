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
from apps.admin.schemas.setting import storage_schema as schema


class StorageService:
    """ 存储配置服务类 """

    @classmethod
    async def detail(cls) -> schema.StorageDetailVo:
        """
        存储配置详情。

        Returns:
            schema.StorageConfigs: 存储配置详情Vo。

         Author:
            zero
        """
        configs = await ConfigUtil.get("storage") or {}
        return schema.StorageDetailVo(
            drive=configs.get("engine", "local"),
            qiniu=schema.StorageParams(
                bucket=configs.get("qiniu", {}).get("bucket", ""),
                domain=configs.get("qiniu", {}).get("domain", ""),
                access_key=configs.get("qiniu", {}).get("access_key", ""),
                secret_key=configs.get("qiniu", {}).get("secret_key", ""),
            ),
            aliyun=schema.StorageParams(
                bucket=configs.get("aliyun", {}).get("bucket", ""),
                domain=configs.get("aliyun", {}).get("domain", ""),
                access_key=configs.get("aliyun", {}).get("access_key", ""),
                secret_key=configs.get("aliyun", {}).get("secret_key", ""),
                region=configs.get("aliyun", {}).get("region", ""),
            ),
            qcloud=schema.StorageParams(
                bucket=configs.get("qcloud", {}).get("bucket", ""),
                domain=configs.get("qcloud", {}).get("domain", ""),
                access_key=configs.get("qcloud", {}).get("access_key", ""),
                secret_key=configs.get("qcloud", {}).get("secret_key", ""),
                region=configs.get("qcloud", {}).get("region", ""),
            ),
        )

    @classmethod
    async def save(cls, post: schema.StorageDetailVo):
        """
        存储配置保存。

        Args:
            post (schema.StorageConfigs): 存储配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("storage", "engine", post.drive)
        await ConfigUtil.set("storage", "qiniu", post.qiniu.dict())
        await ConfigUtil.set("storage", "aliyun", post.aliyun.dict())
        await ConfigUtil.set("storage", "qcloud", post.qcloud.dict())
