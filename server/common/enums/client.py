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
class ClientEnum:
    # 访问终端专属
    MNP = 1      # 微信小程序
    OA = 2       # 微信公众号
    H5 = 3       # H5(非微信)
    PC = 4       # 电脑端
    ANDROID = 5  # 安卓端
    IOS = 6      # 苹果端

    # 微信授权专属
    WX_MNP = 1   # 微信小程序
    WX_OA = 2    # 微信公众号

    @classmethod
    def get_msg_by_code(cls, code: int) -> str:
        _desc = {
            cls.MNP: "微信小程序",
            cls.OA: "公众号",
            cls.H5: "H5",
            cls.PC: "电脑",
            cls.ANDROID: "安卓",
            cls.IOS: "苹果"
        }
        return _desc.get(code, "")
