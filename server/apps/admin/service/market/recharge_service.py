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
from decimal import Decimal
from typing import List, Dict, Union
from common.utils.times import TimeUtil
from common.utils.config import ConfigUtil
from common.models.market import RechargePackageModel
from apps.admin.schemas.market import recharge_schema as schema


class RechargeService:

    @classmethod
    async def lists(cls) -> Dict[str, Union[schema.RechargeConfigIn, schema.RechargePackageListVo]]:
        """
        充值套餐详情

        Returns:
            List[schema.RechargePackageListVo]: 充值套餐列表Vo。

        Author:
            zero
        """
        lists = await RechargePackageModel.filter(is_delete=0).order_by("-sort", "-id").all()
        _data = []
        for item in lists:
            _data.append(schema.RechargePackageListVo(
                id=item.id,
                money=item.money,
                give_money=item.give_money,
                sort=item.sort,
                is_show=item.is_show,
                create_time=TimeUtil.timestamp_to_date(item.create_time),
                update_time=TimeUtil.timestamp_to_date(item.update_time),
            ))

        config = await ConfigUtil.get("recharge") or {}
        extend = schema.RechargeConfigIn(
            status=int(config.get("status", 0)),
            min_recharge=Decimal(config.get("min_recharge", 0))
        )

        return {"extend": extend, "lists": _data}

    @classmethod
    async def detail(cls, id_: int) -> schema.RechargePackageDetailVo:
        """
        充值套餐详情

        Args:
            id_ (int): 套餐ID。

        Returns:
            schema.RechargePackageDetailVo: 充值套餐详情Vo。

        Author:
            zero
        """
        package = await RechargePackageModel.filter(id=id_, is_delete=0).get()
        return schema.RechargePackageDetailVo(
            id=package.id,
            money=package.money,
            give_money=package.give_money,
            sort=package.sort,
            is_show=package.is_show,
        )

    @classmethod
    async def add(cls, post: schema.RechargePackageAddIn):
        """
        充值套餐新增

        Args:
            post (schema.RechargePackageAddIn): 套餐新增参数。

        Author:
            zero
        """
        await RechargePackageModel.create(
            money=post.money,
            give_money=post.give_money,
            sort=post.sort,
            is_show=post.is_show,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

    @classmethod
    async def edit(cls, post: schema.RechargePackageEditIn):
        """
        充值套餐编辑

        Args:
            post (schema.RechargePackageEditIn): 套餐编辑参数。

        Author:
            zero
        """
        await RechargePackageModel.filter(id=post.id, is_delete=0).get()
        await RechargePackageModel.filter(id=post.id).update(
            money=post.money,
            give_money=post.give_money,
            sort=post.sort,
            is_show=post.is_show,
            update_time=int(time.time())
        )

    @classmethod
    async def delete(cls, id_: int):
        """
        充值套餐删除

        Args:
            id_ (int): 套餐ID。

        Author:
            zero
        """
        await RechargePackageModel.filter(id=id_).get()
        await RechargePackageModel.filter(id=id_).update(
            is_delete=1,
            delete_time=int(time.time())
        )

    @classmethod
    async def config(cls, post: schema.RechargeConfigIn):
        """
        充值配置修改

        Args:
            post (schema.RechargeConfigIn): 配置参数。

        Author:
            zero
        """
        await ConfigUtil.set("recharge", "status", post.status)
        await ConfigUtil.set("recharge", "min_recharge", post.min_recharge)
