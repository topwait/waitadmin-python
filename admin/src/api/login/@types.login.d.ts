/**
 * 登录验证码类型
 */
interface LoginCaptchaResponse {
    // UUID
    uuid: string;
    // 验证码图
    image: string;
}

/**
 * 登录成功类型
 */
interface LoginSuccessResponse {
    // Token
    token: string;
    // 用户账号
    username: string;
    // 用户昵称
    nickname: string;
    // 用户头像
    avatar: string;
}
