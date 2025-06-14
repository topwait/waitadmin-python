import request from '@/utils/request'

const authDeptApi = {
    /**
     * 所有部门
     */
    whole(): Promise<any> {
        return request.get({
            url: '/auth/dept/whole'
        })
    },

    /**
     * 部门列表
     *
     * @param {string} [params.name]
     * @param {string} [params.mobile]
     * @param {string} [params.is_disable]
     */
    lists(params: {
        name?: string;
        mobile?: string;
        is_disable?: number;
    }): Promise<any> {
        return request.get({
            url: '/auth/dept/lists',
            params
        })
    },

    /**
     * 部门详情
     *
     * @param {number} id
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/dept/detail',
            params: { id }
        })
    },

    /**
     * 部门新增
     *
     * @param {Object} params
     * @param {number} params.pid
     * @param {string} params.name
     * @param {string} params.string
     * @param {string} params.mobile
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    add(params: {
        pid: number;
        name: string;
        duty: string;
        mobile: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/dept/add',
            params
        })
    },

    /**
     * 部门编辑
     *
     * @param {Object} params
     * @param {number} params.id
     * @param {number} params.pid
     * @param {string} params.name
     * @param {string} params.string
     * @param {string} params.mobile
     * @param {number} [params.sort]
     * @param {number} [params.is_disable]
     */
    edit(params: {
        id: number;
        pid: number;
        name: string;
        duty: string;
        mobile: string;
        sort?: number;
        is_disable?: number;
    }): Promise<any> {
        return request.post({
            url: '/auth/dept/edit',
            params
        })
    },

    /**
     * 部门删除
     *
     * @param {number} id
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/dept/delete',
            params: { id }
        })
    }
}

export default authDeptApi
