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
class ApiConfig:
    # 免登录验证
    not_need_login = [
        "weixin:reply",
        "login:qrcode",
        "login:ticket",
        "login:logout",
        "login:register",
        "login:oa_login",
        "login:mobile_login",
        "login:account_login",
        "payment:notify_mnp",
        "payment:notify_ali",
        "user:forget_pwd",
        "user:bind_wechat",
        "index:homing",
        "index:config",
        "index:policy",
        "index:send_sms",
        "index:send_email",
        "article:lists",
        "article:pages",
        "article:detail"
    ]

    # 需记日志
    add_record_log = [
        "login:account_login",
        "login:mobile_login",
        "login:oa_login",
        "index:homing",
        "article:lists",
        "article:detail"
    ]

    # 安全配置项
    security = {
        # 令牌数量限制
        "token_limit": 100,
        # 令牌过期时间
        "token_timeout": 7200,
        # 令牌续签期限
        "token_renewal": 1800,
        # 支持并发登录
        "is_concurrent": True,
        # 缓存前缀名称
        "cache_prefix": "login:api_"
    }
