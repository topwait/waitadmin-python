import request from '@/utils/request'

const basicsApi = {
    /**
     * 网站配置详情
     */
    detail(): Promise<any> {
        return request.get({
            url: '/setting/basics/detail'
        })
    },

    /**
     * 网站配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/basics/save',
            params
        })
    }
}

export default basicsApi
