/**
 * 支付方式类型
 */
interface PayWayResponse {
    // 支付渠道
    channel: number;
    // 支付名称
    shorter: string;
    // 支付图标
    icon: string;
}

/**
 * 支付监听类型
 */
interface PayListenResponse {
    // 订单状态: [-1=订单不存在, 0=未支付, 1=已支付, 2=已过期]
    status: number;
    // 状态描述
    message: string;
}
