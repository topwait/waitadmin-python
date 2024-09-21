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


class WalletEnum:
    UM_DEC_ADMIN = 1001        # 平台扣减余额
    UM_DEC_RECHARGE = 1002     # 退款扣减余额

    UM_INC_ADMIN = 1501        # 平台增加余额
    UM_INC_RECHARGE = 1502     # 充值增加余额

    @classmethod
    def get_source_type_msg(cls, code) -> Union[str, Dict[int, str]]:
        _desc = {
            cls.UM_DEC_ADMIN: "平台扣减余额",
            cls.UM_DEC_RECHARGE: "退款扣减余额",


            cls.UM_INC_ADMIN: "平台增加余额",
            cls.UM_INC_RECHARGE: "充值增加余额",
        }
        if isinstance(code, bool) and code:
            return _desc
        return _desc.get(code, "")
