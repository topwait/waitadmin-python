/**
 * 支付方式类型
 */
interface PayWayResponse {
    channel: number;
    shorter: string;
    icon: string;
}

/**
 * 支付监听类型
 */
interface PayListenResponse {
    status: number;
    message: string;
}

