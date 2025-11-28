/**
 * 个人中心类型
 */
interface UserCenterResponse {
    // ID
    id: number;
    // 用户编号
    sn: string;
    // 用户账号
    account: string;
    // 用户名称
    nickname: string;
    // 用户头像
    avatar: string;
    // 手机号码
    mobile: string;
    // 电子邮箱
    email: string;
    // 收藏数量
    collect: number;
    // 钱包余额
    balance: number;
    // 用户性别: [0=未知, 1=男, 2=女]
    gender: number;
    // 已绑微信: [0=否, 1=是]
    is_wechat: number;
    // 已设密码: [0=否, 1=是]
    is_password: number;
    // 注册时间
    create_time: string;
    // 最后登录时间
    last_login_time: string;
}

/**
 * 我的收藏类型
 */
interface UserCollectResponse {
    // ID
    id: number;
    // 封面图
    image: string;
    // 文章标题
    title: string;
    // 阅读量
    browse: number;
    // 收藏量
    collect: number;
    // 收藏时间
    create_time: string;
}
