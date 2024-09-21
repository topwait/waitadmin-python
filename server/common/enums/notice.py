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
class NoticeEnum:
    # 通知状态
    STATUS_WAIT = 0  # 等待
    STATUS_OK = 1    # 成功
    STATUS_FAIL = 2  # 失败

    # 查看状态
    VIEW_UNREAD = 0  # 未读
    VIEW_READ = 1    # 已读

    # 通知类型
    SENDER_SYS = 1   # 系统类型
    SENDER_EMS = 2   # 邮件类型
    SENDER_SMS = 3   # 短信类型
    SENDER_MNP = 4   # 小程序类型
    SENDER_OA = 5    # 公众号类型

    # 通知渠道
    LOGIN = 101          # 短信免密登录
    FORGET_PWD = 102     # 找回登录密码
    MOBILE_REG = 103     # 手机注册账号
    MOBILE_BIND = 104    # 手机号码绑定
    MOBILE_CHANGE = 105  # 手机号码变更
    EMAIL_REG = 106      # 邮箱注册账号
    EMAIL_BIND = 107     # 邮箱号码变更
    EMAIL_CHANGE = 108   # 邮箱号码绑定
