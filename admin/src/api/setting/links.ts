import request from '@/utils/request'

const linksApi = {
    /**
     * 友链列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        title?: string;
        is_disable?: number;
    }): Promise<any> {
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
    add(params: {
        title: string;
        image?: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/setting/links/add',
            params
        })
    },

    /**
     * 友链编辑
     */
    edit(params: {
        id: number;
        title: string;
        image?: string;
        target: string;
        url?: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
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
