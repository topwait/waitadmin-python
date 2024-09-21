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
from tortoise.models import in_transaction
from common.enums.pay import PayEnum
from common.enums.wallet import WalletEnum
from common.models.users import UserModel
from common.models.users import UserWalletModel
from common.models.market import RechargeOrderModel


class PayNotifyService:
    """ 支付回调服务类 """

    @classmethod
    async def handle(cls, action: str, order_sn: str, transaction_id: str = ""):
        async with in_transaction("mysql"):
            if action == "recharge":
                await cls.recharge(order_sn, transaction_id)

    @classmethod
    async def recharge(cls, order_sn: str, transaction_id: str = ""):
        # 查询订单
        order = await RechargeOrderModel.filter(order_sn=order_sn).first()

        # 查询用户
        user = await UserModel.filter(id=order.user_id).first()

        # 增加余额
        recharge_amount = (order.paid_amount + order.give_amount)
        user.balance += recharge_amount
        await user.save()

        # 更新状态
        order.pay_time = int(time.time())
        order.pay_status = PayEnum.PAID_OK
        order.transaction_id = transaction_id
        await order.save()

        # 记录流水
        await UserWalletModel.inc(
            user_id=user.id,
            source_type=WalletEnum.UM_DEC_RECHARGE,
            change_amount=recharge_amount,
            source_id=order.id,
            source_sn=order.order_sn,
            remarks=WalletEnum.get_source_type_msg(WalletEnum.UM_DEC_RECHARGE),
        )
