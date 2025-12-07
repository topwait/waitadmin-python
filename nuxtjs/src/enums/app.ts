// 弹窗枚举
export enum popupEnum {
    NULL = '',                    // 空
    LOGIN = 'login',              // 登录
    REGISTER = 'register',        // 注册
    FORGOT_PWD = 'forgot_pwd',    // 忘记密码
    CHANGE_PWD = 'change_pwd',    // 修改密码
    BIND_EMAIL = 'bind_email',    // 绑定邮箱
    BIND_MOBILE = 'bind_mobile',  // 绑定手机
    BIND_WECHAT = 'bind_wechat'   // 绑定微信
}

// 协议枚举
export enum policyEnum {
    SERVICE = 'service',  // 服务协议
    PRIVACY = 'privacy',  // 隐私协议
    PAYMENT = 'payment'   // 支付协议
}
