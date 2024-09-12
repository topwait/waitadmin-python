/** ------[登录结果] ------ */
interface LoginResultResponse {
    token: string;
}

/** ------[微信二维码] ------ */
interface LoginQrcodeResponse {
    key: string;
    url: string;
    ticket: string;
    expire_seconds: number;
}

/** ------[扫码检测] ------ */
interface LoginTicketResponse {
    status: number;
    expire: number;
    token: string;
}
