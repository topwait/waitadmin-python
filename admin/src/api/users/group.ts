import request from '@/utils/request'

const userGroupApi = {
    /**
     * 用户分组列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        name?: string;
    }): Promise<any> {
        return request.get({
            url: '/users/group/lists',
            params
        })
    },

    /**
     * 用户分组详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/users/group/detail',
            params: { id }
        })
    },

    /**
     * 用户分组新增
     */
    add(params: {
        name: string;
        remarks: string;
        sort?: number;
    }): Promise<any> {
        return request.post({
            url: '/users/group/add',
            params
        })
    },

    /**
     * 用户分组编辑
     */
    edit(params: {
        id: number;
        name: string;
        remarks: string;
        sort?: number;
    }): Promise<any> {
        return request.post({
            url: '/users/group/edit',
            params
        })
    },

    /**
     * 用户分组删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/users/group/delete',
            params: { id: id }
        })
    }
}

export default userGroupApi
