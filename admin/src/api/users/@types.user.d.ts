/**
 * 用户列表类型
 */
interface UserListResponse {
    // ID
    id: number;
    // 用户编号
    sn: string;
    // 所属分组
    group: string;
    // 用户名称
    nickname: string;
    // 用户头像
    avatar: string;
    // 手机号码
    mobile: string;
    // 电子邮箱
    email: string;
    // 是否显示
    is_disable: boolean;
    // 创建时间
    create_time: string;
    // 更新时间
    update_time: string;
}

/**
 * 用户详情类型
 */
interface UserDetailResponse {
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
    // 用户性别
    gender: string;
    // 手机号码
    mobile: string;
    // 电子邮箱
    email: string;
    // 钱包余额
    balance: number;
    // 是否显示
    is_disable: boolean;
    // 最后登录IP
    last_login_ip: string;
    // 最后登录时间
    last_login_time: string;
    // 创建时间
    create_time: string;
}

/**
 * 余额日志类型
 */
interface UserWalletLogsResponse {
    // ID
    id: number;
    // 操作类型: [1=增加, 2=减少]
    action: number | 1 | 2;
    // 操作人
    op_user: string;
    // 日志编号
    log_sn: string;
    // 来源类型
    source_type: string;
    // 来源单号
    source_sn: string;
    // 变更金额
    change_amount: number;
    // 变更前金额
    before_amount: number;
    // 变更后金额
    after_amount: number;
    // 备注信息
    remarks: string;
    // 创建时间
    create_time: string;
}

/**
 * 会话列表类型
 */
interface UserSessionResponse {
    // UUID
    uuid: string;
    // 提示
    tips: string;
    // 设备
    device: string;
    // 状态: [1=在线, 2=已失效, 3=踢下线]
    status: number | 1 | 2 | 3;
    // 登录主机
    login_host: string;
    // 剩余时长
    surplus_time: string;
    // 创建时间
    create_time: string;
    // 失效时间
    expire_time: string;
    // 最后操作时间
    last_op_time: string;
    // 最后操作IP
    last_ip_address: string;
    // 最后操作UA
    last_ua_browser: string;
}
