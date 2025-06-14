import request from '@/utils/request'

const balanceApi = {
    /**
     * 余额明细列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.user]
     * @param {number} [params.source_type]
     * @param {string} [params.start_time]
     * @param {string} [params.end_time]
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
