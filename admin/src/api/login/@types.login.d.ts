/**
 * 登录验证码类型
 */
interface LoginCaptchaResponse {
    uuid: string;
    image: string;
}

/**
 * 登录成功类型
 */
interface LoginSuccessResponse {
    token: string;
    username: string;
    nickname: string;
    avatar: string;
}
