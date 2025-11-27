/**
 * 个人中心类型
 */
interface UserCenterResponse {
    id: number;
    sn: string;
    account: string;
    nickname: string;
    avatar: string;
    mobile: string;
    email: string;
    collect: number;
    balance: number;
    gender: number;
    is_wechat: number;
    is_password: number;
    create_time: string;
    last_login_time: string;
}

/**
 * 我的收藏类型
 */
interface UserCollectResponse {
    id: number;
    image: string;
    title: string;
    browse: number;
    collect: number;
    create_time: string;
}
