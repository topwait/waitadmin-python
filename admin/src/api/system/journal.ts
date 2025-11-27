import request from '@/utils/request'

const journalApi = {
    /**
     * 系统日志列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.method]
     * @param {string} [params.url]
     * @param {string} [params.ip]
     * @param {string} [params.start_time]
     * @param {string} [params.end_time]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        method?: string;
        url?: string;
        ip?: string;
        start_time?: string;
        end_time?: string;
    }): Promise<SystemJournalListResponse[]> {
        return request.get<SystemJournalListResponse[]>({
            url: '/system/journal/lists',
            params
        })
    },

    /**
     * 系统日志详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<SystemJournalDetailResponse> {
        return request.get<SystemJournalDetailResponse>({
            url: '/system/journal/detail',
            params: { id }
        })
    }
}

export default journalApi
