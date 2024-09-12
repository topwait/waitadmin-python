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
     * 菜单路由
     */
    routes(): Promise<any> {
        return request.get({
            url: '/auth/menu/routes'
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
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/menu/detail',
            params: { id }
        })
    },

    /**
     * 菜单新增
     */
    add(params: any): Promise<any> {
        return request.post({
            url: '/auth/menu/add',
            params
        })
    },

    /**
     * 菜单编辑
     */
    edit(params: any): Promise<any> {
        return request.post({
            url: '/auth/menu/edit',
            params
        })
    },

    /**
     * 菜单删除
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/menu/delete',
            params: { id }
        })
    }
}

export default authMenuApi
