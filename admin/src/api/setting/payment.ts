import request from '@/utils/request'

const paymentApi = {
    /**
     * 支付配置列表
     *
     * @returns {Promise<SettingPaymentListResponse[]>}
     * @author zero
     */
    lists(): Promise<SettingPaymentListResponse[]> {
        return request.get<SettingPaymentListResponse[]>({
            url: '/setting/payment/lists'
        })
    },

    /**
     * 支付配置详情
     *
     * @param {number} id
     * @returns {Promise<SettingPaymentDetailResponse>}
     * @author zero
     */
    detail(id: number): Promise<SettingPaymentDetailResponse> {
        return request.get<SettingPaymentDetailResponse>({
            url: '/setting/payment/detail',
            params: { id }
        })
    },

    /**
     * 支付配置保存
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.channel
     * @param {string} params.shorter
     * @param {string} params.name
     * @param {string} params.icon
     * @param {number} params.sort
     * @param {boolean} params.status
     * @param {any} params.params
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: {
        id: number;
        channel: number;
        shorter: string;
        name: string;
        icon: string;
        sort: number;
        status: boolean;
        params: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/payment/save',
            params
        })
    }
}

export default paymentApi
