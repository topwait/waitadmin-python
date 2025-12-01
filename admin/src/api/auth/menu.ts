import request from '@/utils/request'

const authMenuApi = {
    /**
     * 所有菜单
     *
     * @returns {AuthMenuWholeResponse[]}
     * @author zero
     */
    whole(): Promise<AuthMenuWholeResponse[]> {
        return request.get<AuthMenuWholeResponse[]>({
            url: '/auth/menu/whole'
        })
    },

    /**
     * 菜单列表
     *
     * @returns {AuthMenuListResponse[]}
     * @author zero
     */
    lists(): Promise<AuthMenuListResponse[]> {
        return request.get<AuthMenuListResponse[]>({
            url: '/auth/menu/lists'
        })
    },

    /**
     * 菜单详情
     *
     * @param {number} id
     * @returns {AuthMenuDetailResponse}
     * @author zero
     */
    detail(id: number): Promise<AuthMenuDetailResponse> {
        return request.get<AuthMenuDetailResponse>({
            url: '/auth/menu/detail',
            params: { id }
        })
    },

    /**
     * 菜单新增
     *
     * @param {Object} params
     * @param {number} params.pid
     * @param {string} params.name
     * @param {string} [params.icon]
     * @param {string} [params.icon]
     * @param {number} [params.sort]
     * @param {string} [params.perms]
     * @param {string} [params.params]
     * @param {string} [params.component]
     * @param {string} [params.path]
     * @param {boolean} [params.is_show]
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    add(params: {
        pid: number;
        type: string;
        name: string;
        icon?: string;
        sort?: number;
        perms?: string;
        params?: string;
        component?: string;
        path?: string;
        is_show?: boolean;
        is_disable?: boolean;
    }): Promise<any> {
        return request.post({
            url: '/auth/menu/add',
            params
        })
    },

    /**
     * 菜单编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.pid
     * @param {string} params.name
     * @param {string} [params.icon]
     * @param {string} [params.icon]
     * @param {number} [params.sort]
     * @param {string} [params.perms]
     * @param {string} [params.params]
     * @param {string} [params.component]
     * @param {string} [params.path]
     * @param {boolean} [params.is_show]
     * @param {boolean} [params.is_disable]
     * @returns {Promise<any>}
     * @author zero
     */
    edit(params: {
        id: number;
        pid: number;
        type: string;
        name: string;
        icon?: string;
        sort?: number;
        perms?: string;
        params?: string;
        component?: string;
        path?: string;
        is_show?: boolean;
        is_disable?: boolean;
    }): Promise<any> {
        return request.post({
            url: '/auth/menu/edit',
            params
        })
    },

    /**
     * 菜单删除
     *
     * @param {number} id
     * @returns {Promise<any>}
     * @author zero
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/menu/delete',
            params: { id }
        })
    }
}

export default authMenuApi
