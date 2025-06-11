import request from '@/utils/request'

const balanceApi = {
    /**
     * 余额明细列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        user?: string;
        source_type?: number;
        start_time?: string;
        end_time?: string;
    }): Promise<any> {
        return request.get({
            url: '/finance/balance/lists',
            params
        })
    }
}

export default balanceApi
