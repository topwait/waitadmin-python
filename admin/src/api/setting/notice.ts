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
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.scene
     * @param {string} params.name
     * @param {string} params.type
     * @param {string} params.client
     * @param {string} [params.remarks]
     * @param {any} params.variable
     * @param {any} params.sys_template
     * @param {any} params.ems_template
     * @param {any} params.sms_template
     * @returns {Promise<any>}
     * @author zero
     */
    save(params: {
        id: number;
        scene: number;
        name: string;
        type: string;
        client: string;
        remarks?: string;
        variable: any;
        sys_template: any;
        ems_template: any;
        sms_template: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/notice/save',
            params
        })
    }
}

export default noticeApi
