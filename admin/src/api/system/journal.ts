import request from '@/utils/request'

const journalApi = {
    /**
     * 系统日志列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        method?: string;
        url?: string;
        ip?: string;
        start_time?: string;
        end_time?: string;
    }): Promise<any> {
        return request.get({
            url: '/system/journal/lists',
            params
        })
    },

    /**
     * 系统日志详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/system/journal/detail',
            params: { id }
        })
    }
}

export default journalApi
