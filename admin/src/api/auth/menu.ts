import request from '@/utils/request'

const authMenuApi = {
    /**
     * 所有菜单
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/menu/whole'
        })
    },

    /**
     * 菜单列表
     */
    lists(): Promise<any> {
        return request.get({
            url: '/auth/menu/lists'
        })
    },

    /**
     * 菜单详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
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
     * @param {number} [params.is_show]
     * @param {number} [params.is_disable]
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
        is_show?: number;
        is_disable?: number;
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
     * @param {number} [params.is_show]
     * @param {number} [params.is_disable]
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
        is_show?: number;
        is_disable?: number;
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
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/menu/delete',
            params: { id }
        })
    }
}

export default authMenuApi
