import request from '@/utils/request'

const noticeApi = {
    /**
     * 通知配置列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/setting/notice/lists'
        })
    },

    /**
     * 通知配置详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/notice/detail',
            params: { id }
        })
    },

    /**
     * 通知配置保存
     */
    save(params: any): Promise<any> {
        return request.post({
            url: '/setting/notice/save',
            params
        })
    }
}

export default noticeApi
