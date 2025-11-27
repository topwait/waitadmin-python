/**
 * 充值记录列表类型
 */
interface FinanceRechargeListResponse {
    id: number;
    order_sn: string;
    paid_amount: number;
    give_amount: number;
    pay_way: string;
    pay_status: number;
    create_time: string;
    pay_time: string;
    user: {
        sn: string;
        avatar: string;
        mobile: string;
        nickname: string;
    }
}
