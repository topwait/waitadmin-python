import request from '@/utils/request'

const emailApi = {
    /**
     * 邮箱配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/email/detail'
        })
    },

    /**
     * 邮箱配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/email/save',
            params
        })
    }
}

export default emailApi
