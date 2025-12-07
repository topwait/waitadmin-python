import request from '@/utils/request'

const noticeApi = {
    /**
     * 通知配置列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {number} params.client
     * @returns {Promise<SettingNoticeListResponse[]>}
     * @author zero
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        client: number;
    }): Promise<SettingNoticeListResponse[]> {
        return request.get<SettingNoticeListResponse[]>({
            url: '/setting/notice/lists',
            params
        })
    },

    /**
     * 通知配置详情
     *
     * @param {number} id
     * @returns {Promise<SettingNoticeDetailResponse>}
     * @author zero
     */
    detail(id: number): Promise<SettingNoticeDetailResponse> {
        return request.get<SettingNoticeDetailResponse>({
            url: '/setting/notice/detail',
            params: { id }
        })
    },

    /**
     * 通知配置保存
     *
     * @param {SettingNoticeDetailResponse} params
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: SettingNoticeDetailResponse): Promise<any> {
        return request.post({
            url: '/setting/notice/save',
            params
        })
    }
}

export default noticeApi
