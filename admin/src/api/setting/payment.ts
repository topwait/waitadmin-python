import request from '@/utils/request'

const paymentApi = {
    /**
     * 支付配置列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/setting/payment/lists'
        })
    },

    /**
     * 支付配置详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/payment/detail',
            params: { id }
        })
    },

    /**
     * 支付配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/payment/save',
            params
        })
    }
}

export default paymentApi
