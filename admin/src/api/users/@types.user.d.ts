/**
 * 用户列表类型
 */
interface UserListResponse {
    id: number;
    sn: string;
    group: string;
    nickname: string;
    avatar: string;
    mobile: string;
    email: string;
    is_disable: number;
    create_time: string;
    update_time: string;
}

/**
 * 用户详情类型
 */
interface UserDetailResponse {
    id: number;
    sn: string;
    account: string;
    nickname: string;
    avatar: string;
    gender: string;
    mobile: string;
    email: string;
    balance: number;
    is_disable: number;
    last_login_ip: string;
    last_login_time: string;
    create_time: string;
}

/**
 * 余额日志类型
 */
interface UserWalletLogsResponse {
    id: number;
    action: number;
    op_user: string;
    log_sn: string;
    source_type: string;
    source_sn: string;
    change_amount: number;
    before_amount: number;
    after_amount: number;
    remarks: string;
    create_time: string;
}

/**
 * 会话列表类型
 */
interface UserSessionResponse {
    uuid: string;
    tips: string;
    device: string;
    status: number;
    login_host: string;
    create_time: string;
    expire_time: string;
    last_op_time: string;
    last_ip_address: string;
    last_ua_browser: string;
}
