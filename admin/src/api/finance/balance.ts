import request from '@/utils/request'

const balanceApi = {
    /**
     * 余额明细列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/finance/balance/lists',
            params
        })
    }
}

export default balanceApi
