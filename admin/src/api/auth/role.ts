import request from '@/utils/request'

const authRoleApi = {
    /**
     * 所有角色
     *
     * @returns {AuthRoleWholeResponse[]}
     * @author zero
     */
    whole(): Promise<AuthRoleWholeResponse[]> {
        return request.get<AuthRoleWholeResponse[]>({
            url: '/auth/role/whole'
        })
    },

    /**
     * 角色列表
     *
     * @param {Object} params
     * @param {number} [params.page_no]
     * @param {number} [params.page_size]
     * @param {string} params.name
     * @returns {AuthRoleListResponse[]}
     * @author zero
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        name?: string;
    }): Promise<AuthRoleListResponse[]> {
        return request.get<AuthRoleListResponse[]>({
            url: '/auth/role/lists',
            params
        })
    },

    /**
     * 角色详情
     *
     * @param {number} id
     * @returns {AuthRoleDetailResponse}
     * @author zero
     */
    detail(id: number): Promise<AuthRoleDetailResponse> {
        return request.get<AuthRoleDetailResponse>({
            url: '/auth/role/detail',
            params: { id }
        })
    },

    /**
     * 角色新增
     *
     * @param {Object} params
     * @param {string} params.name
     * @param {string} [params.describe]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     * @param {number[]} [params.menu_ids]
     * @returns {Promise<any>}
     * @author zero
     */
    add(params: {
        name: string;
        describe?: string;
        sort?: number;
        is_disable?: number;
        menu_ids?: number[];
    }): Promise<any> {
        return request.post({
            url: '/auth/role/add',
            params
        })
    },

    /**
     * 角色编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {string} params.name
     * @param {string} [params.describe]
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     * @param {number[]} [params.menu_ids]
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: {
        id: number;
        name: string;
        describe?: string;
        sort?: number;
        is_disable?: number;
        menu_ids?: number[];
    }): Promise<any> {
        return request.post({
            url: '/auth/role/edit',
            params
        })
    },

    /**
     * 角色删除
     *
     * @param {number} id
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/role/delete',
            params: { id: id }
        })
    }
}

export default authRoleApi
