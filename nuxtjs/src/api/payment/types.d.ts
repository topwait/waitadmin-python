/** ------ [支付方式] ------ */
interface PayWayResponse {
    channel: number;
    shorter: string;
    icon: string;
}

/** ------ [支付监听] ------ */
interface PayListenResponse {
    status: number;
    message: string;
}

