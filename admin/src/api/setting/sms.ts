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
     */
    detail(alias: string): Promise<any> {
        return request.get({
            url: '/setting/sms/detail',
            params: { alias }
        })
    },

    /**
     * 短信配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/sms/save',
            params
        })
    }
}

export default smsApi
