/**
 * 登录结果类型
 */
interface LoginResultResponse {
    token: string;
}

/**
 * 微信二维码类型
 */
interface LoginQrcodeResponse {
    key: string;
    url: string;
    ticket: string;
    expire_seconds: number;
}

/**
 * 扫码检测类型
 */
interface LoginTicketResponse {
    status: number;
    expire: number;
    token: string;
}
