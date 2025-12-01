/**
 * 充值记录列表类型
 */
interface FinanceRechargeListResponse {
    // ID
    id: number;
    // 订单号
    order_sn: string;
    // 支付金额
    paid_amount: number;
    // 赠送金额
    give_amount: number;
    // 支付方式: [余额支付,微信支付,支付宝支付]
    pay_way: string;
    // 支付状态: [0=未支付, 1=已支付]
    pay_status: number | 0 | 1;
    // 创建时间
    create_time: string;
    // 支付时间
    pay_time: string;
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
