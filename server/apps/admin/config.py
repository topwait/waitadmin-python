# +----------------------------------------------------------------------
# | WaitAdmin(fastapi)快速开发后台管理系统
# +----------------------------------------------------------------------
# | 欢迎阅读学习程序代码,建议反馈是我们前进的动力
# | 程序完全开源可支持商用,允许去除界面版权信息
# | gitee:   https://gitee.com/wafts/waitadmin_fastapi
# | github:  https://github.com/topwait/waitadmin_fastapi
# | 官方网站: https://www.waitadmin.cn
# | WaitAdmin团队版权所有并拥有最终解释权
# +----------------------------------------------------------------------
# | Author: WaitAdmin Team <2474369941@qq.com>
# +----------------------------------------------------------------------
class AdminConfig:
    # 免登录验证
    not_need_login = [
        "index:config",
        "login:captcha",
        "login:check"
    ]

    # 免权限验证
    not_need_perms = [
        "login:logout",
        "attach:cate_lists",
        "attach:album_lists",
        "auth:admin:oneself",
        "auth:admin:set_info",
        "auth:role:whole",
        "auth:dept:whole",
        "auth:post:whole",
        "content:category:whole"
    ]

    # 登录验证码
    enable_captcha = True
