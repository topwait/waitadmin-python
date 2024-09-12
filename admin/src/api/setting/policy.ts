import request from '@/utils/request'

const policyApi = {
    /**
     * 协议配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/policy/detail'
        })
    },

    /**
     * 协议配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/policy/save',
            params
        })
    }
}

export default policyApi
