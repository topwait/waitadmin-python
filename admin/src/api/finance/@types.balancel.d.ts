/**
 * 余额明细列表类型
 */
interface FinanceBalanceListResponse {
    // ID
    id: number;
    // 日志编号
    log_sn: string;
    // 变动类型: [1=增加, 2=减少]
    action: number;
    // 来源单号
    source_sn: string;
    // 来源类型
    source_type: string;
    // 变动的金额
    change_amount: number;
    // 变动前金额
    before_amount: number;
    // 变动后金额
    after_amount: number;
    // 创建时间
    create_time: string;
    // 用户
    user: {
        // 编号
        sn: string;
        // 头像
        avatar: string;
        // 手机号
        mobile: string;
        // 昵称
        nickname: string;
    }
}
