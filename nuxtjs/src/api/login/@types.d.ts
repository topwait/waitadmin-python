/**
 * 登录结果类型
 */
interface LoginResultResponse {
    // 令牌
    token: string;
}

/**
 * 微信二维码类型
 */
interface LoginQrcodeResponse {
    // Key
    key: string;
    // URL
    url: string;
    // Ticket
    ticket: string;
    // 有效秒数
    expire_seconds: number;
}

/**
 * 扫码检测类型
 */
interface LoginTicketResponse {
    // 状态: [0=等待扫码, 1=扫码失败, 2=扫码确认, 3=扫码成功]
    status: number;
    // 时效
    expire: number;
    // 令牌
    token: string;
}
