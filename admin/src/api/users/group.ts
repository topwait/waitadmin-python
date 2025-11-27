import request from '@/utils/request'

const userGroupApi = {
    /**
     * 所有分组列表
     */
    whole(): Promise<UserGroupWholeResponse[]> {
        return request.get<UserGroupWholeResponse[]>({
            url: '/users/group/whole',
        })
    },

    /**
     * 用户分组列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} [params.name]
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        name?: string;
    }): Promise<UserGroupListResponse[]> {
        return request.get<UserGroupListResponse[]>({
            url: '/users/group/lists',
            params
        })
    },

    /**
     * 用户分组详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<UserGroupDetailResponse> {
        return request.get<UserGroupDetailResponse>({
            url: '/users/group/detail',
            params: { id }
        })
    },

    /**
     * 用户分组新增
     *
     * @param {Object} params
     * @param {string} params.name
     * @param {string} params.remarks
     * @param {number} params.sort
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
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.name
     * @param {string} params.remarks
     * @param {number} params.sort
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
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/users/group/delete',
            params: { id: id }
        })
    }
}

export default userGroupApi
