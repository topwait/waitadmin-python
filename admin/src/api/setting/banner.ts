import request from '@/utils/request'

const bannerApi = {
    /**
     * 轮播图位置
     */
    sites(): Promise<any> {
        return request.get({
            url: '/setting/banner/sites'
        })
    },

    /**
     * 轮播图列表
     */
    lists(params: any): Promise<any> {
        return request.get({
            url: '/setting/banner/lists',
            params
        })
    },

    /**
     * 轮播图详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/setting/banner/detail',
            params: { id }
        })
    },

    /**
     * 轮播图新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/setting/banner/add',
            params
        })
    },

    /**
     * 轮播图保存
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/setting/banner/edit',
            params
        })
    },

    /**
     * 轮播图删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/setting/banner/delete',
            params: { id }
        })
    }
}

export default bannerApi
