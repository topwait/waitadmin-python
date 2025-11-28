const paymentApi = {
    /**
     * 支付方式
     *
     * @returns {Promise<PayWayResponse>}
     * @author zero
     */
    payWay(): Promise<PayWayResponse> {
        return $request.get<PayWayResponse>({
            url: '/payment/pay_way'
        })
    },

    /**
     * 支付监听
     *
     * @param params
     * @param {number} params.order_id - 订单ID
     * @param {string} params.attach - 附加数据
     * @returns {Promise<PayListenResponse>}
     * @author zero
     */
    listen(params: {
        order_id: number;
        attach: string;
    }): Promise<PayListenResponse> {
        return $request.get<PayListenResponse>({
            url: '/payment/listen',
            params
        })
    },

    /**
     * 发起支付
     *
     * @param params
     * @param {number} params.order_id - 订单ID
     * @param {number} params.pay_way - 支付方式
     * @param {string} params.attach - 附加数据
     * @param {string} [params.redirect_url] - 跳转地址
     * @returns {Promise<any>}
     * @author zero
     */
    prepay(params: {
        order_id: number;
        pay_way: number;
        attach: string;
        redirect_url?: string;
    }): Promise<any> {
        return $request.post({
            url: '/payment/prepay',
            params
        })
    }
}

export default paymentApi
