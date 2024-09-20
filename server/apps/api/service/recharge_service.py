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
from typing import List
from pydantic import TypeAdapter
from exception import AppException
from common.enums.pay import PayEnum
from common.utils.tools import ToolsUtil
from common.utils.config import ConfigUtil
from common.models.market import RechargeOrderModel
from common.models.market import RechargePackageModel
from apps.api.schemas import recharge_schema as schema


class RechargeService:
    """ 充值服务类 """

    @classmethod
    async def package(cls) -> List[schema.RechargePackageVo]:
        """
        发起充值

        Returns:
            List[schema.RechargePackageVo]: 套餐列表Vo。

        Author:
            zero
        """
        lists = await RechargePackageModel\
            .filter(is_show=1, is_delete=0)\
            .order_by("-sort", "-id")\
            .all().values("id", "name", "money", "give_money")

        return [TypeAdapter(schema.RechargePackageVo).validate_python(item) for item in lists]

    @classmethod
    async def place(cls, user_id: int, terminal: int, post: schema.RechargeIn) -> schema.RechargePlaceVo:
        """
        发起充值

        Args:
            user_id (int): 用户ID。
            terminal (int): 操作平台。
            post (schema.RechargeIn): 充值参数。

        Returns:
            schema.RechargePlaceVo: 下单结果Vo。

        Author:
            zero
        """
        give_amount: Decimal = Decimal(0)
        paid_amount: Decimal = Decimal(post.money)

        config = await ConfigUtil.get("recharge") or {"status": 0, "min_recharge": 0}
        if config.get("status"):
            raise AppException("充值通道已关闭")

        # 查询下套餐
        if post.package_id:
            package = await RechargePackageModel.filter(id=post.package_id, is_delete=0).first()
            if not package:
                raise AppException("套餐不存在")
            if not package.is_show:
                raise AppException("套餐已下架")
            give_amount = package.give_money
            paid_amount = package.money
        else:
            if config.get("min_recharge") and paid_amount < config.get("min_recharge"):
                raise AppException(f"最低充值金额不能少于: " + str(config.get("min_recharge")))

        # 创建订单
        order = await RechargeOrderModel.create(
            user_id=user_id,
            terminal=terminal,
            order_sn=await ToolsUtil.make_order_sn(RechargeOrderModel, "order_sn"),
            pay_way=PayEnum.WAY_MNP,
            package_id=post.package_id,
            paid_amount=paid_amount,
            give_amount=give_amount,
            create_time=int(time.time()),
            update_time=int(time.time())
        )

        return schema.RechargePlaceVo(
            order_id=order.id,
            paid_amount=post.paid_amount
        )
