import request from '@/utils/request'

const linksApi = {
    /**
     * 友链列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/setting/links/lists',
            params
        })
    },

    /**
     * 友链详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/links/detail',
            params: { id }
        })
    },

    /**
     * 友链新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/setting/links/add',
            params
        })
    },

    /**
     * 友链编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/setting/links/edit',
            params
        })
    },

    /**
     * 友链删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/setting/links/delete',
            params: {
                id
            }
        })
    }
}

export default linksApi
