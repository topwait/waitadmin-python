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
from typing import Union, Dict


class PayEnum:
    # 支付方式
    WAY_BALANCE = 1  # 余额支付
    WAY_MNP = 2      # 微信支付
    WAY_ALI = 3      # 支付宝支付

    # 支付状态
    PAID_NO = 0  # 待支付
    PAID_OK = 1  # 待支付

    @classmethod
    def get_pay_way_msg(cls, code) -> Union[str, Dict[int, str]]:
        """ 支付方式描述 """
        _desc = {
            cls.WAY_BALANCE: "余额支付",
            cls.WAY_MNP: "微信支付",
            cls.WAY_ALI: "支付宝支付"
        }
        if isinstance(code, bool) and code:
            return _desc
        return _desc.get(code, "")

    # @classmethod
    # def get_pay_alias_msg(cls, code) -> Union[int, Dict[str, int]]:
    #     """ 支付别名描述 """
    #     _desc = {
    #         "balance": cls.WAY_BALANCE,
    #         "wxpay": cls.WAY_MNP,
    #         "alipay": cls.WAY_ALI
    #     }
    #     if isinstance(code, bool) and code:
    #         return _desc
    #     return int(_desc.get(code, 0))

    @classmethod
    def get_pay_status_msg(cls, code) -> Union[str, Dict[int, str]]:
        """ 支付状态描述 """
        _desc = {
            cls.PAID_NO: "待支付",
            cls.PAID_OK: "已支付"
        }
        if isinstance(code, bool) and code:
            return _desc
        return _desc.get(code, "")
