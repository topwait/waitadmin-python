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
import json
import time

from common.utils.cache import RedisUtil
from common.models.sys import SysConfigModel


class ConfigUtil:
    """ 配置工具 """

    SYSTEM_CONFIG_KEY: str = "sys:config"

    @classmethod
    async def get(cls, type_: str, key: str = "", default_: any = None):
        """
        读取配置

        Args:
            type_ (str): 配置类型。
            key (str, optional): 配置键: 默认为空字符串。
            default_ (any, optional): 默认值: 当无法获取配置时返回,默认为None。

        Returns:
            any: 返回获取到的配置值,如果无法获取则返回默认值。

        Author:
            zero
        """
        cache_data = await RedisUtil.get(cls.SYSTEM_CONFIG_KEY)

        if not cache_data:
            lists = await SysConfigModel.all().values("type", "key", "value")

            results = {}
            for item in lists:
                if item["type"] not in results:
                    results[item["type"]] = {}
                results[item["type"]][item["key"]] = item["value"]

            cache_data = results
            await RedisUtil.set(cls.SYSTEM_CONFIG_KEY, json.dumps(results))
        else:
            cache_data = json.loads(str(cache_data))

        if key:
            value = cache_data.get(type_, {}).get(key)

            if value is not None and value != "":
                try:
                    json_value = json.loads(value)
                    if isinstance(json_value, dict):
                        value = json_value
                except json.JSONDecodeError:
                    pass

            if value is None and default_ is not None:
                return default_

            return value

        data = cache_data.get(type_)
        if isinstance(data, dict):
            for k, v in data.items():
                if v is None:
                    continue

                try:
                    json_value = json.loads(v)
                    if isinstance(json_value, (dict, list)):
                        data[k] = json_value
                except json.JSONDecodeError:
                    pass

        if data is None and default_ is not None:
            return default_

        return data

    @classmethod
    async def set(cls, type_: str,  key: str, value: any, remarks: str = None):
        """
        设置配置

        Args:
            type_ (str): 型。
            key (str): 键。
            value (any): 值。
            remarks (str, optional): 备注信息, 默认为None。

        Returns:
            None

        Author:
            zero
        """

        await RedisUtil.delete(cls.SYSTEM_CONFIG_KEY)

        if isinstance(value, (list, dict, tuple, set)):
            value = json.dumps(value)

        result = await SysConfigModel.filter(type=type_, key=key).first()
        if not result:
            await SysConfigModel.create(
                type=type_,
                key=key,
                value=value,
                remarks=remarks if remarks is not None else "",
                create_time=int(time.time()),
                update_time=int(time.time())
            )
        else:
            _data: dict = {
                "value": value,
                "update_time": int(time.time())
            }

            if remarks is not None:
                _data["remarks"] = remarks

            await SysConfigModel.filter(type=type_, key=key).update(**_data)

