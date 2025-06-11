import request from '@/utils/request'

const authRoleApi = {
    /**
     * 所有角色
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/role/whole'
        })
    },

    /**
     * 角色列表
     */
    lists(params: {
        page_no?: number;
        page_size?: number;
        name?: string;
    }): Promise<any> {
        return request.get({
            url: '/auth/role/lists',
            params
        })
    },

    /**
     * 角色详情
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/role/detail',
            params: { id }
        })
    },

    /**
     * 角色新增
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
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/role/delete',
            params: { id: id }
        })
    }
}

export default authRoleApi
