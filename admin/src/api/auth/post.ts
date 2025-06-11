import request from '@/utils/request'

const authPostApi = {
    /**
     * 所有岗位
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/post/whole'
        })
    },

    /**
     * 岗位列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        code?: string;
        name?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.get({
            url: '/auth/post/lists',
            params
        })
    },

    /**
     * 岗位详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/post/detail',
            params: { id }
        })
    },

    /**
     * 岗位新增
     */
    add(params: {
        code: string;
        name: string;
        remarks?: string;
        sort?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/post/add',
            params
        })
    },

    /**
     * 岗位编辑
     */
    edit(params: {
        id: number;
        code: string;
        name: string;
        remarks?: string;
        sort?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/post/edit',
            params
        })
    },

    /**
     * 岗位删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/post/delete',
            params: { id }
        })
    }
}

export default authPostApi
