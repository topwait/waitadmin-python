/**
 * 余额明细列表类型
 */
interface FinanceBalanceListResponse {
    id: number;
    log_sn: string;
    action: number;
    source_sn: string;
    source_type: string;
    change_amount: number;
    before_amount: number;
    after_amount: number;
    create_time: string;
    user: {
        sn: string;
        avatar: string;
        mobile: string;
        nickname: string;
    }
}
