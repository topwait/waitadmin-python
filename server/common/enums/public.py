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


class BannerEnum:
    HOME = 10  # 首页轮播
    SIDE = 20  # 侧边广告

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        _desc = {
            cls.HOME: "首页轮播",
            cls.SIDE: "侧边广告"
        }
        return _desc.get(code, "")

    @classmethod
    def get_positions(cls) -> Dict[int, str]:
        return {
            cls.HOME: "首页轮播",
            cls.SIDE: "侧边广告"
        }
