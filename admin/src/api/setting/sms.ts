import request from '@/utils/request'

const smsApi = {
    /**
     * 短信配置列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/setting/sms/lists'
        })
    },

    /**
     * 短信配置详情
     *
     * @param {string} alias
     */
    detail(alias: string): Promise<any> {
        return request.get({
            url: '/setting/sms/detail',
            params: { alias }
        })
    },

    /**
     * 短信配置保存
     *
     * @param {Object} params
     * @param {string} params.alias
     * @param {string} params.name
     * @param {number} params.status
     * @param {any} params.params
     */
    save(params: {
        alias: string;
        name: string;
        status: number;
        params: any;
    }): Promise<any> {
        return request.post({
            url: '/setting/sms/save',
            params
        })
    }
}

export default smsApi
