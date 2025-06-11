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
     */
    detail(id: number): Promise<any> {
        return request.get({
            url: '/auth/dept/detail',
            params: { id }
        })
    },

    /**
     * 部门新增
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
     */
    delete(id: number): Promise<any> {
        return request.post({
            url: '/auth/dept/delete',
            params: { id }
        })
    }
}

export default authDeptApi
